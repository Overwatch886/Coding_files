import requests

try:
    res = requests.get('https://automatetheboringstuff.com/')
    res.raise_for_status()
    with open("/storage/EFD6-7824/Documents/Coding_Files/hello.html", "wb") as PlayFile:
        for chunk in res.iter_content(1024):
            PlayFile.write(chunk)
except Exception as exc:
    print(f'An error occurred: {exc}')