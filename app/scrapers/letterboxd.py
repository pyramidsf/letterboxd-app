import httpx
from bs4 import BeautifulSoup
import asyncio
import random # Novo: para gerar um tempo de espera aleatório
from xml.etree import ElementTree

# Cabeçalhos mais completos para simular perfeitamente um navegador real no macOS
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://letterboxd.com/"
}

RSS_NAMESPACE = {"letterboxd": "https://letterboxd.com"}


async def scrape_letterboxd_rss(username: str):
    """Coleta os filmes recentes de um perfil público pelo RSS do Letterboxd."""
    url = f"https://letterboxd.com/{username}/rss/"

    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=30.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            if error.response.status_code == 404:
                raise ValueError(f"Usuário do Letterboxd não encontrado: {username}") from error
            raise RuntimeError(
                f"Letterboxd recusou o feed RSS (HTTP {error.response.status_code})"
            ) from error
        except httpx.RequestError as error:
            raise RuntimeError("Não foi possível conectar ao Letterboxd") from error

    root = ElementTree.fromstring(response.content)
    movies_data = []

    for item in root.findall("./channel/item"):
        rating = item.findtext("letterboxd:memberRating", default="", namespaces=RSS_NAMESPACE)
        year = item.findtext("letterboxd:filmYear", default="", namespaces=RSS_NAMESPACE)
        movies_data.append({
            "title": item.findtext("letterboxd:filmTitle", default="Sem título", namespaces=RSS_NAMESPACE),
            "year": int(year) if year.isdigit() else None,
            "user_rating": float(rating) if rating else None,
            "watch_date": item.findtext("letterboxd:watchedDate", namespaces=RSS_NAMESPACE),
        })

    return movies_data

async def scrape_letterboxd_diary(username: str):
    """
    Realiza o scraping do diário de um usuário no Letterboxd.
    Retorna uma lista de dicionários com os filmes assistidos.
    """
    base_url = f"https://letterboxd.com/{username}/films/diary/"
    movies_data = []
    
    # Configuramos um timeout maior (30 segundos)
    timeout = httpx.Timeout(30.0)
    
    # Passamos o timeout para o AsyncClient
    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=timeout) as client:
        page_number = 1
        
        while True:
            url = f"{base_url}page/{page_number}/"
            print(f"Lendo página {page_number}...")
            
            try:
                response = await client.get(url)
            except httpx.RequestError as e:
                print(f"Erro ao conectar na página {page_number}: {e}")
                break
            
            if response.status_code == 403:
                ray_id = response.headers.get("cf-ray", "indisponível")
                print(
                    "O Letterboxd bloqueou a paginação (HTTP 403). "
                    f"cf-ray: {ray_id}. Filmes coletados até aqui: {len(movies_data)}."
                )
                break

            if response.status_code != 200:
                print(f"Página não encontrada ou acesso negado. Status: {response.status_code}")
                break
                
            soup = BeautifulSoup(response.text, "html.parser")
            diary_rows = soup.find_all("tr", class_="diary-entry-row")
            
            if not diary_rows:
                break
                
            for row in diary_rows:
                # 1. Extraindo o Título de forma defensiva
                headline = row.find("h3")
                if headline and headline.find("a"):
                    title = headline.find("a").text.strip()
                else:
                    # Fallback: tentar pegar o atributo 'alt' da imagem do poster, se existir
                    img = row.find("img")
                    title = img.get("alt", "Sem título") if img else "Sem título"
                
                # 2. Extraindo o Ano
                year_td = row.find("td", class_="td-released")
                year_span = year_td.find("span") if year_td else None
                year = int(year_span.text.strip()) if year_span and year_span.text.strip().isdigit() else None
                
                # 3. Extraindo a Nota do Usuário
                rating_tag = row.find("span", class_="rating")
                rating_text = rating_tag.text.strip() if rating_tag else ""
                user_rating = converter_estrelas_para_nota(rating_text)
                
                movies_data.append({
                    "title": title,
                    "year": year,
                    "user_rating": user_rating,
                    "watch_date": None
                })

            page_number += 1

            tempo_espera = random.uniform(2.0, 4.5)
            print(f"Pausa de {tempo_espera:.1f}s simulando um humano...")
            await asyncio.sleep(tempo_espera)

    return movies_data

def converter_estrelas_para_nota(estrelas_str: str) -> float:

    # converte as estrelas do letterboxd para um número.
    if not estrelas_str:
        return None
        
    nota = 0.0
    nota += estrelas_str.count('★')
    if '½' in estrelas_str:
        nota += 0.5
        
    return nota

# Bloco pra testar o arquivo isoladamente
if __name__ == "__main__":
    # Substitua pelo username de alguém (o seu, por exemplo)
    teste_username = "userteste" 
    filmes = asyncio.run(scrape_letterboxd_diary(teste_username))
    print(f"\nTotal de filmes encontrados: {len(filmes)}")
    print("Primeiros 3 filmes:", filmes[:3])