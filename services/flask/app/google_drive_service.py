"""
Install the Google Client Library
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# pip install -U google-api-python-client oauth2client
"""

from googleapiclient import discovery
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools
import io


SCOPES = ['https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive.metadata',
          'https://www.googleapis.com/auth/drive.appdata']


def get_auth():
    store = file.Storage('auth/storage.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('auth/credencials-nfc.json', SCOPES)
        creds = tools.run_flow(flow, store)

    return discovery.build('drive', 'v3', http=creds.authorize(Http()))


def get_data_file():
    # request file
    drive = get_auth()
    file_id = '1ubq53xDZpNrk9hGz3tlMpzAS4vQn2Z5aNemRCE-7XHo'
    request = drive.files().export_media(fileId=file_id, mimeType='text/csv')

    # read file
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download File  %d%%." % int(status.progress() * 100))

    # decoding file
    byte_str = fh.getvalue()
    text_data = byte_str.decode('UTF-8')
    return text_data
