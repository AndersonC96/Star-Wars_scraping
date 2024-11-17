import requests
from bs4 import BeautifulSoup
import json
import os

# Define o diretório onde os arquivos serão salvos
directory = './DB/Groups'

# Cria o diretório se ele não existir
if not os.path.exists(directory):
    os.makedirs(directory)

# Nome do arquivo que contém a lista de URLs
url_list_file = './DB/groups.txt'

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

                # Inicializa listas para categorias adicionais
                afiliacoes = []
                locais = []
                droid = []
                veiculos = []
                armas = []
                ferramentas = []
                recursos = []
                historia = ""

                # Encontrar todos os divs com a classe 'category'
                categories = soup.find_all('div', {'class': 'category'})
                for category in categories:
                    heading = category.find('div', {'class': 'heading'})
                    if heading:
                        heading_text = heading.get_text(strip=True)
                        ul = category.find('ul')
                        if ul:
                            li_tags = ul.find_all('li', {'class': 'data'})
                            for li in li_tags:
                                property_name = li.find('div', {'class': 'property-name'})
                                if heading_text == 'Affiliations' and property_name:
                                    afiliacoes.append(property_name.get_text(strip=True))
                                elif heading_text == 'Locations' and property_name:
                                    locais.append(property_name.get_text(strip=True))
                                elif heading_text.lower() == 'droid' and property_name:
                                    droid.append(property_name.get_text(strip=True))
                                elif heading_text == 'Vehicles' and property_name:
                                    veiculos.append(property_name.get_text(strip=True))
                                elif heading_text == 'Weapons' and property_name:
                                    armas.append(property_name.get_text(strip=True))
                                elif heading_text == 'Tool' and property_name:
                                    ferramentas.append(property_name.get_text(strip=True))
                                elif heading_text == 'Resource' and property_name:
                                    recursos.append(property_name.get_text(strip=True))

                # Extrai a história
                historia_div = soup.find('div', {'class': 'rich-text-output'})
                if historia_div:
                    paragraphs = historia_div.find_all('p')
                    for p in paragraphs:
                        historia += p.get_text(strip=True) + "\n\n"
                data['História'] = historia.strip() if historia else None

                # Adiciona as informações extraídas ao dicionário de dados
                data['Afiliações'] = afiliacoes
                data['Locais'] = locais
                data['Droid'] = droid
                data['Veículos'] = veiculos
                data['Armas'] = armas
                data['Ferramentas'] = ferramentas
                data['Recursos'] = recursos

                # Nome do arquivo baseado no nome do grupo
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
