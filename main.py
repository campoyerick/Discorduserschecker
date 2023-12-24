import time
import requests

token = ""
headers = {"Authorization": token}

# Discord username API endpoint
endpoint = "https://discord.com/api/v10/users/@me/pomelo"

def check_username_availability(username):
    url = endpoint
    body = {"username": username}
    
    response = requests.post(url, headers=headers, json=body)
    
    # Tratamento de limite de taxa (Rate limit)
    if response.status_code == 429:
        sleep_time = response.json()["retry_after"]
        print(f"Limite atingido. Aguardando {sleep_time}s")
        time.sleep(sleep_time)
        response = requests.post(url, headers=headers, json=body)
    
    if response.status_code == 200:
        if response.json()['code'] == 40001:
            print(f"{username} está disponível")
            return True
        elif response.json()['code'] == 50035:
            print(f"{username} está ocupado")
        else:
            print(f"Erro ao verificar {username}: {response.json()['message']}")
    else:
        print(f"Erro na solicitação para {username}. Código de status: {response.status_code}")

    return False

# Carrega nomes de usuário a partir do arquivo
with open("usernames.txt") as file:
    usernames = [line.strip() for line in file]

# Verifica a disponibilidade e armazena os nomes de usuário disponíveis
available_usernames = [username for username in usernames if check_username_availability(username)]

# Salva os nomes de usuário disponíveis em um arquivo
with open("available_usernames.txt", "w") as file:
    file.write("\n".join(available_usernames))
