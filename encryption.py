import cv2
import numpy as np


def phtc_transform(image, k=1):
    n = image.shape[0]

    transformed = np.zeros_like(image)

    for x in range(n):
        for y in range(n):

            a = (x + y + 2 * k) % n
            b = (x + 2 * y + 2 * k) % n

            transformed[a, b] = image[x, y]

    return transformed

def generate_secret_key():
    key = "1011001110001111000011111010101010101100110011001100110011110000" \
          "1100110011001100001111110000111101010101101010101010101001010101"

    return key
def split_key(key):
    groups = []

    for i in range(0, 128, 16):
        groups.append(key[i:i+16])

    return groups
def initial_permutation(groups):
    permutation = [1, 3, 5, 7, 0, 2, 4, 6]

    permuted_groups = []

    for index in permutation:
        permuted_groups.append(groups[index])

    return permuted_groups
def generate_sbox(permuted_groups):
    key_bits = "".join(permuted_groups)

    seed = int(key_bits, 2)

    rng = np.random.default_rng(seed)

    sbox = rng.permutation(256)

    return sbox
def xor_diffusion(transformed, sbox):

    flat_image = transformed.flatten().astype(np.uint8)

    encrypted = np.zeros_like(flat_image)

    previous = 0

    for i in range(len(flat_image)):

        value = (
            int(flat_image[i]) + int(previous)
        ) % 256

        encrypted[i] = (
            int(sbox[value]) ^ int(sbox[i % 256])
        )

        previous = encrypted[i]

    return encrypted.reshape(transformed.shape)