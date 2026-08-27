# vLLM + LiteLLM auf Kubernetes (HAW Hamburg)

Anleitung zur Inbetriebnahme einer LLM-Inferenz-Plattform für studentische
Implementierungsprojekte. Bietet einen OpenAI-kompatiblen Endpoint mit
Per-Student-API-Keys, Quotas und Usage-Tracking. Kein externer Cloud-Cost.

## Zielarchitektur

```
Studierende --(persönlicher LiteLLM-Key)--> LiteLLM-Proxy ──┐
                                                            ↓
                                              ┌──> vLLM (Qwen2.5-7B)
                                              │      auf V100S/32GB
                                              │
                                       Modell auf PVC
                                       (einmalig vom Admin geladen)

                              + PostgreSQL für Keys & Usage
```

Ein zentrales vLLM-Deployment versorgt eine Lehrveranstaltung mit ~30
Studierenden gleichzeitig (KV-Cache via vLLMs Continuous Batching). LiteLLM
sitzt davor und stellt pro Studierendem einen API-Key mit Token-Budget und
Rate-Limit aus.

## Voraussetzungen

- Zugriff auf den Cluster (`kubectl` konfiguriert, gültiges Token)
- Namespace `inf-vllm` existiert (oder entsprechend anpassen)
- StorageClass `rook-ceph-block` verfügbar (oder anpassen)
- NVIDIA GPU Operator installiert, GPUs sichtbar als `nvidia.com/gpu`
- GPU-Nodes haben Tolerations-Taint `nvidia.com/gpu` mit Effect `NoSchedule`
- Hugging-Face-Account mit Access Token (für gated Modelle bzw.
  Rate-Limit-Umgehung beim Download)

Vorab-Verifikation:

```bash
kubectl auth whoami
kubectl get ns inf-vllm
kubectl get nodes -L nvidia.com/gpu.product,nvidia.com/gpu.memory
```

Die letzte Zeile sollte mindestens eine Node mit GPU-Produkt und
Speichergröße zeigen. Notieren Sie das **exakte** Produkt-Label
(z.B. `Tesla-V100S-PCIE-32GB`) – das brauchen wir gleich für den NodeSelector.

## Wichtige Hinweise zu HAW-Cluster-Spezifika

Einige Eigenheiten dieses Clusters, die das Setup beeinflussen:

- **Cluster-DNS-Suffix ist nicht `cluster.local`**, sondern
  `k8s.informatik.haw-hamburg.de`. Alle internen Service-FQDNs müssen das
  verwenden.
- **HRQ (Hierarchical Resource Quotas) erzwingen Resource Limits** auf jedem
  Pod. Ohne `requests` und `limits` für CPU und Memory wird kein Pod
  zugelassen.
- **Heterogene GPU-Hardware**: V100 (16 GB) und V100S (32 GB) im selben
  Cluster. Ohne expliziten Node-Selector kann es passieren, dass Pods auf
  16-GB-Karten landen, obwohl 32 GB benötigt werden.
- **vLLM-Image hat keine V100-Wheels mehr** ab Versionen nach v0.7.3 –
  daher pinnen wir auf eine ältere Version.

## Schritt 1: PVC für Modellgewichte

Die Modellgewichte (~14 GB für Qwen2.5-7B in FP16) werden einmalig
heruntergeladen und auf ein persistentes Volume geschrieben. vLLM-Pods
mounten dieses Volume read-only.

`pvc-vllm.yaml`:

```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: vllm-pvc
  namespace: inf-vllm
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: rook-ceph-block
  resources:
    requests:
      storage: 250Gi
```

250 GB sind großzügig bemessen – reicht für mehrere Modelle parallel
(z.B. später ergänzend Qwen2.5-Coder oder eine quantisierte Variante).

```bash
kubectl apply -f pvc-vllm.yaml
kubectl get pvc -n inf-vllm
# STATUS sollte 'Bound' werden
```

