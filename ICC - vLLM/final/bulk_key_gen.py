import csv, requests, os

MASTER_KEY = os.environ["LITELLM_MASTER_KEY"]
BASE_URL = "https://llm.inf.haw-hamburg.de"

with open("students.csv") as f:
    for row in csv.DictReader(f):
        r = requests.post(
            f"{BASE_URL}/key/generate",
            headers={"Authorization": f"Bearer {MASTER_KEY}"},
            json={
                "user_id": row["email"],
                "key_alias": f"ss26-{row['matrikel']}",
                "models": ["qwen2.5-7b"],
                "max_budget": 10.0,
                "duration": "120d",
                "tpm_limit": 50000,
                "rpm_limit": 60,
            },
        )
        key = r.json()["key"]
        print(f"{row['email']},{key}")  # später per Mail versenden
