import datetime
import json
import requests
from urllib.parse import urlencode

from .models import YoutubeVideo

YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
PRE_DEFINED_STRING = 'corona'
TOKENS = ["AIzaSyCCLO5ZxJy7W_FYE8362NcaAhxKOkQLFPQ", "AIzaSyBuScbdHbZUrQtKUVYzREPf7Jy1eMObMfk"]

class YouTubeApi():
    token = TOKENS[0]

    def store_search_result(self, search_response):
        for search_result in search_response.get("items", []):
            YoutubeVideo.add_item(search_result)

    def refresh_token(self, attempt=1):
        self.token = TOKENS[min(len(TOKENS), attempt)]

    def store_recent_data(self, key_word=PRE_DEFINED_STRING):
        now = datetime.datetime.now()
        now_minus_30 = now - datetime.timedelta(minutes=30)
        published_after = now_minus_30.strftime("%Y-%m-%dT%H:%M:%SZ")
        params = {
                    'key': self.token,
                    'part': 'id,snippet',
                    'q': key_word,
                    'type': 'video',
                    'order' : 'date',
                    'publishedAfter': published_after
                }

        matches = self.get_data(YOUTUBE_SEARCH_URL, params)
        search_response = json.loads(matches)
        next_page = search_response.get("nextPageToken",'')
        self.store_search_result(search_response)

        while next_page:
            params.update({'pageToken': next_page})
            matches = self.get_data(YOUTUBE_SEARCH_URL, params)
            search_response = json.loads(matches)
            next_page = search_response.get("nextPageToken",'')
            self.store_search_result(search_response)


    def get_data(self, url, params, attempt=1):
        print(url + '?' + urlencode(params))
        f = requests.get(url + '?' + urlencode(params))
        if f.status_code == 200:
            print(f.content)
            return f.content
        elif attempt<3:
            #3 retry to toggle/refresh token
            self.refresh_token(attempt)
            self.get_data(url, params, attempt=attempt+1)
        else:
            return {}