## Schritt 2: Hugging-Face-Token als Secret

Hugging Face verlangt für viele Modelle ein Access Token. Den holen Sie
einmalig auf https://huggingface.co/settings/tokens (Read-Token reicht).

```bash
kubectl create secret generic huggingface-credentials \
  --from-literal=token=hf_IhrTokenHier \
  -n inf-vllm
```

**Tipp:** Ein führendes Leerzeichen vor dem Befehl unterdrückt in den
meisten Shells den History-Eintrag.

## Schritt 3: Modell herunterladen (Init-Job)

Ein einmaliger Job lädt die Modellgewichte ins PVC. Wir nutzen das
vLLM-Image, weil es `huggingface_hub` schon enthält (kein `pip install`
zur Laufzeit nötig) und ohnehin gleich für das Serving gebraucht wird.

`download-qwen25-7b.yaml`:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: download-qwen25-7b
  namespace: inf-vllm
spec:
  template:
    spec:
      restartPolicy: OnFailure
      containers:
        - name: downloader
          image: vllm/vllm-openai:v0.7.3
          command:
            - /bin/sh
            - -c
            - |
              hf download \
                Qwen/Qwen2.5-7B-Instruct \
                --local-dir /models/Qwen2.5-7B-Instruct
          env:
            - name: HF_TOKEN
              valueFrom:
                secretKeyRef:
                  name: huggingface-credentials
                  key: token
          volumeMounts:
            - name: models
              mountPath: /models
          resources:
            requests:
              cpu: "1"
              memory: "1Gi"
            limits:
              cpu: "2"
              memory: "2Gi"
      volumes:
        - name: models
          persistentVolumeClaim:
            claimName: vllm-pvc
```

```bash
kubectl apply -f download-qwen25-7b.yaml
kubectl logs -n inf-vllm -l job-name=download-qwen25-7b -f
```

Dauert je nach Netzanbindung 10–20 Minuten. Der Job ist fertig, wenn
`kubectl get jobs -n inf-vllm` `COMPLETIONS: 1/1` zeigt.

**Falls der Job mit "command not found" für `hf` abbricht:** Älteres
Image mit nur `huggingface-cli` als Befehl. Dann im Command `hf` durch
`huggingface-cli` ersetzen.

## Schritt 4: vLLM-Deployment

Hier kommen die V100-spezifischen Anpassungen ins Spiel:

- **`image: vllm/vllm-openai:v0.7.3`** – neuere Versionen enthalten keine
  CUDA-Kernels für V100 (Compute Capability 7.0) mehr.
- **`--dtype=half`** – V100 unterstützt kein BF16 nativ, nur FP16.
- **`nodeSelector` auf 32-GB-Karten** – sonst landet der Pod ggf. auf
  einer 16-GB-V100, in die Qwen2.5-7B nicht entspannt passt.
- **Toleration für GPU-Taint** – sonst lässt der Scheduler den Pod nicht
  auf die GPU-Nodes.
- **Shared-Memory-Volume** – vLLM braucht > 64 MB shm; Container-Default
  reicht nicht.

`vllm-qwen25-7b.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-qwen25-7b
  namespace: inf-vllm
  labels:
    app: vllm-qwen25-7b
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vllm-qwen25-7b
  strategy:
    type: Recreate                      # GPU exklusiv -> kein RollingUpdate
  template:
    metadata:
      labels:
        app: vllm-qwen25-7b
    spec:
      nodeSelector:
        # Stellt sicher, dass nur 32-GB-Karten gewählt werden.
        # Den exakten Wert mit 'kubectl get nodes -L nvidia.com/gpu.product'
        # verifizieren.
        nvidia.com/gpu.product: "Tesla-V100S-PCIE-32GB"
      tolerations:
        # GPU-Nodes sind getaintet, damit nur GPU-Workloads dort schedulen.
        - key: "nvidia.com/gpu"
          operator: "Exists"
          effect: "NoSchedule"
      containers:
        - name: vllm
          image: vllm/vllm-openai:v0.7.3
          args:
            - "--model=/models/Qwen2.5-7B-Instruct"
            - "--served-model-name=qwen2.5-7b"
            - "--dtype=half"             # FP16 statt BF16 (V100-Pflicht)
            - "--max-model-len=8192"     # konservativ wegen fehlender FlashAttn2
            - "--gpu-memory-utilization=0.90"
            - "--enable-prefix-caching"
            - "--host=0.0.0.0"
            - "--port=8000"
          ports:
            - name: http
              containerPort: 8000
          env:
            - name: HF_HUB_OFFLINE
              value: "1"                 # keine HF-Calls zur Laufzeit
          volumeMounts:
            - name: models
              mountPath: /models
              readOnly: true
            - name: shm
              mountPath: /dev/shm
          resources:
            requests:
              cpu: "4"
              memory: "16Gi"
              nvidia.com/gpu: 1
            limits:
              cpu: "8"
              memory: "32Gi"
              nvidia.com/gpu: 1
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 60
            periodSeconds: 10
            failureThreshold: 30         # bis zu 5 Min für Modell-Load
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 300
            periodSeconds: 30
            failureThreshold: 3
      volumes:
        - name: models
          persistentVolumeClaim:
            claimName: vllm-pvc
        - name: shm
          emptyDir:
            medium: Memory
            sizeLimit: 4Gi

