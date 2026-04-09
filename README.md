# Cotação do dólar

Script em Python que consulta a cotação do dólar na página pública da [Remessa Online](https://www.remessaonline.com.br/cotacao/cotacao-dolar) e mantém um histórico em JSON. Um novo registro só é gravado quando o valor exibido muda em relação ao último salvo.

Há também um **dashboard** no navegador (HTML em `dolar/templates/front.html`) servido por Flask, com gráfico e histórico a partir de `data/banco_cotacoes.json`.

## Requisitos

- Python 3.10 ou superior (recomendado)

## Instalação

Na raiz do repositório:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Como rodar

### 1. Atualizar a cotação (scraping)

Executa uma vez: busca o valor no site e, se mudou, acrescenta em `data/banco_cotacoes.json`.

```powershell
python -m dolar
```

### 2. Ver o site (dashboard)

Com o ambiente virtual ativado, na **raiz do repositório**:

```powershell
python -m flask --app dolar.web:app run --debug
```

Abra no navegador: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

A API usada pela página é [http://127.0.0.1:5000/api/dolar](http://127.0.0.1:5000/api/dolar) (JSON com `data_hora` e `valor` numérico).

Para aceitar conexões de outros dispositivos na rede local (opcional):

```powershell
python -m flask --app dolar.web:app run --host 0.0.0.0 --port 5000
```

## Dados

O histórico fica em `data/banco_cotacoes.json`. Cada item tem:

- `data_hora`: data e hora no formato `dd/mm/aaaa hh:mm:ss`
- `valor`: texto retornado pela página (por exemplo `5,11 reais`)

## Agendamento (opcional)

No Windows, use o **Agendador de Tarefas** para executar periodicamente o interpretador do `venv` com o argumento `-m dolar` e o diretório de trabalho na raiz deste repositório.

## Aviso

A coleta depende da estrutura HTML/CSS do site. Alterações na página podem exigir ajuste no código. Use de forma responsável e de acordo com os termos do serviço.
