from googlesearch import search
import requests
import re
from bs4 import BeautifulSoup
import time
import os

def extract_emails(text):
    """Extrai e-mails de um texto"""
    return set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text))

def get_emails_from_url(url):
    """Acessa um site e busca e-mails na primeira página"""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 403:
            print(f"⚠️ Acesso negado em {url} (403 Forbidden)")
            return set()

        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        emails = extract_emails(soup.get_text())
        return emails
    except requests.RequestException as e:
        print(f"❌ Erro ao acessar {url}: {e}")
        return set()

def save_email(email):
    """Salva um e-mail no arquivo emails.txt se ainda não estiver salvo"""
    file_path = "emails.txt"

    # Criar o arquivo se não existir
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            pass

    # Verificar se o e-mail já existe no arquivo
    with open(file_path, "r") as f:
        existing_emails = {line.strip() for line in f}

    if email not in existing_emails:
        with open(file_path, "a") as f:
            f.write(email + "\n")
        print(f"✅ E-mail salvo: {email}")

def search_and_scrape_emails(queries, num_results=50):
    """Executa a busca no Google para cada query e extrai e-mails"""
    for query in queries:
        print(f"\n🔎 Iniciando busca para: {query}")

        for url in search(query, num_results=num_results):
            if not url.startswith("http"):
                print(f"⚠️ URL inválida ignorada: {url}")
                continue  # Ignora URLs inválidas
            
            print(f"🔍 Acessando: {url}")
            emails = get_emails_from_url(url)

            if emails:
                print("\n📧 Novos e-mails encontrados:")
                for email in emails:
                    print(email)
                    save_email(email)

            time.sleep(4)  # Espera 4 segundos para evitar bloqueios
        
        print(f"\n⏳ Concluída a busca para '{query}'. Aguardando 60 segundos antes de iniciar a próxima busca...\n")
        time.sleep(60)  # Espera 1 minuto antes de começar a próxima busca

    print("\n✅ Todas as buscas foram concluídas. Programa finalizado.")

# Lista de palavras-chave para busca
queries = [
    "pousada em arraial d'ajuda ba",
    "pousada em trancoso ba",
    "pousada em caraiva ba",
    "pousada em porto seguro ba",
    "pousada em itacaré ba",
    "pousada em ilhéus ba",
    "pousada em morro de são paulo ba",
    "pousada em praia do forte ba",
    "pousada em imbassaí ba",
    "pousada em guarajuba ba",
    "pousada em imbassaí ba",
]

# Executar as buscas para todas as queries
search_and_scrape_emails(queries, num_results=50)
