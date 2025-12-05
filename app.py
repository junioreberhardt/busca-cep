from flask import Flask, request, jsonify, render_template
from data_handler import load_file, search_cep
from utils import format_cep

app = Flask(__name__)

DADOS_CEPS = load_file('logradouros.csv')

if not DADOS_CEPS:
    print("ERRO: Não foi possível carregar os dados de CEP. O aplicativo não funcionará corretamente.")


@app.route('/')
def index():
    """Renderiza a página inicial com o formulário de busca."""
    return render_template('index.html')


@app.route('/api/search', methods=['GET'])
def api_search():
    """
    Endpoint (API) para buscar CEPs.
    Espera um parâmetro 'rua' na URL. Ex: /api/search?rua=mario
    """
    term_search = request.args.get('rua', '').strip()

    if not term_search:
        # Retorna erro se o termo de busca estiver vazio
        return jsonify({'error': 'Termo de busca (rua) não fornecido.'}), 400

    # 1. Realiza a busca usando sua função existente
    results_found = search_cep(DADOS_CEPS, term_search)

    # 2. Formata a lista de resultados para JSON
    formatted_results = []
    for result in results_found:
        formatted_results.append({
            'cep_formatado': format_cep(result.get('CEP', 'CEP Inválido')),
            'logradouro': result.get('Logradouro', 'N/A'),
            'bairro': result.get('Bairro', 'N/A')
        })

    # 3. Retorna os resultados como JSON
    return jsonify(formatted_results)


if __name__ == '__main__':
    # Ativa o modo debug para desenvolvimento
    app.run(debug=True)
