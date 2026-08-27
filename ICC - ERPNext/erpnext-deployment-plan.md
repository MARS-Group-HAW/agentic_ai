# ERPNext-Service auf der ICC — Deployment-Plan (Entwurf)

Diese Datei ist ein **Plan**, kein bereits getesteter Aufbau wie
`../ICC - vLLM/final/vllm-litellm-setup.md`. Sie beschreibt, wie ein Frappe/ERPNext-Bench mit einer
isolierten Site pro Studierendenfirma auf der ICC aufgesetzt werden soll. Firmenname, Ressourcenwerte
und einige Frappe-spezifische Details sind Annahmen und müssen vor der ersten Anwendung gegen den
echten Cluster und die aktuelle [frappe_docker](https://github.com/frappe/frappe_docker)-Dokumentation
geprüft werden — mit ⚠️ markiert.

## Zielarchitektur

Ein gemeinsamer Frappe-Bench (ein App-Image, ein Satz Worker-/Scheduler-/Socket.IO-Pods) hostet für
jede Firma eine eigene **Site** — eigene Datenbank, eigene Dateien, eigene Subdomain, eigenes
Administrator-Login. Das gibt jedem Team "seine eigene Instanz" (wie im Student Company Handbook
gefordert), ohne fünf komplett getrennte Deployments betreiben zu müssen.

```
inf-erpnext (neuer Namespace, getrennt vom GPU-Kontingent in inf-vllm)
├── MariaDB (1 Pod, RWO-PVC)
├── Redis Cache (1 Pod)
├── Redis Queue (1 Pod)
├── sites/ (RWX-PVC, von allen Frappe-Pods gemeinsam gemountet)  ⚠️
├── configurator (Init-Job, schreibt common_site_config.json)
├── erpnext-web        (Deployment, Backend/Gunicorn)
├── erpnext-socketio   (Deployment)
├── erpnext-scheduler  (Deployment, genau 1 Replica!)
├── erpnext-worker-short / erpnext-worker-long (Deployments)
└── Ingress — ein Host pro Firma:
      firma-a.erp.inf.haw-hamburg.de → erpnext-web
      firma-b.erp.inf.haw-hamburg.de → erpnext-web
      ...
```

## Voraussetzungen

- Eigener Namespace (Vorschlag: `inf-erpnext`) mit CPU/RAM/Storage-Kontingent — separat vom
  GPU-Kontingent in `inf-vllm` beantragen, da diese Last CPU-/DB-gebunden ist und keine GPU braucht.
- ⚠️ **RWX-fähige StorageClass** (z. B. CephFS) — mit ICC klären, ob eine existiert
  (`kubectl get storageclass` zeigt die verfügbaren Klassen). `rook-ceph-block`, das in
  `ICC - vLLM/` verwendet wird, ist nur ReadWriteOnce und reicht hier **nicht**, weil mehrere
  Frappe-Pods gleichzeitig auf `sites/` zugreifen müssen. Falls keine RWX-Klasse verfügbar ist,
  ersatzweise ein In-Cluster-NFS-Pod auf einer RWO-Platte.
- DNS: eine Subdomain pro Firma (z. B. `firma-a.erp.inf.haw-hamburg.de`) — Frappe routet
  Multi-Tenancy über den Host-Header; Pfad-basiertes Routing auf einem einzigen Host funktioniert
  dafür nicht zuverlässig.
- ⚠️ Klären, ob Helm-Releases im ICC-Namespace erlaubt sind. Der offizielle Weg für produktive
  Frappe-Bench-Deployments ist der Helm-Chart unter [helm.erpnext.com](https://helm.erpnext.com/)
  (Repo `frappe/helm`) — er verwaltet die Mehr-Pod-Topologie deutlich robuster als Hand-YAML. Die
  folgenden Schritte zeigen trotzdem den Hand-YAML-Weg (konsistent mit dem Rest von
  `ICC - vLLM/`); wenn Helm erlaubt ist, ist er vorzuziehen.

## Wichtige Unterschiede zum vLLM-Setup

- Kein GPU-Taint nötig — dieser Service läuft auf normalen CPU-Nodes.
- Mehrere Pods teilen sich einen Datenordner (`sites/`) → RWX statt RWO (siehe oben).
- Mehrere Firmen = mehrere **Sites** auf einer Bench, nicht mehrere Bench-Installationen. Ein
  `bench new-site` pro Firma reicht; Container-Image, Worker und Scheduler laufen nur einmal.
- Keine Modell-Download-Phase wie bei vLLM — dafür eine Site-Erstellungsphase pro Firma (Schritt 6).

## Schritt 1: PVCs und DB-Secret

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: erpnext-sites-pvc
  namespace: inf-erpnext
spec:
  accessModes:
    - ReadWriteMany          # ⚠️ StorageClass muss RWX unterstützen
  storageClassName: <RWX-STORAGECLASS>   # ⚠️ mit ICC klären, welche das ist
  resources:
    requests:
      storage: 50Gi

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mariadb-pvc
  namespace: inf-erpnext
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: rook-ceph-block
  resources:
    requests:
      storage: 20Gi
```

Root-Passwort analog zum LiteLLM-Setup generieren und **nicht** im Klartext ins Repo committen:

```bash
DB_ROOT_PASSWORD=$(openssl rand -hex 24)
kubectl create secret generic erpnext-db-secret \
  --from-literal=mariadb-root-password="$DB_ROOT_PASSWORD" \
  -n inf-erpnext
```

## Schritt 2: MariaDB

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mariadb
  namespace: inf-erpnext
  labels:
    app: mariadb
spec:
  replicas: 1
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: mariadb
  template:
    metadata:
      labels:
        app: mariadb
    spec:
      containers:
        - name: mariadb
          image: mariadb:10.6            # ⚠️ Version gegen aktuelle frappe_docker-Empfehlung prüfen
          args:
            - --character-set-server=utf8mb4
            - --collation-server=utf8mb4_unicode_ci
            - --skip-character-set-client-handshake
            - --skip-innodb-read-only-compressed
          env:
            - name: MARIADB_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: erpnext-db-secret
                  key: mariadb-root-password
          ports:
            - containerPort: 3306
          volumeMounts:
            - name: data
              mountPath: /var/lib/mysql
          resources:
            requests:
              cpu: "500m"
              memory: "1Gi"
            limits:
              cpu: "2"
              memory: "4Gi"
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: mariadb-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: mariadb
  namespace: inf-erpnext
spec:
  selector:
    app: mariadb
  ports:
    - port: 3306
      targetPort: 3306
```

## Schritt 3: Redis (Cache + Queue)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-cache
  namespace: inf-erpnext
spec:
  replicas: 1
  selector:
    matchLabels: { app: redis-cache }
  template:
    metadata:
      labels: { app: redis-cache }
    spec:
      containers:
        - name: redis
          image: redis:7-alpine
          ports: [{ containerPort: 6379 }]
          resources:
            requests: { cpu: "100m", memory: "128Mi" }
            limits: { cpu: "500m", memory: "512Mi" }
---
apiVersion: v1
kind: Service
metadata:
  name: redis-cache
  namespace: inf-erpnext
spec:
  selector: { app: redis-cache }
  ports: [{ port: 6379, targetPort: 6379 }]

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-queue
  namespace: inf-erpnext
spec:
  replicas: 1
  selector:
    matchLabels: { app: redis-queue }
  template:
    metadata:
      labels: { app: redis-queue }
    spec:
      containers:
        - name: redis
          image: redis:7-alpine
          ports: [{ containerPort: 6379 }]
          resources:
            requests: { cpu: "100m", memory: "128Mi" }
            limits: { cpu: "500m", memory: "512Mi" }
---
apiVersion: v1
kind: Service
metadata:
  name: redis-queue
  namespace: inf-erpnext
spec:
  selector: { app: redis-queue }
  ports: [{ port: 6379, targetPort: 6379 }]
```

⚠️ frappe_docker führt teils noch eine dritte Redis-Instanz für Socket.IO, teils mappt es das auf
`redis-queue` — vor Schritt 4 gegen die aktuelle frappe_docker-Doku prüfen.

## Schritt 4: Configurator (Init-Job)

Schreibt `sites/common_site_config.json` einmalig; danach beendet sich der Pod.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: erpnext-configurator
  namespace: inf-erpnext
spec:
  template:
    spec:
      restartPolicy: OnFailure
      containers:
        - name: configurator
          image: frappe/erpnext-worker:v15   # ⚠️ Tag gegen frappe_docker-Releases prüfen
          command: ["bash", "/opt/frappe_docker_scripts/configure.py"]  # ⚠️ exakten Befehl aus frappe_docker/docs übernehmen
          env:
            - { name: DB_HOST, value: mariadb }
            - { name: DB_PORT, value: "3306" }
            - { name: REDIS_CACHE, value: "redis-cache:6379" }
            - { name: REDIS_QUEUE, value: "redis-queue:6379" }
            - { name: SOCKETIO_PORT, value: "9000" }
          volumeMounts:
            - { name: sites, mountPath: /home/frappe/frappe-bench/sites }
      volumes:
        - name: sites
          persistentVolumeClaim:
            claimName: erpnext-sites-pvc
```

## Schritt 5: Frappe-Deployments (Web, Socket.IO, Scheduler, Worker)

Alle vier teilen sich `erpnext-sites-pvc` und dasselbe Image — nur Command/Rolle unterscheiden sich,
analog zu frappe_docker's `docker-compose.yml`. Gerüst für den Web-Pod:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: erpnext-web
  namespace: inf-erpnext
spec:
  replicas: 1
  selector:
    matchLabels: { app: erpnext-web }
  template:
    metadata:
      labels: { app: erpnext-web }
    spec:
      containers:
        - name: web
          image: frappe/erpnext-worker:v15   # ⚠️ Tag prüfen
          command: ["bash", "-c", "bench serve --port 8000"]   # ⚠️ frappe_docker-Standardkommando übernehmen
          ports: [{ containerPort: 8000 }]
          volumeMounts:
            - { name: sites, mountPath: /home/frappe/frappe-bench/sites }
          resources:
            requests: { cpu: "500m", memory: "1Gi" }
            limits: { cpu: "2", memory: "2Gi" }
      volumes:
        - name: sites
          persistentVolumeClaim:
            claimName: erpnext-sites-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: erpnext-web
  namespace: inf-erpnext
spec:
  selector: { app: erpnext-web }
  ports: [{ port: 8000, targetPort: 8000 }]
```

Socket.IO-, Scheduler- und Worker-Deployments folgen demselben Muster, mit den in frappe_docker
dokumentierten Commands (`node socketio.js`, `bench schedule`, `bench worker --queue short,default` /
`--queue long`) und **genau 1 Replica beim Scheduler** — mehrere Scheduler-Pods erzeugen doppelte
Cron-Läufe.

## Schritt 6: Site pro Firma anlegen

Einmalig pro Firma, als Job oder `kubectl exec`:

```bash
kubectl exec -n inf-erpnext deploy/erpnext-web -- \
  bench new-site firma-a.erp.inf.haw-hamburg.de \
    --mariadb-root-password "$DB_ROOT_PASSWORD" \
    --admin-password "$(openssl rand -hex 12)" \
    --install-app erpnext
```

Admin-Passwort pro Firma sicher (nicht ins Repo) an das jeweilige Team weitergeben. Eine Firma
zurücksetzen = Site löschen (`bench drop-site`) und neu anlegen — betrifft keine andere Firma.

## Schritt 7: Ingress pro Firma

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: erpnext-firma-a
  namespace: inf-erpnext
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-production
spec:
  ingressClassName: nginx
  rules:
    - host: firma-a.erp.inf.haw-hamburg.de
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: erpnext-web
                port: { number: 8000 }
  tls:
    - secretName: firma-a-erp-tls
      hosts: [firma-a.erp.inf.haw-hamburg.de]
```

Ein Ingress-Objekt pro Firma, alle auf denselben `erpnext-web`-Service — Frappe entscheidet anhand
des Host-Headers, welche Site bedient wird. ⚠️ Socket.IO braucht ggf. eine eigene Pfad-Route auf
demselben Ingress — prüfen.

## Schritt 8: Backups

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: erpnext-backup-firma-a
  namespace: inf-erpnext
spec:
  schedule: "0 3 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: backup
              image: frappe/erpnext-worker:v15
              command: ["bench", "--site", "firma-a.erp.inf.haw-hamburg.de", "backup"]
              volumeMounts:
                - { name: sites, mountPath: /home/frappe/frappe-bench/sites }
          volumes:
            - name: sites
              persistentVolumeClaim:
                claimName: erpnext-sites-pvc
```

Ein CronJob pro Firma (oder ein Script, das über alle Sites iteriert).

## Offene Punkte vor der ersten Umsetzung

1. **Blockierend:** Ist eine RWX-fähige StorageClass auf der ICC verfügbar?
2. Sind Helm-Releases im Namespace erlaubt? (entscheidet, ob der robustere Helm-Chart-Weg möglich ist)
3. Exakte Image-Tags und Bench-Commands gegen die aktuelle
   [frappe_docker-Doku](https://github.com/frappe/frappe_docker) prüfen — hier nur als Platzhalter markiert.
4. DNS-Delegation für `*.erp.inf.haw-hamburg.de` oder einzelne Records pro Firma?
5. Eigenes Ressourcenkontingent bei ICC beantragen (separat vom GPU-Kontingent in `inf-vllm`).
6. Lasttest mit gleichzeitigem Zugriff mehrerer Firmen vor Semesterstart.

## Nächste Schritte

- Offene Punkte oben mit ICC klären.
- Nach Klärung: Schritte 1–8 tatsächlich ausführen und — wie beim vLLM-Setup — zu einem verifizierten
  Walkthrough mit Troubleshooting-Abschnitt ausbauen.
- Studierenden-Guide analog zu `../ICC - vLLM/final/llm-service-fuer-studierende.md` schreiben,
  sobald die Sites stehen.
