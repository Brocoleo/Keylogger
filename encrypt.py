from cryptography.fernet import Fernet

def generar_key():
    key = Fernet.generate_key()
    with open('pass.key', 'wb') as file:
        file.write(key)

def cargar_key():
    return open('pass.key', 'rb').read()

generar_key()

key = cargar_key()

mensaje = b'tucontrasenaaqui'

clave = Fernet(key)
pass_enc = clave.encrypt(mensaje)
print(pass_enc)
pass_decrypt = clave.decrypt(pass_enc)
print(pass_decrypt)
