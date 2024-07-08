from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
import os
from datetime import datetime

# Verifica e cria a pasta de logs se não existir
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Função para ler os números de telefone do arquivo
def ler_numeros(arquivo):
    with open(arquivo, 'r') as f:
        numeros = f.read().splitlines()
    return numeros

# Função para enviar a mensagem com log
def enviar_mensagem(numero, mensagem):
    try:
        # Abre a conversa com o número especificado
        driver.get(f'https://web.whatsapp.com/send?phone=55{numero}&text&app_absent=0')
        
        # Espera até que a caixa de mensagem esteja disponível
        caixa_mensagem = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        
        # Copia e cola a mensagem, espera 1 segundo para garantir que a mensagem foi colada
        pyperclip.copy(mensagem)
        caixa_mensagem.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)     
        
        caixa_mensagem.send_keys(Keys.ENTER)
        time.sleep(3)  # Espera a mensagem ser enviada

        # Log de sucesso
        with open(os.path.join(log_directory, 'success.log'), 'a', encoding='utf-8') as log_file:
            log_file.write(f"{datetime.now()} - Mensagem enviada para {numero}\n")

        print(f"{datetime.now()} - Mensagem enviada com sucesso para o número {numero}")

    except Exception as e:
        # Log de erro simplificado
        error_message = f"{datetime.now()} - Erro ao enviar mensagem para {numero}"
        with open(os.path.join(log_directory, 'error.log'), 'a', encoding='utf-8') as log_file:
            log_file.write(f"{error_message}\n")
        print(error_message)

# Configura o driver do Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Mensagem personalizada no terminal
print(" ==========================================================================================")
print("|| Desenvolvido por @duhmurillo (https://instagram.com/duhmurillo)                        ||")
print("|| Por favor, escaneie o código QR com o seu aplicativo WhatsApp para iniciar a execução! ||")
print("|| Após escanear, apenas relaxe e deixe com a gente :)                                    ||")
print(" ==========================================================================================\n")

# Abra o WhatsApp Web para login manual
driver.get('https://web.whatsapp.com')

# Espera até que o QR code seja escaneado e o WhatsApp esteja pronto
try:
    WebDriverWait(driver, timeout=600).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="pane-side"]'))
    )    
    print("QR code escaneado. Iniciando processo em 3")
    time.sleep(1)
    print("QR code escaneado. Iniciando processo em 2")
    time.sleep(1)
    print("QR code escaneado. Iniciando processo em 1")
    time.sleep(1)
    print("Execução iniciada!")

    # Inicia o cronômetro
    start_time = time.time()

    # Caminhos dos seus arquivos
    caminho_arquivo_numeros = 'C:\\WppBotPython\\numeros.txt'
    caminho_arquivo_mensagem = 'C:\\WppBotPython\\mensagem.txt'

    # Ler números e mensagem dos arquivos
    numeros = ler_numeros(caminho_arquivo_numeros)
    with open(caminho_arquivo_mensagem, 'r', encoding='utf-8') as file:
        mensagem = file.read()

    # Loop para enviar mensagens para cada número
    for numero in numeros:
        try:
            enviar_mensagem(numero, mensagem)
        except Exception as e:
            print(f"Erro ao processar o número {numero}: {e}")
        
        time.sleep(2)  # Espera um tempo entre mensagens para evitar bloqueios

    # Calcula o tempo total de execução
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Tempo total de execução: {total_time:.2f} segundos")

finally:
    # Encerra o driver após o término do processo
    driver.quit()
