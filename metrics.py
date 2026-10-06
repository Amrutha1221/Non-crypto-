import cv2
import numpy as np


def calculate_entropy(image):
    histogram = cv2.calcHist([image], [0], None, [256], [0, 256])

    probabilities = histogram / histogram.sum()

    entropy = 0

    for p in probabilities:
        if p > 0:
            entropy -= p * np.log2(p)

    return float(entropy)
def calculate_npcr(cipher1, cipher2):
    different_pixels = np.sum(cipher1 != cipher2)

    total_pixels = cipher1.size

    npcr = (different_pixels / total_pixels) * 100

    return float(npcr)
def calculate_uaci(cipher1, cipher2):
    difference = np.abs(
        cipher1.astype(np.int16) - cipher2.astype(np.int16)
    )

    uaci = (np.sum(difference) / (cipher1.size * 255)) * 100

    return float(uaci)
def calculate_correlation(image):
    x = image[:, :-1].flatten().astype(np.float64)
    y = image[:, 1:].flatten().astype(np.float64)

    correlation = np.corrcoef(x, y)[0, 1]

    return float(correlation)
def save_histogram(image, path, title):

    import matplotlib.pyplot as plt

    plt.figure()
    plt.hist(image.flatten(), bins=256, range=(0, 256))
    plt.title(title)
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")
    plt.savefig(path)
    plt.close()