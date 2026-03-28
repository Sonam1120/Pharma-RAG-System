import requests
import json

with open("questions.json") as f:
    questions = json.load(f)

url = "http://127.0.0.1:8000/query"

for category in questions:
    print(f"\n--- {category.upper()} ---")
    
    for q in questions[category]:
        response = requests.post(url, json={"query": q})
        print(f"\nQ: {q}")
        print("A:", response.json()["answer"])