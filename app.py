from flask import Flask, Response
import requests
import re
import os

app = Flask(__name__)

ICS_SOURCE_URL = "https://jlive.app/markets/cincinnati/ics-feed/feed.ics"

# Função para melhorar a formatação do ICS
def format_ics(ics_content):
    # Exemplo de formatação: Remover campos extras e melhorar a descrição
    ics_content = ics_content.replace("_", "")  # Exemplo de substituição
    ics_content = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", ics_content)  # Converter negrito em HTML
    return ics_content

# Rota para servir o ICS formatado
@app.route("/formatted-ics")
def serve_formatted_ics():
    response = requests.get(ICS_SOURCE_URL)
    if response.status_code == 200:
        ics_content = response.text
        formatted_ics = format_ics(ics_content)
        return Response(formatted_ics, mimetype="text/calendar")
    else:
        return "Erro ao acessar o ICS", 500

if __name__ == "__main__":
    # Configuração para o Flask escutar em 0.0.0.0 e usar a porta definida pela variável de ambiente
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
