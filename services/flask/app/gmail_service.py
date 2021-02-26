# Creating messages
"""
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
"""
import base64
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

from email.message import EmailMessage
from email.utils import make_msgid

from apiclient import errors

scopes = [
    'https://www.googleapis.com/auth/gmail.metadata',
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/gmail.send'
]

path_spreadsheet = 'utils/tugs_scheduler.xlsx'


def send():
    # If modifying these scopes, delete the file token.pickle.
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('auth/token.pickle'):
        with open('auth/token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('auth/credencials-nfc.json', scopes)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('auth/token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    # create service
    service = build('gmail', 'v1', credentials=credentials)

    # create message
    emails = [
        'marlene.ortiz@naviera.com.co',
        'marleneortizrivera@gmail.com',
        'marle.rivera@yahoo.es',
        'giovanet.0313@gmail.com']

    message = create_message('carrenolg@gmail.com', emails, 'NFC Operaciones')
    respond = send_message(service, 'me', message)
    # respond = None
    if not respond:
        print('No email send.')
    else:
        print(respond)


def create_message(sender, to, subject):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    # First craft the message to be encapsulated
    m = EmailMessage()
    m['to'] = to
    m['from'] = sender
    m['subject'] = subject
    asparagus_cid = make_msgid(idstring="img-nfc")
    file = open("utils/style.css", "r")
    style = file.read()
    file.close()

    # adding html text
    m.add_alternative("""\
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <style type="text/css">
            {styles_cid}
        </style>
      </head>
      <body>
        <p>Planificación de fumigación y desinfección </p>
        <p>Naviera fluvial Colombiana S.A.</p>
        <img src="cid:{asparagus_cid}" />
      </body>
    </html>
    """.format(asparagus_cid=asparagus_cid[1:-1], styles_cid=style), subtype='html')

    # Now add the related image to the html part.
    with open("utils/nfc.png", 'rb') as img:
        m.get_payload()[0].add_related(img.read(), 'image', 'png', cid=asparagus_cid)

    # Now add attachment
    with open(path_spreadsheet, 'rb') as fp:
        m.add_attachment(fp.read(), maintype='application', subtype='vnd.ms-excel', filename='tugs_scheduled.xlsx')

    return {'raw': base64.urlsafe_b64encode(m.as_bytes()).decode()}


def send_message(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
