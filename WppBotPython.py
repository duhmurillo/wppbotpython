from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from supabase import create_client, Client
import os
import pyperclip
import pwinput
import socket
import sys
import time

# Configurações do Supabase
url: str = "https://your-supabase-url.supabase.co"
key: str = "your-supabase-api-key"
supabase: Client = create_client(url, key)

def get_machine_name():
    try:
        hostname = socket.gethostname()
        return hostname
    except Exception:        
        return 'None'
    
# Função para atualizar o IP e a data do último acesso
def access_register(userId, username):
    try:
        # Define a tabela e o ID do usuário (exemplo)
        table = 'wppbot_accesshistory'        
        computer_name = get_machine_name()
        access_date = datetime.now().isoformat()

        # Dados para inserção
        data = {
            'username': username,
            'user_id': userId,
            'computer_name': computer_name,
            'access_date': access_date
        }

        # Insere os dados na tabela de histórico
        insert_result = supabase.table(table).insert(data).execute()

        if len(insert_result.data) == 0:
            print("Erro ao inserir registro de acesso (não influencia no uso da automação)")

        if len(insert_result.data) > 0:
            print(f"Registro de acesso inserido com sucesso para o usuário '{username}'\n")

    except Exception:
        print(f"Erro ao inserir registro de acesso (não influencia no uso da automação)")

# Função para verificar login e licença
def login(username, password):
    try:
        # Busca o usuário no banco de dados
        response = supabase.table('wppbot_users').select('*').eq('username', username).eq('password', password).execute()
        if len(response.data) == 0:
            print("\nUsuário ou senha incorretos. Encerrando o programa.")
            print("Execute novamente para tentar o login.")
            return False
        
        # Verifica a data de expiração
        user_data = response.data[0]
        expired_date = datetime.fromisoformat(user_data['expired_date'])
        if expired_date < datetime.now():
            print("\nA licença expirou.")
            print("Entre em contato com o suporte para reativar seu acesso.")
            return False
        
        print("\nLogin realizado com sucesso!\n")
        access_register(user_data['id'], user_data['username'])
        return True
    except Exception as e:
        print(f"Erro ao verificar login")
        return False

# Verifica e cria a pasta de logs se não existir
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Função para ler os números de telefone do arquivo
def get_phones(archive):
    with open(archive, 'r') as f:
        phones = f.read().splitlines()
    return phones

# Função para enviar a mensagem com log
def send_message(phoneNumber, message):
    try:
        # Abre a conversa com o número especificado
        driver.get(f'https://web.whatsapp.com/send?phone=55{phoneNumber}&text&app_absent=0')
        
        # Espera até que a caixa de mensagem esteja disponível
        message_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        
        # Copia e cola a mensagem, espera 1 segundo para garantir que a mensagem foi colada
        pyperclip.copy(message)
        message_box.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)     
        
        message_box.send_keys(Keys.ENTER)
        time.sleep(3)  # Espera a mensagem ser enviada

        # Log de sucesso
        with open(os.path.join(log_directory, 'success.log'), 'a', encoding='utf-8') as log_file:
            log_file.write(f"{datetime.now()} - Mensagem enviada para {phoneNumber}\n")

        print(f"{datetime.now()} - Mensagem enviada com sucesso para o número {phoneNumber}")

    except Exception as e:
        # Log de erro simplificado
        error_message = f"{datetime.now()} - Erro ao enviar mensagem para {phoneNumber}"
        with open(os.path.join(log_directory, 'error.log'), 'a', encoding='utf-8') as log_file:
            log_file.write(f"{error_message}\n")
        print(error_message)

# Configura o driver do Chrome
os.environ['WDM_LOG'] = '0'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

# Login do usuário
print("Por favor faça login abaixo informando seu usuário e senha para que o bot funcione corretamente :)")
username = input("Digite seu usuário: ")
password = pwinput.pwinput(prompt='Digite sua senha: ')

# Verifica o login e a licença
if not login(username, password):
    time.sleep(5)
    sys.exit()

company_name_path = 'C:\\WppBotPython\\company_name.txt'
with open(company_name_path, 'r', encoding='utf-8') as file:
        company_name = file.read()

# Mensagem personalizada no terminal
print(f"Olá {company_name}, vamos trabalhar?")
print(" ==========================================================================================")
#print("|| Desenvolvido por @duhmurillo (https://instagram.com/duhmurillo)                        ||")
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
    print("Execução iniciada!\n")

    # Inicia o cronômetro
    start_time = time.time()

    # Caminhos dos seus arquivos
    phone_path = 'C:\\WppBotPython\\phones.txt'
    message_path = 'C:\\WppBotPython\\messages.txt'

    # Ler números e mensagem dos arquivos
    phones = get_phones(phone_path)
    with open(message_path, 'r', encoding='utf-8') as file:
        message = file.read()

    # Loop para enviar mensagens para cada número
    for phone in phones:
        try:
            send_message(phone, message)
        except Exception as e:
            print(f"Erro ao processar o número {phone}")
        
        time.sleep(2)  # Espera um tempo entre mensagens para evitar bloqueios

    # Calcula o tempo total de execução
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Tempo total de execução: {total_time:.2f} segundos\n")
    print("Até mais :)")

finally:
    # Encerra o driver após o término do processo
    driver.quit()
