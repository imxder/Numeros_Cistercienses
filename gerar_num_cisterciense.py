import cv2
import numpy as np

THICKNESS = 2
SIZE = (200, 200)
COR_PADRAO = (0, 0, 0)

class CistercienseDrawer:
    def __init__(self, cor=COR_PADRAO):
        self.cor = cor
        self.img = np.ones((*SIZE, 3), dtype=np.uint8) * 255
        self._desenhar_tronco()

    def _desenhar_tronco(self):
        cv2.line(self.img, (100, 25), (100, 170), (0, 0, 0), THICKNESS)

    def desenhar_unidade(self, valor):
        nome_func = f"unidade_{valor}"
        func = getattr(self, nome_func, None)
        if func:
            func()

    def desenhar(self, numero):
        if not (1 <= numero <= 9999):
            raise ValueError("Número deve estar entre 1 e 9999")

        unidades = numero % 10
        dezenas = (numero // 10) % 10
        centenas = (numero // 100) % 10
        milhares = numero // 1000

        for valor, mult in [(milhares, 1000), (centenas, 100), (dezenas, 10), (unidades, 1)]:
            if valor > 0:
                self.desenhar_unidade(valor * mult)

        return self.img


    def unidade_1(self): cv2.line(self.img, (100, 25), (143, 25), self.cor, THICKNESS)
    def unidade_2(self): cv2.line(self.img, (100, 65), (143, 65), self.cor, THICKNESS)
    def unidade_3(self): cv2.line(self.img, (101, 25), (135, 63), self.cor, THICKNESS, lineType=cv2.LINE_AA)
    def unidade_4(self): cv2.line(self.img, (101, 63), (135, 25), self.cor, THICKNESS, lineType=cv2.LINE_AA)
    def unidade_5(self): self.unidade_4(); cv2.line(self.img, (100, 25), (135, 25), self.cor, THICKNESS)
    def unidade_6(self): cv2.line(self.img, (143, 25), (143, 65), self.cor, THICKNESS)
    def unidade_7(self): self.unidade_1(); self.unidade_6()
    def unidade_8(self): self.unidade_2(); self.unidade_6()
    def unidade_9(self): self.unidade_1(); self.unidade_8()

    def unidade_10(self): cv2.line(self.img, (100, 25), (57, 25), self.cor, THICKNESS)
    def unidade_20(self): cv2.line(self.img, (100, 65), (57, 65), self.cor, THICKNESS)
    def unidade_30(self): cv2.line(self.img, (99, 25), (65, 63), self.cor, THICKNESS, lineType=cv2.LINE_AA)
    def unidade_40(self): cv2.line(self.img, (99, 63), (65, 25), self.cor, THICKNESS, lineType=cv2.LINE_AA)
    def unidade_50(self): self.unidade_40(); cv2.line(self.img, (100, 25), (65, 25), self.cor, THICKNESS)
    def unidade_60(self): cv2.line(self.img, (57, 25), (57, 65), self.cor, THICKNESS)
    def unidade_70(self): self.unidade_10(); self.unidade_60()
    def unidade_80(self): self.unidade_20(); self.unidade_60()
    def unidade_90(self): self.unidade_10(); self.unidade_80()

    def unidade_100(self): cv2.line(self.img, (100, 170), (143, 170), self.cor, THICKNESS)
    def unidade_200(self): cv2.line(self.img, (100, 130), (143, 130), self.cor, THICKNESS)
    def unidade_300(self): cv2.line(self.img, (101, 170), (135, 135), self.cor, THICKNESS, lineType=cv2.LINE_AA)
    def unidade_400(self): cv2.line(self.img, (101, 130), (135, 170), self.cor, THICKNESS, lineType=cv2.LINE_AA)
    def unidade_500(self): self.unidade_400(); cv2.line(self.img, (100, 170), (135, 170), self.cor, THICKNESS)
    def unidade_600(self): cv2.line(self.img, (143, 170), (143, 130), self.cor, THICKNESS)
    def unidade_700(self): self.unidade_100(); self.unidade_600()
    def unidade_800(self): self.unidade_200(); self.unidade_600()
    def unidade_900(self): self.unidade_100(); self.unidade_800()

    def unidade_1000(self): cv2.line(self.img, (100, 170), (57, 170), self.cor, THICKNESS)
    def unidade_2000(self): cv2.line(self.img, (100, 130), (57, 130), self.cor, THICKNESS)
    def unidade_3000(self): cv2.line(self.img, (99, 170), (65, 135), self.cor, THICKNESS, lineType=cv2.LINE_AA)
    def unidade_4000(self): cv2.line(self.img, (99, 130), (65, 170), self.cor, THICKNESS, lineType=cv2.LINE_AA)
    def unidade_5000(self): self.unidade_4000(); cv2.line(self.img, (100, 170), (65, 170), self.cor, THICKNESS)
    def unidade_6000(self): cv2.line(self.img, (57, 170), (57, 130), self.cor, THICKNESS)
    def unidade_7000(self): self.unidade_1000(); self.unidade_6000()
    def unidade_8000(self): self.unidade_2000(); self.unidade_6000()
    def unidade_9000(self): self.unidade_1000(); self.unidade_8000()


def desenhar_cisterciense(numero: int, cor=(0, 0, 0)):
    drawer = CistercienseDrawer(cor)
    return drawer.desenhar(numero)
