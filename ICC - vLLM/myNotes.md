## Homebrew

### Prüfen, welche Pakete veraltet sind (ohne zu aktualisieren)

`brew outdated`

### Homebrew selbst aktualisieren

`brew update`

### Alle Pakete aktualisieren

`brew upgrade`

### Aufräumen

`brew cleanup`

## UV

[https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

`brew install uv`


## Hugging Face CLI

[https://huggingface.co/docs/huggingface_hub/en/guides/cli](https://huggingface.co/docs/huggingface_hub/en/guides/cli)



## ICC

### Doku
[https://doc.inf.haw-hamburg.de/Dienste/icc/getting-started/](https://doc.inf.haw-hamburg.de/Dienste/icc/getting-started/)

### Config-Datei
[https://icc-login.informatik.haw-hamburg.de](https://icc-login.informatik.haw-hamburg.de)

`mv ~/Downloads/config.txt ~/.kube/config`

### Namespace

`inf-vllm`

### HuggingFace Secret generieren
[https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

`kubectl create secret generic huggingface-credentials --from-literal=token=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 -n inf-vllm`
 
### Modell Download in der ICC anstoßen 
 
`kubectl apply -f download-qwen25-14b.yaml -n inf-vllm`

### Fortschritt überprüfen

`kubectl get pods -n inf-vllm`  
`kubectl get jobs -n inf-vllm`  
`kubectl -n inf-vllm describe pod download-qwen25-14b-w5hvk`
 
 
### Secret für PostgreSQL für LiteLLM
 
 `PG_PASSWORD=$(openssl rand -hex 24)`    
 `echo "Passwort: $PG_PASSWORD"  # einmal notieren, falls Sie es brauchen`  
 
 Passwort: a485a916a2f1bfcbf863443928fd483a7e772f52cf72cf1a
 
 `kubectl create secret generic litellm-postgres \
  --from-literal=postgres-password="$PG_PASSWORD" \
  --from-literal=database-url="postgresql://litellm:${PG_PASSWORD}@litellm-postgres:5432/litellm" \
  -n inf-vllm`
  
Das Secret enthält zwei Schlüssel: postgres-password für den Postgres-Pod selbst, database-url als komplette Connection-String für LiteLLM. Beide Stellen müssen dasselbe Passwort verwenden, deshalb erzeugen wir sie in einem Aufwasch.

### LiteLLM-Proxy

Jetzt der eigentliche Proxy. LiteLLM ist als fertiges Image verfügbar (ghcr.io/berriai/litellm) und braucht zwei Konfigurationsteile: eine config.yaml (welche Modelle gibt es, wo liegen sie, welche Defaults gelten) und einen Master-Key (mit dem der Admin neue Keys erzeugt).
Erst den Master-Key als Secret. Auch der ist ein zufälliger String, gewählt nach LiteLLM-Konvention mit sk--Präfix:

`LITELLM_MASTER_KEY="sk-$(openssl rand -hex 24)"
echo "Master-Key: $LITELLM_MASTER_KEY"  # in den Admin-Passwort-Tresor!

kubectl create secret generic litellm-master-key \
  --from-literal=master-key="$LITELLM_MASTER_KEY" \
  -n inf-vllm`
  
Master-Key: sk-06b10bd529134c3d5ff4aa565cef19d363a6998e9d36a2f1

### Master Key aus Secrets ins Terminal übernehmen
 
`export LITELLM_MASTER_KEY=$(kubectl get secret litellm-master-key \
  -n inf-vllm -o jsonpath='{.data.master-key}' | base64 -d)

echo "Verifikation: $LITELLM_MASTER_KEY"

 # sollte 'sk-...' anzeigen`
 
## Deployment auf die ICC

`vllm-litellm-setup.md` enthält eine detailierte Beschreibung aller Deployment-Schritte.

`llm-service-fuer-studierende.md`eine Anleitung zur Nutzung des Deployments für Studierende.

Master-Key aus Secret auslesen und Terminalvariable setzen: 
`export LITELLM_MASTER_KEY=$(kubectl get secret litellm-master-key -n inf-vllm -o jsonpath='{.data.master-key}' | base64 -d)`

Port-Forward in anderem Terminal: `kubectl port-forward -n inf-vllm svc/litellm 4000:4000`

Mit `generate_keys_and_rbac.py` werden Schlüssel und RBAC gemäß `students.csv` angelegt. 
Key an Studierenden schicken aus `keys.csv`
RBAC aktualisieren: `kubectl apply -f rbac-students.yaml`

Mit `kubectl -n inf-vllm get rolebinding llm-service-users -o yaml` können wir sehen, welche Nutzer eingetragen sind.

Details zum dem Rolebinding erhalten wir mit `kubectl -n inf-vllm get rolebinding inf-vllm-members -o yaml`. 

### Pragmatischer Test mit echtem Studierenden-Account

1. Cluster-Zugang da?
`kubectl get ns inf-vllm`

2. Service sichtbar?
`kubectl get svc -n inf-vllm`

3. Port-forward + curl-Test
`kubectl port-forward -n inf-vllm svc/litellm 4000:4000`  
in zweitem Terminal:
`curl http://localhost:4000/v1/models -H "Authorization: Bearer sk-EinTestKey"`

### Eintragen von neuen Nutzern

`export LITELLM_MASTER_KEY=$(kubectl get secret litellm-master-key 
  -n inf-vllm -o jsonpath='{.data.master-key}' | base64 -d)`
  
`vi students.csv`

`python bulk_key_gen.py`

Keys über Teams verschicken