 Moin Thomas! 
 Ich habe deiner w-Kennung wbb822 ordentlich Ressourcen gegeben (32 CPU-Kerne, 64GB RAM und 250GB HDD) und in den YAML-Dateien schon überall deine w-Kennung als Namespace eingesetzt. D.h. im Prinzip sind die so direkt einsatzbereit. Mit kubectl apply -f <Datei> kannst du die anwenden, ich würde empfehlen, das nacheinander zu machen und immer erstmal sicherzustellen, dass der vorige Dienst läuft, bevor man weiter macht. Einfach mit kubectl get pods gucken, ob der auf "Running" steht, dann kann's weitergehen. 
 
 Um auf die UIs oder APIs zuzugreifen, brauchst du eine Portweiterleitung in das Cluster. Dazu muss man den Service-Namen, den Clusterport und einen freien, lokalen Port angeben. Bei n8n beispielsweise läuft der Service clusterintern auf Port 5678. Mit kubectl port-forward service/n8n 8080:5678 holst du dir den auf 8080 und kannst dann über http://localhost:8080 auf das Webinterface zugreifen.
 
 Phoenix hatte ich jetzt erstmal weggelassen. Und bei vLLM steht noch in dem Secret das AccessToken von meinem Account bei Huggingface drin. Falls du da selbst noch keinen Account hast, aber schon loslegen willst, kannst du auch ruhig mein Token nutzen, das ist ja bereits für das Repository freigeschaltet. 
 
 Und das war die einfache Anfrage an das vLLM:
 # vLLM-API wurde mittels kubectl port-forward auf Port 8000 gemappt
 curl http://localhost:8000/v1/chat/completions \
   -H "Content-Type: application/json" -d '{
     "messages": [
       {"role": "user", "content": "Hallo, wer bist du?"}
     ]
   }'
 ...für die "schicke" Ausgabe noch   | jq  an den Aufruf anhängen (wenn du das in deinem Terminal installiert hast). Der Server hostet auch seine eigene API-Dokumentation (OpenAPI Spec), die erreicht man unter http://localhost:8000/docs .
 
 Und hier noch ein paar Links, die ich nützlich fand:
 https://northflank.com/blog/vllm-vs-ollama-and-how-to-run-them
 https://github.com/vllm-project/vllm
 https://docs.vllm.ai/en/latest/deployment/k8s/
 https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct
 https://dev.to/aws-builders/vllm-on-x86-because-not-everyone-can-afford-a-gpu-cluster-15ep
 https://qdrant.tech/documentation/quickstart/
 https://qdrant.tech/documentation/guides/installation/
 vLLM vs Ollama: Key differences, performance, and how to run them | Blog — Northflank
 Explore vLLM vs Ollama: key features, performance, and use cases. Learn how to choose the right LLM runtime and deploy seamlessly with Northflank’s full-stack AI cloud platform.
 01-n8n-postgres.yaml
 02-n8n.yaml
 03-qdrant.yaml
 04-vllm.yaml
 