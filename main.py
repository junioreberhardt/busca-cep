import utils as u
import data_handler as dh

data_ceps = dh.load_file('logradouros.csv')

if data_ceps:
    print(
        f"Total de {len(data_ceps)} CEPs de São Francisco do Sul carregados.")
    while True:
        # Pede entrada ao usuário
        input_user = input(
            "\nDigite o nome ou parte do nome da rua (ou 'sair' para encerrar): ").strip()

        if input_user.lower() == 'sair':
            print("Encerrando a busca. Até mais!")
            break

        if input_user:
            # 3. Realiza a busca
            result_found = dh.search_cep(
                data_ceps, input_user)

            # 4. Mostra os resultados
            print("\n--- Resultados Encontrados ---")
            if result_found:
                for result in result_found:
                    # Garante que o campo 'CEP' exista e formata a saída
                    cep_no_format = result.get(
                        'CEP', '').replace('-', '').strip()
                    if len(cep_no_format) == 8:
                        cep_format = f'{cep_no_format[:-3]}-{cep_no_format[-3:]}'
                    else:
                        cep_format = result.get('CEP', 'CEP Inválido')

                    print(
                        f"CEP: {cep_format} - {result.get('Logradouro', 'N/A')}, {result.get('Bairro', 'N/A')}")
            else:
                print(f"Nenhum CEP encontrado para '{input_user}'.")
        else:
            print("A busca não pode ser vazia. Digite algo para pesquisar.")
else:
    print("Não foi possível realizar a busca porque nenhum dado de CEP foi carregado.")
