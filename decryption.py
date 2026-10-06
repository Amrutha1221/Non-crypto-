import numpy as np


def inverse_phtc_transform(transformed, k=1):
    n = transformed.shape[0]

    recovered = np.zeros_like(transformed)

    for a in range(n):
        for b in range(n):

            y = (b - a) % n
            x = (2 * a - b - 2 * k) % n

            recovered[x, y] = transformed[a, b]

    return recovered
def xor_decryption(cipher_image, sbox):

    flat_image = cipher_image.flatten().astype(np.uint8)

    decrypted = np.zeros_like(flat_image)

    previous = 0

    for i in range(len(flat_image)):

        # Find the S-box input
        target = int(flat_image[i])

        for value in range(256):

            if (
                int(sbox[value]) ^ int(sbox[i % 256])
            ) == target:
                current_value = value
                break

        # Reverse addition
        decrypted[i] = (
            current_value - int(previous)
        ) % 256

        previous = flat_image[i]

    return decrypted.reshape(cipher_image.shape)