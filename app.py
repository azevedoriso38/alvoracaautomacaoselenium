import subprocess
import sys
import time
import random
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

# ================== INSTALAR PACOTES ==================
def instalar_pacote(pacote):
    try:
        __import__(pacote)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

instalar_pacote("selenium")
instalar_pacote("webdriver_manager")

# ================== IMPORTS ==================
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ================== DRIVER GLOBAL ==================
driver = None

# ================== DIGITAÇÃO HUMANA ==================
def digitar_humano(elemento, texto):
    for letra in texto:
        elemento.send_keys(letra)
        time.sleep(random.uniform(0.05, 0.15))

# ================== ENVIO DE MENSAGENS ==================
def enviar_mensagens():
    global driver

    numeros = text_numeros.get("1.0", tk.END).strip().splitlines()
    mensagem = text_mensagem.get("1.0", tk.END).strip()

    if not numeros or not mensagem:
        app.after(0, lambda: messagebox.showerror("Erro", "Preencha números e mensagem."))
        return

    try:
        if driver is None:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
            driver.get("https://web.whatsapp.com")
            app.after(0, lambda: messagebox.showinfo(
                "WhatsApp",
                "Escaneie o QR Code e aguarde o WhatsApp abrir completamente."
            ))
            time.sleep(15)
    except Exception as e:
        app.after(0, lambda: messagebox.showerror("Erro", str(e)))
        return

    wait = WebDriverWait(driver, 30)

    for numero in numeros:
        numero = numero.strip().replace(" ", "").replace("+", "")
        if not numero:
            continue

        try:
            driver.get(f"https://web.whatsapp.com/send?phone={numero}")
            time.sleep(random.uniform(6, 10))

            caixa = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@contenteditable="true" and @data-tab="10"]')
                )
            )

            caixa.click()
            digitar_humano(caixa, mensagem)
            time.sleep(random.uniform(1, 2))
            caixa.send_keys(Keys.ENTER)

            time.sleep(random.uniform(10, 18))

        except Exception as e:
            print(f"[ERRO] Número {numero}: {e}")
            continue

    app.after(0, lambda: messagebox.showinfo("Finalizado", "Envio concluído!"))

# ================== THREAD ==================
def iniciar_envio():
    threading.Thread(target=enviar_mensagens, daemon=True).start()

# ================== INTERFACE ==================
app = tk.Tk()
app.title("WhatsApp Sender - Selenium")
app.geometry("500x600")

tk.Label(app, text="NÚMEROS (1 por linha)").pack()
text_numeros = scrolledtext.ScrolledText(app, height=10)
text_numeros.pack(fill="both", padx=10)

tk.Label(app, text="MENSAGEM").pack()
text_mensagem = scrolledtext.ScrolledText(app, height=6)
text_mensagem.pack(fill="both", padx=10)

btn = tk.Button(
    app,
    text="ENVIAR MENSAGENS",
    command=iniciar_envio,
    bg="green",
    fg="white"
)
btn.pack(pady=20)

app.mainloop()
