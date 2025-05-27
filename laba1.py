import requests
import os

def print_task_header(task_number, description):
    print(f"\n{'=' * 50}")
    print(f"ЗАДАНИЕ {task_number}: {description}")
    print(f"{'=' * 50}\n")

def download_image(url, filename):
    print_task_header(1, "Скачивание файла с картинкой")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Успешно! Изображение сохранено как '{filename}'")
        print(f"Размер файла: {os.path.getsize(filename)} байт")
    except Exception as e:
        print(f"Ошибка: {e}")

def view_headers(url):
    print_task_header(2, "Просмотр заголовков HTTP-ответа")
    try:
        response = requests.head(url)
        print("Заголовки ответа:")
        for header, value in response.headers.items():
            print(f"  {header:30}: {value}")
    except Exception as e:
        print(f"Ошибка: {e}")

def get_with_params(url, params):
    print_task_header(3, "Запрос с параметрами")
    try:
        response = requests.get(url, params=params)
        print(f"Отправленные параметры: {params}")
        print("\n Ответ сервера:")
        print(response.text)
    except Exception as e:
        print(f"Ошибка: {e}")

def send_request(url, method='GET', data=None):
    methods = {
        'GET': "GET-запрос",
        'POST': "POST-запрос",
        'PUT': "PUT-запрос",
        'DELETE': "DELETE-запрос"
    }
    print_task_header(4, f"{methods.get(method, method)}")
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data)
        elif method.upper() == 'DELETE':
            response = requests.delete(url)
        else:
            print("Неизвестный метод")
            return
            
        print(f"🛠️ Метод: {method}")
        print(f"📌 URL: {url}")
        if data:
            print(f"Отправленные данные: {data}")
        print(f"\n Ответ ({response.status_code}):")
        print(response.text)
    except Exception as e:
        print(f"Ошибка: {e}")

def resume_download(url, filename):
    print_task_header(5, "Докачка файла после остановки")
    try:
        file_size = os.path.getsize(filename) if os.path.exists(filename) else 0
        print(f"Текущий размер файла: {file_size} байт")
        
        headers = {'Range': f'bytes={file_size}-'}
        response = requests.get(url, headers=headers, stream=True)
        
        if response.status_code == 206:
            with open(filename, 'ab') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Успешно! Новый размер файла: {os.path.getsize(filename)} байт")
        else:
            print("Сервер не поддерживает докачку")
    except Exception as e:
        print(f"Ошибка: {e}")

def use_cookies(url):
    print_task_header(6, "Работа с Cookies")
    try:
        session = requests.Session()
        
        print("Отправляем запрос с cookies...")
        response = session.get(url, cookies={'test_cookie': '12345'})
        
        print("Установленные cookies:")
        for cookie in session.cookies:
            print(f"  {cookie.name}: {cookie.value}")
        
        print("\n Отправляем второй запрос (cookies будут автоматически)...")
        response2 = session.get(url)
        print(f"Ответ сервера:\n{response2.text}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    image_url = "https://bigpicture.ru/wp-content/uploads/2015/11/nophotoshop29-800x532.jpg"
    api_url = "https://bigpicture.ru/wp-content/uploads/2015/11/nophotoshop29-800x532.jpg"

    download_image(image_url, "image.jpg")
    view_headers(image_url)
    get_with_params(api_url + "get", {"param1": "value1", "test": "123"})

    send_request(api_url + "get", 'GET')
    send_request(api_url + "post", 'POST', {"key": "value"})
    send_request(api_url + "put", 'PUT', {"key": "value"})
    send_request(api_url + "delete", 'DELETE')

    if not os.path.exists("partial.jpg"):
        with open("partial.jpg", 'wb') as f:
            r = requests.get(image_url, stream=True)
            for i, chunk in enumerate(r.iter_content(1024)):
                if i < 5:
                    f.write(chunk)
                else:
                    break
    resume_download(image_url, "partial.jpg")
    
    use_cookies(api_url + "cookies")
