from flask import Flask, render_template, request, send_from_directory
import os
import cv2
import numpy as np
from gerar_num_cisterciense import desenhar_cisterciense
from ler_img import processar_quadrantes

app = Flask(__name__)
OUTPUT_FOLDER = 'static/output'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    total_valor = None
    coluna1 = []
    coluna2 = []
    imagem_original_nome = None

    if request.method == "POST":
        if "numero" in request.form:
            try:
                numero = int(request.form["numero"])
                img = desenhar_cisterciense(numero)
                caminho = os.path.join(OUTPUT_FOLDER, f"{numero}.png")
                cv2.imwrite(caminho, img)
                resultado = f"{numero}.png"
            except ValueError:
                resultado = "Erro: Digite um número válido entre 1 e 9999."

        elif "imagem" in request.files:
            imagem = request.files["imagem"]
            if imagem.filename:
                imagem_original_nome = imagem.filename
                caminho_img = os.path.join(OUTPUT_FOLDER, imagem_original_nome)
                imagem.save(caminho_img)

                valores = processar_quadrantes(caminho_img)
                total_valor = 0

                for quadrante, valor in valores.items():
                    if valor > 0:
                        img = desenhar_cisterciense(valor, (0, 0, 255))
                        nome_arquivo = f"{quadrante}_{valor}.png"
                        caminho_valor = os.path.join(OUTPUT_FOLDER, nome_arquivo)
                        cv2.imwrite(caminho_valor, img)

                        if quadrante in ["dezenas", "milhares"]:
                            coluna1.append((nome_arquivo, quadrante, valor))
                        elif quadrante in ["unidades", "centenas"]:
                            coluna2.append((nome_arquivo, quadrante, valor))

                        total_valor += valor

                coluna1.sort(key=lambda x: ["dezenas", "milhares"].index(x[1]))
                coluna2.sort(key=lambda x: ["unidades", "centenas"].index(x[1]))

    return render_template("index.html",
                           imagem_gerada=resultado,
                           imagem_original=imagem_original_nome,
                           coluna1=coluna1,
                           coluna2=coluna2,
                           total_valor=total_valor)

@app.route('/static/output/<filename>')
def output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
