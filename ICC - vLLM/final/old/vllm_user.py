import csv, requests, os

MASTER_KEY = os.environ["LITELLM_MASTER_KEY"]
BASE_URL = "http://localhost:4000"

with open("students.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        # Whitespace bereinigen
        email = row["email"].strip()
        matrikel = row["matrikel"].strip()
        kurs = row.get("kurs", "default").strip()

        r = requests.post(
            f"{BASE_URL}/key/generate",
            headers={"Authorization": f"Bearer {MASTER_KEY}"},
            json={
                "user_id": email,
                "key_alias": f"{kurs}-{matrikel}",
                "models": ["qwen2.5-7b"],
                "max_budget": 10.0,
                "budget_duration": "30d",
                "tpm_limit": 50000,
                "rpm_limit": 60,
                "duration": "120d",
            },
        )
        if r.status_code != 200:
            print(f"FEHLER bei {email}: {r.status_code} {r.text}")
            continue

        key = r.json()["key"]
        # CSV-Output für späteren Mail-Versand
        print(f"{email},{matrikel},{key}")

