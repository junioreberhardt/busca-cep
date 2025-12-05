import csv
import utils as u


def load_file(file):
    data = []
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = csv.DictReader(f)

            for line in content:
                city_clear = u.normal_text(line.get('Cidade', ''))
                if 'sao francisco do sul' in city_clear:
                    data.append(line)
        return data
    except FileNotFoundError:
        print(f'Erro: Arquivo {file} não encontrado.')
        return []
    except Exception as e:
        print(f'Ocorreu um erro ao carregar o arquivo: {e}')
        return []


def search_cep(data, term_search):
    term_default = u.normal_text(term_search)
    result = []

    for item in data:
        street_default = u.normal_text(item.get('Logradouro', ''))

        if term_default in street_default:
            result.append(item)

    return result