---
apiVersion: v1
kind: Service
metadata:
  name: vllm-qwen25-7b
  namespace: inf-vllm
  labels:
    app: vllm-qwen25-7b
spec:
  type: ClusterIP
  selector:
    app: vllm-qwen25-7b
  ports:
    - name: http
      port: 8000
      targetPort: 8000
      protocol: TCP
```

```bash
kubectl apply -f vllm-qwen25-7b.yaml
kubectl get pods -n inf-vllm -l app=vllm-qwen25-7b -w
# warten bis READY 1/1 (Modell-Load dauert 1-2 Minuten)

kubectl logs -n inf-vllm -l app=vllm-qwen25-7b -f
# bei Erfolg sehen Sie: "Uvicorn running on http://0.0.0.0:8000"
```

### Smoke-Test direkt gegen vLLM

```bash
kubectl port-forward -n inf-vllm svc/vllm-qwen25-7b 8000:8000
```

In einem zweiten Terminal:

```bash
curl http://localhost:8000/v1/models

curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-7b",
    "messages": [{"role": "user", "content": "Erkläre Kubernetes in einem Satz."}],
    "max_tokens": 100
  }'
```

Wenn beide Calls funktionieren, ist die Inferenz-Schicht produktiv.

## Schritt 5: PostgreSQL für LiteLLM

LiteLLM speichert API-Keys und Usage-Daten in einer Postgres-Datenbank.
Wir machen es minimal: ein einzelner Pod mit eigenem PVC. Für eine
Lehrveranstaltung absolut ausreichend.

**Wichtig: Passwort URL-safe wählen!** Sonderzeichen wie `/`, `+`, `:`
in Connection-Strings führen zu kryptischen Prisma-Fehlern (`P1013:
invalid port number`). `openssl rand -hex 24` liefert nur Hex-Zeichen
und ist garantiert sicher.

```bash
PG_PASSWORD=$(openssl rand -hex 24)
echo "Postgres-Passwort: $PG_PASSWORD"   # einmal notieren

kubectl create secret generic litellm-postgres \
  --from-literal=postgres-password="$PG_PASSWORD" \
  --from-literal=database-url="postgresql://litellm:${PG_PASSWORD}@litellm-postgres:5432/litellm" \
  -n inf-vllm
