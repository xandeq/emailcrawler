import requests
from bs4 import BeautifulSoup
import re
import time
import os
from datetime import datetime
from urllib.parse import urlparse
from googlesearch import search  # 🔹 Importação correta do Google Search

# Conjunto de URLs já visitadas para evitar loops infinitos
visited_urls = set()

def extract_emails(text, soup):
    """Extrai e-mails do texto da página e de links mailto:"""
    emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text))

    # Captura e-mails dentro de mailto:
    mailto_links = soup.select("a[href^=mailto]")
    for link in mailto_links:
        email = link.get("href").replace("mailto:", "").split("?")[0]  # Remove "mailto:" e parâmetros extras
        if email:
            emails.add(email)

    return emails

def get_emails_from_url(url):
    """Acessa um site e busca e-mails na primeira página, evitando loops"""
    if url in visited_urls:
        print(f"🔄 Já visitado, ignorando: {url}")
        return set()

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 403:
            print(f"⚠️ Acesso negado em {url} (403 Forbidden)")
            return set()

        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Marca a URL como visitada para evitar loops
        visited_urls.add(url)

        # Extrai e-mails da página principal
        emails = extract_emails(soup.get_text(), soup)

        return emails
    except requests.RequestException as e:
        print(f"❌ Erro ao acessar {url}: {e}")
        return set()

def save_email(email):
    """Salva um e-mail no arquivo emails.txt se ainda não estiver salvo"""
    file_path = "emails.txt"

    # Criar o arquivo se não existir
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            pass

    # Verificar se o e-mail já existe no arquivo
    with open(file_path, "r", encoding="utf-8") as f:
        existing_emails = {line.strip() for line in f}

    if email not in existing_emails:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(email + "\n")
        print(f"✅ E-mail salvo: {email}")

def log_search_start(query):
    """Registra o início de uma busca no arquivo emails.txt"""
    file_path = "emails.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"\n🔎 Iniciando busca: {query} - {timestamp}\n"

    # 🔹 Escreve o log no arquivo usando UTF-8 para evitar erros de encoding
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(log_entry)

def search_and_scrape_emails(queries, num_results=50):
    """Executa a busca no Google para cada query e extrai e-mails"""
    for query in queries:
        log_search_start(query)  # 🔹 Adiciona a entrada no emails.txt
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
    "pousada em Algodoal pa",
    "pousada em Alter do Chão pa",
    "pousada em Atins ma",
    "pousada em Barreirinhas ma",
    "pousada em Santo Amaro do Maranhão ma",
    "pousada em Jericoacoara ce",
    "pousada em Flecheiras ce",
    "pousada em Icaraí de Amontada ce",
    "pousada em Canoa Quebrada ce",
    "pousada em São Miguel do Gostoso rn",
    "pousada em Pipa rn",
    "pousada em Baía Formosa rn",
    "pousada em São Miguel dos Milagres al",
    "pousada em Porto de Pedras al",
    "pousada em Maragogi al",
    "pousada em Tamandaré pe",
    "pousada em Praia dos Carneiros pe",
    "pousada em Algodões ba",
    "pousada em Prado ba",
    "pousada em Ilha do Mosqueiro pa",
    "pousada em Soure pa",
    "pousada em Salvaterra pa"
]

# Executar as buscas para todas as queries
search_and_scrape_emails(queries, num_results=50)
