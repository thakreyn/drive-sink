import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaFileUpload

from termcolor import colored

# from . import utility import read_config_file, edit_config_file, log
from . import utility as user_utility
# from init import edit_config_file

import os
from . import scan as user_scan

class MyDrive():

    def __init__(self):
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/drive']

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        curr_dir = user_utility.read_config_file() + "/.sink/config/"

        if os.path.exists(curr_dir + 'token.json'):
            creds = Credentials.from_authorized_user_file(curr_dir + 'token.json', SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    curr_dir + 'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(curr_dir + 'token.json', 'w') as token:
                token.write(creds.to_json())

        # Service variable
        self.service = build('drive', 'v3', credentials=creds)
        print("Google Drive Service Built! Connected to Drive. . .")


    def list_files(self, page_size = 10):
        # Call the Drive v3 API
        results = self.service.files().list(
            pageSize=page_size, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))


    def upload_file(self, filename, path, folder_id):

        media = MediaFileUpload(os.path.join(path, filename))

        file_metadata = {
            'name': filename,
            'parents' : [folder_id]
            
            }
        file = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        
        print(f"New file created! {file.get('id')}")

        return file.get('id')


    def update_file(self, filename, path, file_id):
        """ Update the contents of the given file id"""

        update_media = MediaFileUpload(os.path.join(path, filename))

        file_metadata = {
            'name': filename
            }

        update_file = self.service.files().update(
            fileId = file_id,
            body = file_metadata,
            media_body = update_media).execute()



    def create_folder(self, folder_name, parent_folder = ""):
        """ Creates a folder in the drive with specified name and parent (no parent by default) """

        if parent_folder == "":
            file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }   
        else:
            file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents' : [parent_folder]
        }
            
        file = self.service.files().create(body=file_metadata,
                                            fields='id').execute()

        # print(f"\nSource Folder ID {file.get('id')}")
        # log(f"Created drive Folder ID {file.get('id')}")

        return file.get('id')

    def delete_file(self, file_id):
        """ Deletes the file / folder with given id"""

        # file_id='1AKMgCR6v-6uc-JSvhsttBITJzf7k-pDg'

        file = self.service.files().delete(fileId=file_id).execute()


def list_all_files():
    """ List the first 10 files of the drive """
    mydrive = MyDrive()
    mydrive.list_files()


def init_drive_files():
    """ Initializes the files token.json and verfies credentials.json for further use """

    curr_dir = user_utility.read_config_file()

    if user_utility.read_config_file("general","drive_status") == "False":
        if os.path.exists(curr_dir + "/.sink/config/credentials.json"):
            mydrive = MyDrive()
            user_utility.edit_config_file("general", "drive_status", "True")
            print(colored("Drive succesfully verified and Initialised",'green'))

            folder_id = mydrive.create_folder(user_utility.read_config_file("user", "folder_name"))
            user_utility.log(f"Root Folder ID : {folder_id}")

            user_utility.edit_config_file("user", "folder_id", folder_id)

            print("\nScanning and Initialising Folders. . .")

            user_utility.log("Drive credentials verified")
            return True



        else:
            print(colored( "[Error] : credentials.json not found ! Verfictaion unsuccesful", 'red'))

    else:
        print(colored("[Error] The drive has already been initialised! Use '--help' to see more options",'red'))

    return False

