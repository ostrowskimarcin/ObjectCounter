from __future__ import print_function
import config

import pickle
import os
from enum import Enum

import cv2
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

actual_dir = os.path.dirname(os.path.abspath(__file__))
credentials_json_path = os.path.join(actual_dir, 'credentials.json')
token_pickle_path = os.path.join(actual_dir, 'token.pickle')
temp_img_path = os.path.join(actual_dir, 'temporary.jpg')


class Lines(Enum):
    ENTRANCE_LINE = 0
    EXIT_LINE = 1


class Drive:

    def __init__(self):
        self.creds = None
        self.service = None
        self.set_api()

    def set_api(self):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_pickle_path):
            with open(token_pickle_path, 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_json_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_pickle_path, 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('drive', 'v3', credentials=self.creds)

    def upload(self, frame, time, ID: int, line: Lines):
        if line == Lines.ENTRANCE_LINE:
            directory_id = config.ENTRANCE_DIRECTORY_DRIVE_ID
            img_name = str(time) + '_entrance_ID=' + str(ID)

        elif line == Lines.EXIT_LINE:
            directory_id = config.EXIT_DIRECTORY_DRIVE_ID
            img_name = str(time) + '_exit_ID=' + str(ID)
        else:
            pass
            #TODO Error handling

        cv2.imwrite(temp_img_path, frame)

        file_metadata = {
            'name': img_name,
            'parents': [directory_id]
        }
        media = MediaFileUpload(temp_img_path,
                                mimetype='image/jpeg',
                                resumable=True)
        file = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        'File ID: %s' % file.get('id')


