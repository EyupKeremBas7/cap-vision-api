from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os


def API_AUTH():
    client_secret_path = 'storage/client_secret.json'
    if not os.path.exists(client_secret_path):
        raise FileNotFoundError(f"client_secret.json dosyası bulunamadı: {client_secret_path}")
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secret_path,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    creds = flow.run_console()