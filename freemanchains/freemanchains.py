import cv2
import numpy as np
from matplotlib import pyplot as plt

def conectividad(imagen_path, conectividad=8, umbral_min=80, umbral_max=130, iteraciones_erosion=20, rotate = False):
    if rotate == False:
        img = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    _, bin = cv2.threshold(img, umbral_min, umbral_max, cv2.THRESH_BINARY)
    kernel = np.ones((3, 3), np.uint8)
    morfo = cv2.erode(bin, kernel, iterations=iteraciones_erosion)

    stpunto = None
    for i in range(bin.shape[0]):
        for j in range(bin.shape[1]):
            if morfo[i, j] > 0:
                stpunto = (i, j)
                break
        if stpunto is not None:
            break

    if conectividad == 4:
        move = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        direc = [0, 1, 2, 3]
    else:
        move = [
            (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)
        ]
        direc = [0, 1, 2, 7, 3, 6, 5, 4]
        actualp = stpunto
    guardar = []
    direccionactual = 0
    while True:
        for i in range(len(direc)):
            newdirec = (direccionactual + i) % len(direc)
            newp = (actualp[0] + move[newdirec][0], actualp[1] + move[newdirec][1])
            if 0 <= newp[0] < morfo.shape[0] and 0 <= newp[1] < morfo.shape[1] and morfo[newp[0], newp[1]] > 0:
                guardar.append(newdirec)
                actualp = newp
                direccionactual = newdirec
                break

        if actualp == stpunto:
            break

    fig, ax = plt.subplots()
    ax.imshow(morfo, cmap='Greys')

    x, y = stpunto[1], stpunto[0]
    for direc in guardar:
        move = [
            (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)
        ][direc]
        x += move[1]
        y += move[0]
        ax.plot(x, y, 'ro')

    ax.plot(stpunto[1], stpunto[0], 'go')
    plt.show()
    return guardar