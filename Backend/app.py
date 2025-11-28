from flask import Flask, jsonify
from flask_cors import CORS # Para evitar problemas de comunicação com o frontend
import requests
from bs4 import BeautifulSoup

# --- Configuração do Flask ---
app = Flask(__name__)
# Habilita o CORS para que o frontend possa acessar esta API
CORS(app) 

# --- Função de Scraping (Seu Código Original Adaptado) ---
def raspar_noticias():
    """Realiza o scraping na Globo.com e retorna os títulos como uma lista de dicionários."""
    url = 'https://www.globo.com/'
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Verifica se a requisição foi bem-sucedida
    except requests.exceptions.RequestException as e:
        # Em caso de erro, retorna uma mensagem de erro
        return {"erro": f"Falha na requisição: {e}"}, 500

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    titulos_raw = soup.find_all('h2', class_='post__title')
    
    # Criamos uma lista de dicionários para facilitar a conversão para JSON
    noticias = []
    for titulo in titulos_raw:
        noticias.append({
            "titulo": titulo.text.strip()
        })
        
    return noticias

# --- Endpoint da API ---
@app.route('/api/noticias', methods=['GET'])
def get_noticias():
    """Rota que executa o scraper e retorna os resultados em JSON."""
    resultados = raspar_noticias()
    
    # Se o resultado for um erro (dicionário com chave 'erro'), retorna o erro e o status 500
    if isinstance(resultados, dict) and 'erro' in resultados:
        return jsonify(resultados), 500
        
    # Retorna a lista de notícias como JSON
    return jsonify(resultados)

if __name__ == '__main__':
    # Roda a aplicação Flask na porta 5000
    print("🚀 Servidor Flask iniciado na porta 5000 (http://127.0.0.1:5000/api/noticias)")
    app.run(debug=True, port=5000)