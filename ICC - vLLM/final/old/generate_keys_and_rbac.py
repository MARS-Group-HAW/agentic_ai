"""
Erzeugt für jede Studierende aus students.csv:
1) einen LiteLLM-API-Key (per /key/generate)
2) einen Eintrag im RBAC-RoleBinding-Manifest

Ausgabe:
- keys.csv mit Spalten email,matrikel,ad_user,api_key (für Mail-Versand)
- rbac-students.yaml mit allen Studierenden als Subjects

Voraussetzungen:
- Umgebungsvariable LITELLM_MASTER_KEY ist gesetzt
- LiteLLM ist via port-forward auf localhost:4000 erreichbar
- students.csv liegt im aktuellen Verzeichnis mit den Spalten
  email, matrikel, ad_user
"""

import csv
import os
import sys
import requests

MASTER_KEY = os.environ["LITELLM_MASTER_KEY"]
BASE_URL = "http://localhost:4000"
KURS = "ss26-agentic-ai"

# RBAC-Header ausgeben
RBAC_HEADER = """apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: llm-service-user
  namespace: inf-vllm
rules:
  - apiGroups: [""]
    resources: ["services"]
    verbs: ["get", "list"]
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list"]
  - apiGroups: [""]
    resources: ["pods/log"]
    verbs: ["get"]
  - apiGroups: [""]
    resources: ["pods/portforward"]
    verbs: ["create", "get"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: llm-service-users
  namespace: inf-vllm
subjects:
"""

RBAC_FOOTER = """roleRef:
  kind: Role
  name: llm-service-user
  apiGroup: rbac.authorization.k8s.io
"""


def main():
    rbac_subjects = []
    keys_rows = []

    with open("students.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            email = row["email"].strip()
            matrikel = row["matrikel"].strip()
            ad_user = row["ad_user"].strip()

            # 1) Key bei LiteLLM anfordern
            r = requests.post(
                f"{BASE_URL}/key/generate",
                headers={"Authorization": f"Bearer {MASTER_KEY}"},
                json={
                    "user_id": email,
                    "key_alias": f"{KURS}-{matrikel}",
                    "models": ["qwen2.5-7b"],
                    "max_budget": 10.0,
                    "budget_duration": "30d",
                    "tpm_limit": 50000,
                    "rpm_limit": 60,
                    "duration": "120d",
                },
                timeout=10,
            )
            if r.status_code != 200:
                print(f"FEHLER bei {email}: {r.status_code} {r.text}",
                      file=sys.stderr)
                continue
            api_key = r.json()["key"]

            # 2) Datensätze für die beiden Output-Dateien sammeln
            keys_rows.append({
                "email": email,
                "matrikel": matrikel,
                "ad_user": ad_user,
                "api_key": api_key,
            })
            rbac_subjects.append(ad_user)
            print(f"OK: {email} ({ad_user})", file=sys.stderr)

    # keys.csv schreiben
    with open("keys.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "matrikel", "ad_user", "api_key"])
        writer.writeheader()
        writer.writerows(keys_rows)
    print(f"\n{len(keys_rows)} Keys -> keys.csv", file=sys.stderr)

    # rbac-students.yaml schreiben
    with open("rbac-students.yaml", "w", encoding="utf-8") as f:
        f.write(RBAC_HEADER)
        for user in rbac_subjects:
            f.write(f"  - kind: User\n")
            f.write(f"    name: {user}\n")
            f.write(f"    apiGroup: rbac.authorization.k8s.io\n")
        f.write(RBAC_FOOTER)
    print(f"{len(rbac_subjects)} Subjects -> rbac-students.yaml", file=sys.stderr)


if __name__ == "__main__":
    main()
