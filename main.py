import cv2
import numpy as np
import os

from encryption import (
    phtc_transform,
    generate_secret_key,
    split_key,
    initial_permutation,
    generate_sbox,
    xor_diffusion
)

from decryption import (
    inverse_phtc_transform,
    xor_decryption
)

from metrics import (
    calculate_entropy,
    calculate_npcr,
    calculate_uaci,
    calculate_correlation,
    save_histogram
)


def process_image(image_path, name):

    print("\n==============================")
    print("Processing:", name)
    print("==============================")

    os.makedirs(f"results/{name}", exist_ok=True)

    # Load image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    print("Original image:", image.shape)

    # PHTC
    transformed = phtc_transform(image)

    save_histogram(
    image,
    f"results/{name}/original_histogram.png",
    f"{name.capitalize()} Original Image Histogram"
)

    cv2.imwrite(
        f"results/{name}/phtc.png",
        transformed
    )

    print("PHTC transformation completed")

    # Secret key
    key = generate_secret_key()

    groups = split_key(key)
    
    # Initial permutation
    permuted_groups = initial_permutation(groups)

    # S-box
    sbox = generate_sbox(permuted_groups)

    print("S-box generated")

    # Encryption
    cipher_image = xor_diffusion(
        transformed,
        sbox
    )

    cv2.imwrite(
        f"results/{name}/cipher.png",
        cipher_image
    )
    save_histogram(
    cipher_image,
    f"results/{name}/cipher_histogram.png",
    f"{name.capitalize()} Cipher Image Histogram"
)

    print("Encryption completed")

    # Decryption
    decrypted_transformed = xor_decryption(
        cipher_image,
        sbox
    )

    recovered_image = inverse_phtc_transform(
        decrypted_transformed
    )

    cv2.imwrite(
        f"results/{name}/decrypted.png",
        recovered_image
    )

    # Verify
    if np.array_equal(image, recovered_image):
        print("SUCCESS: Original and decrypted images are identical")
    else:
        print("ERROR: Original and decrypted images are different")

    # Entropy
    entropy = calculate_entropy(cipher_image)

    print("Entropy:", entropy)

    # Create modified image
    modified_image = image.copy()

    modified_image[0, 0] = (
        int(modified_image[0, 0]) + 1
) % 256
    

    # Encrypt modified image
    modified_transformed = phtc_transform(
        modified_image
    )

    modified_cipher = xor_diffusion(
        modified_transformed,
        sbox
    )
    
    cv2.imwrite(
        f"results/{name}/cipher_modified.png",
        modified_cipher
    )

    # NPCR
    npcr = calculate_npcr(
        cipher_image,
        modified_cipher
    )

    print("NPCR:", npcr, "%")

    # UACI
    uaci = calculate_uaci(
        cipher_image,
        modified_cipher
    )

    print("UACI:", uaci, "%")

    # Correlation
    correlation = calculate_correlation(
        cipher_image
    )

    print("Correlation:", correlation)

    return entropy, npcr, uaci, correlation


process_image(
    "images/lena.png",
    "lena"
)

process_image(
    "images/baboon.bmp",
    "baboon"
)

process_image(
    "images/peppers.jpg",
    "peppers"
)