from dolar.cotacao import obter_cotacao, salvar_no_json


def main():
    valor_atual = obter_cotacao()
    if valor_atual:
        salvar_no_json(valor_atual)
    else:
        print("Não foi possível encontrar o valor.")


if __name__ == "__main__":
    main()
