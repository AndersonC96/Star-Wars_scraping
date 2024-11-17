import requests
from bs4 import BeautifulSoup
import json
import os

# URL da página que queremos fazer o scraping
url = "https://www.starwars.com/databank/cabuck"

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

    # Inicializa as listas para aparições, dimensões, espécie e afiliações
    appearances = []
    dimensions = []
    species = []
    afiliacoes = []

    # Encontrar todos os divs com a classe 'category'
    categories = soup.find_all('div', {'class': 'category'})
    for category in categories:
        heading = category.find('div', {'class': 'heading'})
        if heading:
            heading_text = heading.get_text(strip=True)
            if heading_text == 'Appearances':
                # Extrai as aparições
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
                        else:
                            property_name = li.find('div', {'class': 'property-name'})
                            if property_name:
                                appearance_name = property_name.get_text(strip=True)
                                appearances.append(appearance_name)
            elif heading_text == 'Dimensions':
                # Extrai as dimensões
                ul = category.find('ul')
                if ul:
                    li_tags = ul.find_all('li', {'class': 'data'})
                    for li in li_tags:
                        property_name = li.find('div', {'class': 'property-name'})
                        if property_name:
                            dimension = property_name.get_text(strip=True)
                            dimensions.append(dimension)
            elif heading_text.lower() == 'species':
                # Extrai a espécie
                ul = category.find('ul')
                if ul:
                    li_tags = ul.find_all('li', {'class': 'data'})
                    for li in li_tags:
                        property_name = li.find('div', {'class': 'property-name'})
                        if property_name:
                            specie = property_name.get_text(strip=True)
                            species.append(specie)
            elif heading_text == 'Affiliations':
                # Extrai as afiliações
                ul = category.find('ul')
                if ul:
                    li_tags = ul.find_all('li', {'class': 'data'})
                    for li in li_tags:
                        a_tag = li.find('a', {'class': 'section-color'})
                        if a_tag:
                            property_name = a_tag.find('div', {'class': 'property-name'})
                            if property_name:
                                affiliation_name = property_name.get_text(strip=True)
                                afiliacoes.append(affiliation_name)
                        else:
                            property_name = li.find('div', {'class': 'property-name'})
                            if property_name:
                                affiliation_name = property_name.get_text(strip=True)
                                afiliacoes.append(affiliation_name)

    # Adiciona as informações extraídas ao dicionário de dados
    data['Aparições'] = appearances
    data['Dimensões'] = dimensions
    data['Espécie'] = species
    data['Afiliações'] = afiliacoes

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
