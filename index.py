import requests
from bs4 import BeautifulSoup
import json
import os

# URL da página que queremos fazer o scraping
url = "https://www.starwars.com/databank/barash-vow"

# Faz uma requisição HTTP GET para a URL
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Analisa o conteúdo HTML da página
    soup = BeautifulSoup(response.content, 'html.parser')

    data = {}

    # Extrai a imagem
    img_tag = soup.find('img', {'class': 'thumb reserved-ratio'})
    if img_tag:
        imagem = img_tag.get('data-src') or img_tag.get('src')
        data['Imagem'] = imagem
    else:
        data['Imagem'] = None

    # Extrai o nome
    nome_tag = soup.find('span', {'class': 'long-title'})
    if nome_tag:
        nome = nome_tag.get_text(strip=True)
        data['Nome'] = nome
    else:
        data['Nome'] = None

    # Extrai a descrição
    desc_tag = soup.find('p', {'class': 'desc'})
    if desc_tag:
        descricao = desc_tag.get_text(strip=True)
        data['Descrição'] = descricao
    else:
        data['Descrição'] = None

    # Extrai as aparições
    appearances = []
    # Encontrar todos os divs com a classe 'category'
    categories = soup.find_all('div', {'class': 'category'})
    for category in categories:
        heading = category.find('div', {'class': 'heading'})
        if heading and heading.get_text(strip=True) == 'Appearances':
            # Encontrou a seção de aparições
            ul = category.find('ul')
            if ul:
                li_tags = ul.find_all('li', {'class': 'data'})
                for li in li_tags:
                    a_tag = li.find('a', {'class': 'section-color'})
                    if a_tag:
                        property_name = a_tag.find('div', {'class': 'property-name'})
                        if property_name:
                            appearance_name = property_name.get_text(strip=True)
                            appearances.append(appearance_name)
            break  # Já encontramos a seção de aparições, podemos sair do loop

    data['Aparições'] = appearances

    # Define o diretório onde o arquivo será salvo
    directory = './DB/The Acolyte'

    # Cria o diretório se ele não existir
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Nome do arquivo baseado no nome do personagem
    # Substitui espaços por underscores e remove caracteres não permitidos
    if data['Nome']:
        filename = ''.join(c for c in data['Nome'] if c.isalnum() or c in (' ', '_')).rstrip()
        filename = filename.replace(' ', '_')
        filepath = os.path.join(directory, f"{filename}.json")
    else:
        filepath = os.path.join(directory, "personagem.json")

    # Salva os dados em um arquivo JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Dados salvos em: {filepath}")

else:
    print("Não foi possível acessar a página.")
