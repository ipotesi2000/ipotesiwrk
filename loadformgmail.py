#!/usr/bin/env python
# coding: utf-8
import imaplib
import email
from email.header import decode_header
import os
import argparse

def download_attachments(msg, email_id, output_dir):
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        file_name = part.get_filename()
        if bool(file_name):
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, 'wb') as f:
                f.write(part.get_payload(decode=True))
            print(f'Allegato scaricato: {file_name} da email ID: {email_id}')

def main(email, password, folder, output_dir):
    print(email)
    print(password)
    # Connessione al server IMAP di Gmail
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email, password)

    # Seleziona la cartella da cui vuoi scaricare le email
    mail.select(folder)

    # Cerca tutte le email nella cartella selezionata
    status, messages = mail.search(None, 'ALL')

    # Converte i risultati della ricerca in una lista di ID email
    email_ids = messages[0].split()

    # Directory in cui salvare gli allegati
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Itera su tutte le email e scarica gli allegati
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg['Subject'])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)
                print(f'Oggetto: {subject}')
                download_attachments(msg, email_id, output_dir)
    # Chiudi la connessione
    mail.logout()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scarica email e allegati da un account Gmail.')
    parser.add_argument('-e', 
                        type=str, 
                        default='ipotesi2000@gmail.com', 
                        help='Il tuo indirizzo email Gmail.')
    parser.add_argument('-p', 
                        type=str, 
                        default="tesi_678",
                        help='La tua password Gmail.')
    parser.add_argument('-f', 
                        type=str, 
                        default='email', 
                        help='La cartella da cui scaricare le email (default: email).')
    parser.add_argument('-o', 
                        type=str, 
                        default='email_allegati', 
                        help='La directory in cui salvare gli allegati (default: email_allegati).')
    args = parser.parse_args()

    main(args.e, args.p, args.f, args.o)