```

Das Secret enthält zwei Felder: `postgres-password` für den DB-Pod
selbst, `database-url` als kompletter Connection-String für LiteLLM.
Beide müssen dasselbe Passwort verwenden, deshalb in einem Aufwasch
erzeugt.

`litellm-postgres.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: litellm-postgres-pvc
  namespace: inf-vllm
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: rook-ceph-block
  resources:
    requests:
      storage: 10Gi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: litellm-postgres
  namespace: inf-vllm
  labels:
    app: litellm-postgres
spec:
  replicas: 1
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: litellm-postgres
  template:
    metadata:
      labels:
        app: litellm-postgres
    spec:
      containers:
        - name: postgres
          image: postgres:16-alpine
          ports:
            - name: postgres
              containerPort: 5432
          env:
            - name: POSTGRES_DB
              value: litellm
            - name: POSTGRES_USER
              value: litellm
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: litellm-postgres
                  key: postgres-password
            - name: PGDATA
              value: /var/lib/postgresql/data/pgdata
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
          resources:
            requests:
              cpu: "200m"
              memory: "512Mi"
            limits:
              cpu: "1"
              memory: "2Gi"
          readinessProbe:
            exec:
              command: ["pg_isready", "-U", "litellm", "-d", "litellm"]
            initialDelaySeconds: 10
            periodSeconds: 5
          livenessProbe:
            exec:
              command: ["pg_isready", "-U", "litellm", "-d", "litellm"]
            initialDelaySeconds: 30
            periodSeconds: 30
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: litellm-postgres-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: litellm-postgres
  namespace: inf-vllm
  labels:
    app: litellm-postgres
spec:
  type: ClusterIP
  selector:
    app: litellm-postgres
  ports:
    - name: postgres
      port: 5432
      targetPort: 5432
      protocol: TCP
```

```bash
kubectl apply -f litellm-postgres.yaml
kubectl rollout status deployment/litellm-postgres -n inf-vllm
```

## Schritt 6: LiteLLM-Master-Key

Mit dem Master-Key erzeugt der Admin später die Studierenden-Keys. Er
gehört in den Admin-Passwort-Tresor – behandeln Sie ihn wie ein
Datenbank-Root-Passwort.

```bash
LITELLM_MASTER_KEY="sk-$(openssl rand -hex 24)"
echo "Master-Key: $LITELLM_MASTER_KEY"   # in den Tresor!

kubectl create secret generic litellm-master-key \
  --from-literal=master-key="$LITELLM_MASTER_KEY" \
  -n inf-vllm
```

## Schritt 7: LiteLLM-Proxy

Mehrere wichtige Details:

- **Image: `litellm-database:main-stable`** statt `litellm:main-stable`.
  Nur die `-database`-Variante enthält die Prisma-Schemas und kann
  beim Start Migrations ausführen.
- **`--num_workers 1`** – mehr Worker führen zu Prisma-Race-Conditions.
- **Init-Container `wait-for-postgres`** – LiteLLM startet sonst
  möglicherweise vor Postgres und schlägt fehl.
- **`api_base` mit HAW-spezifischem DNS-Suffix** – nicht
  `cluster.local`, sondern `k8s.informatik.haw-hamburg.de`.

`litellm.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: litellm-config
  namespace: inf-vllm
data:
  config.yaml: |
    model_list:
      - model_name: qwen2.5-7b
        litellm_params:
          model: openai/qwen2.5-7b
          # WICHTIG: HAW-Cluster nutzt 'k8s.informatik.haw-hamburg.de'
          # statt 'cluster.local' als Cluster-Domain.
          api_base: http://vllm-qwen25-7b.inf-vllm.svc.k8s.informatik.haw-hamburg.de:8000/v1
          api_key: "dummy"

    general_settings:
      master_key: os.environ/LITELLM_MASTER_KEY
      database_url: os.environ/DATABASE_URL
      default_max_budget: 10.0
      default_team_budget: 100.0

    litellm_settings:
      drop_params: True
      set_verbose: False
      json_logs: True

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: litellm
  namespace: inf-vllm
  labels:
    app: litellm
