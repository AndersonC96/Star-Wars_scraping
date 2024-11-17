import requests
from bs4 import BeautifulSoup
import json
import os

# Define o diretório onde os arquivos serão salvos
directory = './DB/Characters'

# Cria o diretório se ele não existir
if not os.path.exists(directory):
    os.makedirs(directory)

# Nome do arquivo que contém a lista de URLs
url_list_file = './DB/characters.txt'

# Verifica se o arquivo de URLs existe
if not os.path.isfile(url_list_file):
    print(f"O arquivo {url_list_file} não foi encontrado.")
else:
    # Abre o arquivo e lê todas as URLs
    with open(url_list_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    # Itera sobre cada URL
    for url in urls:
        print(f"Processando URL: {url}")

        try:
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

                # Inicializa as listas para as categorias
                appearances = []
                dimensions = []
                species = []
                afiliacoes = []
                locais = []
                armas = []
                genero = []
                veiculos = []
                frases = []
                historia_text = ""

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
                                            appearances.append(property_name.get_text(strip=True))
                                    else:
                                        property_name = li.find('div', {'class': 'property-name'})
                                        if property_name:
                                            appearances.append(property_name.get_text(strip=True))
                        elif heading_text == 'Dimensions':
                            # Extrai as dimensões
                            ul = category.find('ul')
                            if ul:
                                li_tags = ul.find_all('li', {'class': 'data'})
                                for li in li_tags:
                                    property_name = li.find('div', {'class': 'property-name'})
                                    if property_name:
                                        dimensions.append(property_name.get_text(strip=True))
                        elif heading_text.lower() == 'species':
                            # Extrai a espécie
                            ul = category.find('ul')
                            if ul:
                                li_tags = ul.find_all('li', {'class': 'data'})
                                for li in li_tags:
                                    property_name = li.find('div', {'class': 'property-name'})
                                    if property_name:
                                        species.append(property_name.get_text(strip=True))
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
                                            afiliacoes.append(property_name.get_text(strip=True))
                                    else:
                                        property_name = li.find('div', {'class': 'property-name'})
                                        if property_name:
                                            afiliacoes.append(property_name.get_text(strip=True))
                        elif heading_text == 'Locations':
                            # Extrai os locais
                            ul = category.find('ul')
                            if ul:
                                li_tags = ul.find_all('li', {'class': 'data'})
                                for li in li_tags:
                                    a_tag = li.find('a', {'class': 'section-color'})
                                    if a_tag:
                                        property_name = a_tag.find('div', {'class': 'property-name'})
                                        if property_name:
                                            locais.append(property_name.get_text(strip=True))
                                    else:
                                        property_name = li.find('div', {'class': 'property-name'})
                                        if property_name:
                                            locais.append(property_name.get_text(strip=True))
                        elif heading_text == 'Weapons':
                            # Extrai as armas
                            ul = category.find('ul')
                            if ul:
                                li_tags = ul.find_all('li', {'class': 'data'})
                                for li in li_tags:
                                    a_tag = li.find('a', {'class': 'section-color'})
                                    if a_tag:
                                        property_name = a_tag.find('div', {'class': 'property-name'})
                                        if property_name:
                                            armas.append(property_name.get_text(strip=True))
                                    else:
                                        property_name = li.find('div', {'class': 'property-name'})
                                        if property_name:
                                            armas.append(property_name.get_text(strip=True))
                        elif heading_text == 'Gender':
                            # Extrai o gênero
                            ul = category.find('ul')
                            if ul:
                                li_tags = ul.find_all('li', {'class': 'data'})
                                for li in li_tags:
                                    property_name = li.find('div', {'class': 'property-name'})
                                    if property_name:
                                        genero.append(property_name.get_text(strip=True))
                        elif heading_text == 'Vehicles':
                            # Extrai os veículos
                            ul = category.find('ul')
                            if ul:
                                li_tags = ul.find_all('li', {'class': 'data'})
                                for li in li_tags:
                                    a_tag = li.find('a', {'class': 'section-color'})
                                    if a_tag:
                                        property_name = a_tag.find('div', {'class': 'property-name'})
                                        if property_name:
                                            veiculos.append(property_name.get_text(strip=True))
                                    else:
                                        property_name = li.find('div', {'class': 'property-name'})
                                        if property_name:
                                            veiculos.append(property_name.get_text(strip=True))

                # Extrai a história
                historia_divs = soup.find_all('div', {'class': 'rich-text-output'})
                historia_text = ''
                for historia_div in historia_divs:
                    paragraphs = historia_div.find_all('p')
                    for p in paragraphs:
                        historia_text += p.get_text(strip=True) + '\n\n'
                data['História'] = historia_text.strip() if historia_text else None

                # Extrai as frases (Quotes)
                frases = []
                # Procura pelas seções que contêm as frases
                bound_sections = soup.find_all('div', {'class': 'bound'})
                for bound in bound_sections:
                    # Verifica se o bound contém a seção de Quotes
                    module_header = bound.find('div', {'class': 'module_header'})
                    if module_header:
                        title_div = module_header.find('div', {'class': 'title'})
                        if title_div and 'Quotes' in title_div.get_text(strip=True):
                            # Encontrar o container das frases dentro deste bound
                            blocks_bound = bound.find('div', {'class': 'blocks-bound'})
                            if blocks_bound:
                                quote_items = blocks_bound.find_all('li', {'class': 'building-block-config'})
                                for item in quote_items:
                                    quote_text = item.find('p', {'class': 'desc'})
                                    if quote_text:
                                        frases.append(quote_text.get_text(strip=True))
                            break  # Já encontramos a seção de frases

                # Adiciona as informações extraídas ao dicionário de dados
                data['Aparições'] = appearances
                data['Dimensões'] = dimensions
                data['Espécie'] = species
                data['Afiliações'] = afiliacoes
                data['Locais'] = locais
                data['Armas'] = armas
                data['Gênero'] = genero
                data['Veículos'] = veiculos
                data['Frases'] = frases

                # Nome do arquivo baseado no nome do personagem
                # Substitui espaços por underscores e remove caracteres não permitidos
                if data['Nome']:
                    filename = ''.join(c for c in data['Nome'] if c.isalnum() or c in (' ', '_')).rstrip()
                    filename = filename.replace(' ', '_')
                    filepath = os.path.join(directory, f"{filename}.json")
                else:
                    # Se não houver nome, usa um nome padrão baseado na URL
                    filename = url.strip('/').split('/')[-1]
                    filename = ''.join(c for c in filename if c.isalnum() or c in (' ', '_')).rstrip()
                    filepath = os.path.join(directory, f"{filename}.json")

                # Salva os dados em um arquivo JSON
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                print(f"Dados salvos em: {filepath}\n")

            else:
                print(f"Não foi possível acessar a página: {url}\n")

        except Exception as e:
            print(f"Ocorreu um erro ao processar a URL {url}: {e}\n")
