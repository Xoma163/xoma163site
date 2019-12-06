# from __future__ import print_function
import os.path
import pickle
import time

from django.core.management.base import BaseCommand
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from apps.API_VK.models import Words
from secrets.secrets import secrets
from xoma163site.settings import BASE_DIR


class Command(BaseCommand):

    def __init__(self):
        super().__init__()

    def handle(self, *args, **kwargs):
        PETROVICH_ID = secrets['google']['petrovich_id']
        RANGE_NAMES = secrets['google']['range_names']
        API_KEY = secrets['google']['api_key']
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        creds = None
        if os.path.exists(BASE_DIR + '/secrets/google_token.pickle'):
            with open(BASE_DIR + '/secrets/google_token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(BASE_DIR + '/secrets/google_credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open(BASE_DIR + '/secrets/google_token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)
        # drive_service = build('drive', 'v3', credentials=creds)

        result = service.spreadsheets().values().batchGet(spreadsheetId=PETROVICH_ID,
                                                          ranges=RANGE_NAMES,
                                                          key=API_KEY).execute()
        ranges = result.get('valueRanges', [])
        headers = []
        time1 = time.time()

        for i, my_range in enumerate(ranges):
            if i == 0:
                word_type = 'bad'
            else:
                word_type = 'good'
            for j, val in enumerate(my_range['values']):
                if j != 0:
                    word_dict = {'type': word_type}
                    for k, item in enumerate(val):
                        if item != 'None' and item is not None and item != ' ' and item != '':
                            word_dict[headers[k]] = item
                    if 'id' in word_dict:
                        word, created = Words.objects.update_or_create(id=word_dict['id'], defaults=word_dict)
                    else:
                        print("Слово не имеет id. Проверьте - {}".format(word_dict))
                    # new_word = Words(**word_dict)
                    # new_word.save()
                else:
                    headers = [header for header in val]
        print("Result: success")
        print("Time: {}".format(time.time() - time1))