spec:
  replicas: 1
  selector:
    matchLabels:
      app: litellm
  template:
    metadata:
      labels:
        app: litellm
    spec:
      initContainers:
        - name: wait-for-postgres
          image: postgres:16-alpine
          command:
            - sh
            - -c
            - |
              until pg_isready -h litellm-postgres -p 5432 -U litellm; do
                echo "Warte auf Postgres..."
                sleep 2
              done
              echo "Postgres bereit."
          resources:
            requests:
              cpu: "50m"
              memory: "64Mi"
            limits:
              cpu: "200m"
              memory: "128Mi"
      containers:
        - name: litellm
          image: ghcr.io/berriai/litellm-database:main-stable
          args:
            - "--config"
            - "/etc/litellm/config.yaml"
            - "--port"
            - "4000"
            - "--num_workers"
            - "1"
          ports:
            - name: http
              containerPort: 4000
          env:
            - name: LITELLM_MASTER_KEY
              valueFrom:
                secretKeyRef:
                  name: litellm-master-key
                  key: master-key
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: litellm-postgres
                  key: database-url
          volumeMounts:
            - name: config
              mountPath: /etc/litellm
              readOnly: true
          resources:
            requests:
              cpu: "200m"
              memory: "512Mi"
            limits:
              cpu: "2"
              memory: "2Gi"
          readinessProbe:
            httpGet:
              path: /health/readiness
              port: 4000
            initialDelaySeconds: 60
            periodSeconds: 10
            failureThreshold: 12
          livenessProbe:
            httpGet:
              path: /health/liveness
              port: 4000
            initialDelaySeconds: 120
            periodSeconds: 30
      volumes:
        - name: config
          configMap:
            name: litellm-config

---
apiVersion: v1
kind: Service
metadata:
  name: litellm
  namespace: inf-vllm
  labels:
    app: litellm
spec:
  type: ClusterIP
  selector:
    app: litellm
  ports:
    - name: http
      port: 4000
      targetPort: 4000
      protocol: TCP
```

```bash
kubectl apply -f litellm.yaml
kubectl rollout status deployment/litellm -n inf-vllm
kubectl logs -n inf-vllm -l app=litellm -f
```

Bei Erfolg sollten Sie in den Logs sehen:

```
Postgres bereit.
Running prisma migrate deploy
... migrations applied
LiteLLM: Proxy initialized with Config, Set models: qwen2.5-7b
Application startup complete.
Uvicorn running on http://0.0.0.0:4000
```

### Smoke-Test über alle Ebenen

```bash
kubectl port-forward -n inf-vllm svc/litellm 4000:4000
```

In einem zweiten Terminal:

```bash
export LITELLM_MASTER_KEY="sk-..."   # Wert aus Schritt 6

curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-7b",
    "messages": [{"role": "user", "content": "Sag Hallo auf Deutsch."}],
    "max_tokens": 50
  }'
```

Wenn hier eine sinnvolle Antwort kommt, läuft die ganze Kette: LiteLLM
authentifiziert den Master-Key, schreibt einen Eintrag in Postgres,
leitet das Request über den Cluster-DNS an vLLM weiter, dessen Antwort
kommt zurück.

## Schritt 8: Studierenden-Keys erzeugen

Ein einzelner Key per API-Call:

```bash
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "max.mustermann@haw-hamburg.de",
    "key_alias": "ws25-agentic-ai-max",
    "models": ["qwen2.5-7b"],
    "max_budget": 10.0,
    "budget_duration": "30d",
    "tpm_limit": 50000,
    "rpm_limit": 60,
    "duration": "120d"
  }'
