import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:8000/api/"
GROUPCHATS_URL = BASE_URL + "groupchats/"
USERNAME = "olsil"  # Замените на ваш логин
PASSWORD = "123456789"  # Замените на ваш пароль

def list_groupchats():
    response = requests.get(GROUPCHATS_URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        print("List of GroupChats:", response.json())
    else:
        print("Failed to retrieve group chats:", response.status_code, response.text)

def create_groupchat(name):
    data = {"name": name}
    response = requests.post(GROUPCHATS_URL, json=data, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 201:
        print("GroupChat created:", response.json())
    else:
        print("Failed to create group chat:", response.status_code, response.text)

def delete_groupchat(group_id):
    response = requests.delete(f"{GROUPCHATS_URL}{group_id}/", auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 204:
        print("GroupChat deleted successfully")
    else:
        print("Failed to delete group chat:", response.status_code, response.text)

# Примеры использования
list_groupchats()
create_groupchat("NewGroupChat")
group_id = input("Enter the ID of the group chat to delete: ")
delete_groupchat(group_id)
