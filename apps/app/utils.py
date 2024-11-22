import requests

def buscar_imagem_produto(produto_nome):
    client_id = 'SUA_UNSPLASH_API_KEY'
    url = f"https://api.unsplash.com/search/photos?query={produto_nome}&client_id={client_id}&per_page=1"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['urls']['regular']  # URL da imagem
    return None