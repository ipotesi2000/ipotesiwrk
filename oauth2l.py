#!/usr/bin/env python
# coding: utf-8
import os.path
import base64
import email

from email.header import decode_header
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopi richiesti per l'accesso a Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # Il file token.json memorizza l'accesso e i token di aggiornamento dell'utente,
    # e viene creato automaticamente quando l'autorizzazione viene completata per la prima volta.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Se non ci sono credenziali (prima esecuzione) o sono scadute,
    # esegui il flusso di consenso.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva le credenziali per la prossima esecuzione
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Chiama l'API Gmail
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    if not messages:
        print('Nessuna email trovata.')
    else:
        print('Email trovate:')
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            print(f"ID: {message['id']} Snippet: {msg['snippet']}")

if __name__ == '__main__':
    main()
