import cv2
import numpy as np


def carregar_e_dividir_imagem(caminho_imagem):
    imagem = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)
    h, w = imagem.shape

    return {
        "unidades": imagem[0:h//2, w//2+2:],
        "dezenas": imagem[0:h//2, :w//2-1],
        "centenas": imagem[h//2:, w//2+2:],
        "milhares": imagem[h//2:, :w//2-1],
    }


def aplicar_filtro_linhas(imagem, direcao="horizontal"):
    kernel_shape = {
        "horizontal": (15, 1),
        "vertical": (1, 15)
    }.get(direcao)

    if kernel_shape is None:
        raise ValueError("Direção inválida. Use 'horizontal' ou 'vertical'.")

    suavizada = cv2.GaussianBlur(imagem, (5, 5), 0)
    _, binarizada = cv2.threshold(suavizada, 128, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_shape)
    return cv2.morphologyEx(binarizada, cv2.MORPH_OPEN, kernel)


def filtrar_diagonais(imagem, angulo="45", comprimento_min=11):
    kernel = _kernel_diagonal(angulo)

    binarizada = cv2.threshold(cv2.GaussianBlur(imagem, (5, 5), 0), 128, 255, cv2.THRESH_BINARY_INV)[1]
    destaque = cv2.morphologyEx(binarizada, cv2.MORPH_OPEN, kernel)

    kernel_suavizacao = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    destaque = cv2.dilate(destaque, kernel_suavizacao, iterations=1)
    destaque = cv2.erode(destaque, kernel_suavizacao, iterations=1)

    contornos, _ = cv2.findContours(destaque, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    resultado = np.zeros_like(imagem)

    for contorno in contornos:
        if cv2.arcLength(contorno, False) >= comprimento_min:
            cv2.drawContours(resultado, [contorno], -1, 255, cv2.FILLED)

    return resultado


def _kernel_diagonal(angulo):
    if angulo == '45':
        return np.eye(7, dtype=np.uint8)
    elif angulo == '135':
        return np.fliplr(np.eye(7, dtype=np.uint8))
    else:
        raise ValueError("Ângulo deve ser '45' ou '135'")


def contar_componentes(imagem):
    contornos, _ = cv2.findContours(imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return len(contornos)


def separar_linhas_horizontais(mascara, altura_total):
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    acima, abaixo = 0, 0

    for contorno in contornos:
        _, y, _, _ = cv2.boundingRect(contorno)
        if y < altura_total // 2:
            acima += 1
        else:
            abaixo += 1

    return acima, abaixo


def avaliar_combinacao_linhas(h_sup, h_inf, vert, d45, d135, tipo):
    configuracoes = {
        (1, 0, 0, 0, 0): 1,
        (0, 1, 0, 0, 0): 2,
        (0, 0, 0, 1, 0): 3,
        (0, 0, 0, 0, 1): 4,
        (1, 0, 0, 0, 1): 5,
        (0, 0, 1, 0, 0): 6,
        (1, 0, 1, 0, 0): 7,
        (0, 1, 1, 0, 0): 8,
        (1, 1, 1, 0, 0): 9,
    }

    pesos = {
        "unidades": 1,
        "dezenas": 10,
        "centenas": 100,
        "milhares": 1000,
    }

    # Ajustes de rotação
    if tipo in ["dezenas", "centenas"]:
        d45, d135 = d135, d45
    if tipo in ["centenas", "milhares"]:
        h_sup, h_inf = h_inf, h_sup

    valor = configuracoes.get((h_sup, h_inf, vert, d45, d135), 0)
    return valor * pesos[tipo]


def processar_quadrantes(caminho_imagem):
    partes = carregar_e_dividir_imagem(caminho_imagem)
    resultado_final = {}

    ordem = ["milhares", "centenas", "dezenas", "unidades"]

    for tipo in ordem:
        quadro = partes[tipo]
        altura, _ = quadro.shape

        linhas_h = aplicar_filtro_linhas(quadro, "horizontal")
        h_sup, h_inf = separar_linhas_horizontais(linhas_h, altura)

        linhas_v = aplicar_filtro_linhas(quadro, "vertical")
        v_count = contar_componentes(linhas_v)

        diag_45 = filtrar_diagonais(quadro, "45", comprimento_min=11)
        d45_count = contar_componentes(diag_45)

        diag_135 = filtrar_diagonais(quadro, "135", comprimento_min=15)
        d135_count = contar_componentes(diag_135)

        resultado_final[tipo] = avaliar_combinacao_linhas(h_sup, h_inf, v_count, d45_count, d135_count, tipo)

    return resultado_final
