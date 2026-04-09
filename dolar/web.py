import re

from flask import Flask, jsonify, render_template

from dolar.cotacao import carregar_historico, obter_cotacao, salvar_no_json


def valor_br_para_numero(texto):
    if texto is None:
        return None
    s = str(texto).replace("\u00a0", " ").strip()
    if not s:
        return None
    compact = re.sub(r"\s+", "", s)
    # Formato 1.234,56 (milhar com ponto, decimal com vírgula)
    m = re.search(r"(\d{1,3}(?:\.\d{3})+),(\d{2})\b", compact)
    if m:
        inteiro = m.group(1).replace(".", "")
        return float(f"{inteiro}.{m.group(2)}")
    m = re.search(r"(\d+)[,.](\d+)", compact)
    if m:
        return float(f"{m.group(1)}.{m.group(2)}")
    m = re.search(r"(\d+)", s)
    return float(m.group(1)) if m else None


def create_app():
    app = Flask(__name__, template_folder="templates")

    @app.route("/")
    def index():
        return render_template("front.html")

    @app.route("/api/dolar")
    def api_dolar():
        dados = carregar_historico()
        if not dados:
            valor = obter_cotacao()
            if valor:
                salvar_no_json(valor)
                dados = carregar_historico()
        out = []
        for row in dados:
            if not isinstance(row, dict):
                continue
            v = row.get("valor")
            if v is None and "Valor" in row:
                v = row.get("Valor")
            n = valor_br_para_numero(v)
            if n is None:
                continue
            dh = row.get("data_hora") or row.get("Data_Hora")
            if not dh:
                continue
            out.append({"data_hora": dh, "valor": n})
        return jsonify(out)

    return app


app = create_app()
