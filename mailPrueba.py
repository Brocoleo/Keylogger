import smtplib
import ssl

ctx = ssl.create_default_context()
password = "lqcuadiizlyygavn"    # Your app password goes here
sender = "leomir2656@gmail.com"    # Your e-mail address
receiver = "leomir2656@gmail.com" # Recipient's address
message = """
Hello from Python 2.
"""

with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
    server.login(sender, password)
    server.sendmail(sender, receiver, message)