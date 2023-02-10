import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def encrypt_image(image_file, key):
    # Leer el archivo de imagen y convertirlo en una matriz de bytes
    with open(image_file, "rb") as image:
        image_data = image.read()

    # Añadir padding a la imagen para que su tamaño sea múltiplo de 16 bytes
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(image_data) + padder.finalize()

    # Crear un objeto Cipher para encriptar la imagen
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(key), backend=backend)
    encryptor = cipher.encryptor()

    # Encriptar la imagen
    encrypted_image = encryptor.update(padded_data) + encryptor.finalize()

    # Guardar la imagen encriptada en un archivo
    with open("encrypted_" + image_file, "wb") as encrypted_file:
        encrypted_file.write(encrypted_image)

def decrypt_image(encrypted_image_file, key):
    # Leer el archivo de imagen encriptado y convertirlo en una matriz de bytes
    with open(encrypted_image_file, "rb") as encrypted_image:
        encrypted_image_data = encrypted_image.read()

    # Crear un objeto Cipher para desencriptar la imagen
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(key), backend=backend)
    decryptor = cipher.decryptor()

    # Desencriptar la imagen
    decrypted_padded_data = decryptor.update(encrypted_image_data) + decryptor.finalize()

    # Quitar el padding de la imagen
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    # Guardar la imagen desencriptada en un archivo
    with open("decrypted_" + encrypted_image_file, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)

# Ejemplo de uso
key = os.urandom(16)
encrypt_image("image.jpg", key)
decrypt_image("encrypted_image.jpg", key)
