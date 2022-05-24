import requests


def postText(file_path):
    url = 'http://127.0.0.1:8000/receive/'
    file = {'file': open(file_path, 'rb')}
    resp = requests.post(url, files=file)
    print(resp.text)


if __name__ == '__main__':
    postText('smallText.txt')
