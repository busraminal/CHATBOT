import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def load_varliklar(json_path="varliklar.json"):
    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)

def build_prompt(user_question, varlik_list):
    data_text = json.dumps(varlik_list, indent=2, ensure_ascii=False)
    prompt = f"""
Sen bir varlık yönetim asistanısın.
Aşağıda sisteme kayıtlı varlık bilgileri yer almakta:

{data_text}

Kullanıcı sana şu soruyu soruyor:
\"{user_question}\"

Yukarıdaki veriye göre net, doğru ve kısa bir şekilde Türkçe yanıt ver.
"""
    return prompt

def ask_ollama(prompt, model="mistral"):
    response = requests.post(OLLAMA_URL, json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    if response.ok:
        return response.json()["response"]
    else:
        return "❌ Model çalışmadı."

if __name__ == "__main__":
    question = input("💬 Kullanıcı sorusu: ")
    varliklar = load_varliklar("varliklar.json")
    prompt = build_prompt(question, varliklar)
    yanit = ask_ollama(prompt)
    print("\n🧠 Asistanın Cevabı:\n", yanit)
