import requests
from bs4 import BeautifulSoup
import time

pairs = {
    'pochta1@gmail.com': '1234',
    'pochta2@yahoo.com': '5678',
    'pochta3@hotmail.com': '9012',
    'pochta4@outlook.com': '3456',
    'pochta5@icloud.com': '7890',
    'pochta6@aol.com': '2345',
    'pochta7@mail.com': '6789',
    'pochta8@inbox.com': '0123'
}

login_url = 'http://127.0.0.1:5000/login'


def get_csrf_token(session, url):
    # Функция для получения токена CSRF
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'}).get('value')
    return csrf_token


def login_request(session, username, password, csrf_token):
    # Функция для выполнения запроса на вход
    payload = {'email': username, 'password': password, 'csrf_token': csrf_token}
    response = session.post(login_url, data=payload, allow_redirects=False)
    return response


def main():
    with requests.Session() as session:
        csrf_token = get_csrf_token(session, login_url)

        for username, password in pairs.items():
            while True:
                response = login_request(session, username, password, csrf_token)

                if response.status_code == 302:
                    print(f"Successful login - Username: {username}, Password: {password}")
                    return
                elif response.status_code == 429:
                    print("Too Many Requests. Pausing for 1 minute.")
                    time.sleep(60)
                else:
                    break


if __name__ == "__main__":
    main()
