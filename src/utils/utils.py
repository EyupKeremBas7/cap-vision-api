from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os


def API_AUTH():
    client_secret_path = '/storage/favorable-valor-469612-u5-5d06c7320e21.json'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = client_secret_path
    if not os.path.exists(client_secret_path):
        raise FileNotFoundError(f"client_secret.json dosyası bulunamadı: {client_secret_path}")