```

Die Antwort enthält einen `key`-Wert (`sk-...`), den Sie dem
Studierenden zustellen. Was die Felder bewirken:

- `user_id`, `key_alias`: Logging und spätere Zuordnung
- `models`: welche Modelle dieser Key nutzen darf
- `max_budget`: Token-Spend-Cap (LiteLLM rechnet intern um, auch wenn
  Ihre Modelle "kostenlos" laufen – nützlich für Missbrauchserkennung)
- `tpm_limit` / `rpm_limit`: Echtzeit-Drosseln pro Key
- `duration`: Key läuft am Semesterende automatisch ab

Für Bulk-Erzeugung gegen eine CSV-Liste der Kursteilnehmer ein
schlankes Python-Skript:

```python
import csv, requests, os

MASTER_KEY = os.environ["LITELLM_MASTER_KEY"]
BASE_URL = "http://localhost:4000"  # bzw. spätere Public-URL

with open("students.csv") as f:
    for row in csv.DictReader(f):
        r = requests.post(
            f"{BASE_URL}/key/generate",
            headers={"Authorization": f"Bearer {MASTER_KEY}"},
            json={
                "user_id": row["email"],
                "key_alias": f"ws25-{row['matrikel']}",
                "models": ["qwen2.5-7b"],
                "max_budget": 10.0,
                "duration": "120d",
                "tpm_limit": 50000,
                "rpm_limit": 60,
            },
        )
        key = r.json()["key"]
        print(f"{row['email']},{key}")  # später per Mail versenden
```

## Was Studierende konkret bekommen

Drei Informationen pro Studierendem:

```
LLM-Service der HAW Hamburg – Zugangsdaten
───────────────────────────────────────────
OPENAI_API_BASE:     http://localhost:4000/v1   (bzw. Public-URL nach Ingress)
OPENAI_API_KEY:      sk-XYZab123…  (persönlich, nicht weitergeben)
Verfügbares Modell:  qwen2.5-7b
Budget:              $10 / 30 Tage   |   60 Requests/min
```

Damit kann der Studierende sofort loslegen:

```python
from openai import OpenAI
client = OpenAI()  # liest OPENAI_API_BASE und OPENAI_API_KEY aus env
resp = client.chat.completions.create(
    model="qwen2.5-7b",
    messages=[{"role": "user", "content": "Hallo!"}]
)
```

Identisch zu OpenAI/Anthropic/Co. – das ist genau die didaktische
Pointe: Industrie-Standard-Interface ohne Kosten.

## Troubleshooting

Diagnose-Befehle für die häufigsten Probleme.

### Pod startet nicht

```bash
kubectl get pods -n inf-vllm
kubectl describe pod -n inf-vllm <pod-name> | tail -30
kubectl logs -n inf-vllm <pod-name> [--previous]
```

### vLLM-Pod: "no kernel image is available for execution on the device"

Image enthält keine V100-Kernels. Auf `vllm/vllm-openai:v0.7.3` pinnen.

### vLLM-Pod: CUDA out of memory

Wahrscheinlich auf 16-GB-V100 statt 32-GB-V100S geschedult. Prüfen mit:

```bash
kubectl get pod -n inf-vllm -l app=vllm-qwen25-7b -o wide
# NODE-Spalte notieren
kubectl describe node <node-name> | grep -i "gpu.product\|gpu.memory"
```

`nodeSelector` im Manifest auf 32-GB-Karten verschärfen.

### LiteLLM: "Connection error" trotz funktionierendem vLLM

DNS-Suffix prüfen. Aus einem Debug-Pod im selben Namespace testen:

```bash
kubectl run dns-test --rm -it --restart=Never \
  --image=curlimages/curl:latest \
  -n inf-vllm \
  --overrides='{"spec":{"containers":[{"name":"dns-test","image":"curlimages/curl:latest","resources":{"requests":{"cpu":"100m","memory":"64Mi"},"limits":{"cpu":"200m","memory":"128Mi"}},"command":["sh","-c","cat /etc/resolv.conf; echo; nslookup vllm-qwen25-7b"]}]}}'
