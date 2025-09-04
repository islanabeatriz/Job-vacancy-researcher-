import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
params = {
    "keywords": "Testador de QA",
    "location": "Brazil",
    "start": 0
}

all_jobs = []

# Vamos buscar até 100 vagas (4 páginas = 0,25,50,75)
for start in range(0, 100, 25):
    params["start"] = start
    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"⚠️ Erro na página {start}: {response.status_code}")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("li")

    if not jobs:  # Se não houver mais vagas, parar o loop
        print("🚫 Não há mais vagas disponíveis.")
        break

    for job in jobs:
        try:
            title = job.find("h3", class_="base-search-card__title").text.strip()
            company = job.find("h4", class_="base-search-card__subtitle").text.strip()
            link = job.find("a", class_="base-card__full-link")["href"]

            all_jobs.append({
                "Título": title,
                "Empresa": company,
                "Link": link
            })
        except Exception:
            pass

# Salvar em CSV
df = pd.DataFrame(all_jobs)
df.to_csv("linkedin_jobs.csv", index=False, encoding="utf-8-sig")

print(f" Coletadas {len(all_jobs)} vagas e salvas em linkedin_jobs.csv")
