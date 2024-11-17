import requests
from bs4 import BeautifulSoup

# URL da página que queremos fazer o scraping
url = "https://www.starwars.com/databank/barash-vow"

# Faz uma requisição HTTP GET para a URL
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Analisa o conteúdo HTML da página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extrai a imagem
    img_tag = soup.find('img', {'class': 'thumb reserved-ratio'})
    if img_tag:
        imagem = img_tag.get('data-src') or img_tag.get('src')
        print("Imagem:", imagem)
    else:
        print("Imagem não encontrada.")

    # Extrai o nome
    nome_tag = soup.find('span', {'class': 'long-title'})
    if nome_tag:
        nome = nome_tag.get_text(strip=True)
        print("Nome:", nome)
    else:
        print("Nome não encontrado.")

    # Extrai a descrição
    desc_tag = soup.find('p', {'class': 'desc'})
    if desc_tag:
        descricao = desc_tag.get_text(strip=True)
        print("Descrição:", descricao)
    else:
        print("Descrição não encontrada.")
else:
    print("Não foi possível acessar a página.")