```

Die `search`-Domain in `/etc/resolv.conf` zeigt das echte Cluster-Suffix.

### LiteLLM: "P1013: invalid port number in database URL"

Sonderzeichen im Postgres-Passwort. Mit `openssl rand -hex 24` neu
erzeugen, **PVC zwingend mit löschen**, sonst behält Postgres das
alte Passwort:

```bash
kubectl delete deployment litellm-postgres -n inf-vllm
kubectl delete pvc litellm-postgres-pvc -n inf-vllm
kubectl delete secret litellm-postgres -n inf-vllm
# dann ab Schritt 5 neu
```

### "exceeded its progress deadline" bei `kubectl rollout status`

Generische Meldung, sagt nur "10 Min nicht ready geworden". Echte
Ursache in den Pod-Logs (`kubectl logs --previous` falls schon
abgestürzt).

### "must specify limits.cpu for ..." beim `kubectl run`

HRQ erzwingt Limits. `kubectl run` ohne Resource-Overrides geht nicht;
stattdessen Mini-Manifest schreiben oder `--overrides='{"spec":...}'`
mitgeben.

## Komplettes Cleanup

Alle Ressourcen freigeben. Wichtig: Reihenfolge beachten – erst
Workloads, dann Storage und Secrets.

```bash
# 1. Workloads stoppen
kubectl delete deployment litellm -n inf-vllm
kubectl delete deployment litellm-postgres -n inf-vllm
kubectl delete deployment vllm-qwen25-7b -n inf-vllm

# 2. Services und ConfigMap
kubectl delete service litellm -n inf-vllm
kubectl delete service litellm-postgres -n inf-vllm
kubectl delete service vllm-qwen25-7b -n inf-vllm
kubectl delete configmap litellm-config -n inf-vllm

# 3. Etwaige Jobs / Test-Pods
kubectl delete job download-qwen25-7b -n inf-vllm --ignore-not-found
kubectl delete pod --all -n inf-vllm --field-selector=status.phase!=Running

# 4. Secrets
kubectl delete secret litellm-master-key -n inf-vllm
kubectl delete secret litellm-postgres -n inf-vllm
kubectl delete secret huggingface-credentials -n inf-vllm

# 5. PVCs (= echte Speicher-Freigabe)
kubectl delete pvc litellm-postgres-pvc -n inf-vllm
kubectl delete pvc vllm-pvc -n inf-vllm

# 6. Verifikation
kubectl get all,pvc,secret,configmap -n inf-vllm
# sollte leer (oder fast leer) sein
```

**Achtung beim PVC-Löschen:** `vllm-pvc` enthält die heruntergeladenen
Modellgewichte (mehrere GB). Wenn Sie das Setup später wieder aufbauen
wollen, müssen Sie die Modelle neu laden. Falls Sie das vermeiden
wollen, lassen Sie das PVC stehen – beim nächsten Setup mounten dann
neue Pods das vorhandene Modell direkt.

Falls der Namespace `inf-vllm` selbst gelöscht werden soll (löscht
*alles* darin in einem Schritt):

```bash
kubectl delete namespace inf-vllm
```

Das dauert manchmal mehrere Minuten, weil Kubernetes alle Ressourcen
sequenziell aufräumt.

## Nächste Schritte (optional)

Wenn der Pilotbetrieb läuft, sind das die naheliegenden Erweiterungen:

- **Ingress + TLS** für externen Zugang unter
  `llm.inf.haw-hamburg.de` (cert-manager mit Hochschul-PKI oder
  Let's Encrypt).
- **Observability**: Prometheus-Scrape von vLLM (`/metrics`-Endpoint)
  und LiteLLM, Grafana-Dashboard, optional Langfuse für Trace-Logging
  studentischer Agenten-Workflows.
- **SSO-Integration** über LiteLLMs OIDC-Support, statt Keys per
  Skript zu verteilen.
- **Weitere Modelle** parallel: Qwen2.5-Coder für Programmierprojekte
  oder eine quantisierte 14B-Variante für anspruchsvollere Aufgaben.
