import cv2
from google.colab.patches import cv2_imshow
import numpy as np

def backtracking(T, p, c, B):
    x, y = p
    rows, cols = T.shape

    neighbors = [
        (x + 1, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1),
        (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
    ]

    found_index = None

    for index, neighbor in enumerate(neighbors):
        if neighbor == c:
            found_index = index
            break
    if found_index is None:
        return B

    for index in range((found_index + 1) % 8, 8):
        i, j = neighbors[index]
        for l in range(i, rows):
            for k in range(j, cols):
                if T[l, k] == 0:
                    if (l, k) == p:
                        return B
                    else:
                        B.append((l, k))
                        return backtracking(T, (l, k), (i, j), B)

def start(T):
    rows, cols = T.shape
    for j in range(cols):
        for i in range(rows - 1, -1, -1):
            if T[i, j] == 0:
                s = (i, j)
                return s

T = cv2.imread('img1.png', cv2.IMREAD_GRAYSCALE)
threshold_value = 120
_, T = cv2.threshold(T, threshold_value, 255, cv2.THRESH_BINARY)

s = start(T)
p = s

if p[1] != 0:
    c = (p[0], p[1] - 1)
else:
    c = (p[0] + 1, p[1])

B = backtracking(T, p, c, [s])

result = np.zeros_like(T)
for pixel in B:
    result[pixel[0], pixel[1]] = 255

cv2_imshow(result)
