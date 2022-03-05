#!/usr/bin/env python3

import json
import urllib.request

class IwaraWrapper:
    def __init__(self):
        self.preload_tag = '_placeholder_'
        self.preload_data = []
        self.latest_page = -1

    def get_batch(self, current_tag, query_page, query_limit, first_post, caller):
        item_list = []

        # Check if new search needs to be conducted
        wanted_tag = current_tag.replace('%20', ' ').replace('+', ' ')
        if self.preload_tag != wanted_tag:
            self.preload_tag = wanted_tag
            self.preload_data = []
            self.latest_page = -1

        # Conduct minimum needed searches
        if len(self.preload_data) < first_post + query_limit:
            self.latest_page += 1
            while self.do_preload(self.latest_page) and len(self.preload_data) < first_post + query_limit:
                self.latest_page += 1

        # Parse minimum needed API responses
        self.do_load_urls(first_post + query_limit)

        # Return complete data
        for i in range(first_post, min(first_post + query_limit, len(self.preload_data))):
            item_data = {'rating': 's',
                         'score': 0,
                         'fav_count': 0,
                         'image_height': 0,
                         'image_width': 0,
                         'file_size': 0,
                         'tag_string': self.preload_tag,
                         'tag_string_artist': '',
                         'tag_string_character': '',
                         'tag_string_copyright': '',
                         'tag_string_general': self.preload_tag,
                         'tag_string_meta': '',
                         'created_at': '2022-03-01T13:35:13.654-05:00',
                         'updated_at': '2022-03-01T13:35:13.654-05:00',
                         'source': '',
                         'preview_file_url': self.preload_data[i][0],
                         'large_file_url': self.preload_data[i][1],
                         'file_url': self.preload_data[i][1],
                         'id': i
                        }
            item_list.append(item_data)

        return item_list

    def do_preload(self, page_number):
        # Build site and search URL
        site_url = 'https://'
        search_url = 'https://'
        if self.preload_tag.startswith('ecchi'):
            site_url += 'ecchi.iwara.tv'
            search_url += 'ecchi.iwara.tv/search'
            search_url += '?query='
            search_url += self.preload_tag[len('ecchi '):].replace(' ', '+')
        else:
            site_url += 'www.iwara.tv'
            search_url += 'www.iwara.tv/search'
            search_url += '?query='
            search_url += self.preload_tag.replace(' ', '+')
        search_url += '&page='
        search_url += str(page_number)

        # Parse response
        with urllib.request.urlopen(search_url) as search_response:
            search_html = search_response.read().decode('utf-8')
            thumbnail_marker = '<img src="//i.iwara.tv/sites/default/files/styles/thumbnail/public/videos/thumbnails/'
            video_marker = '<a href="/videos/'

            thumbnail_idx = search_html.find(thumbnail_marker, 0)
            if thumbnail_idx == -1:
                return False

            while thumbnail_idx != -1:
                thumbnail_end_idx = search_html.find('"', thumbnail_idx+len(thumbnail_marker))
                thumbnail_url = 'https:' + search_html[thumbnail_idx+len('<img src="'):thumbnail_end_idx]

                video_idx = search_html.find(video_marker, thumbnail_end_idx+1)
                video_end_idx = search_html.find('"', video_idx+len(video_marker))
                video_api_url = site_url + '/api/video/' + search_html[video_idx+len('<a href="/videos/'):video_end_idx]

                print(video_api_url + ' - ' + thumbnail_url + ' - ' + 'URL not loaded')
                self.preload_data.append([thumbnail_url, None, video_api_url])

                thumbnail_idx = search_html.find(thumbnail_marker, video_end_idx+1)
            return True

    def do_load_urls(self, max_video_id):
        for i in range(0, max_video_id):
            if self.preload_data[i][1] is None:
                # Query API for video URL
                video_api_url = self.preload_data[i][2]
                thumbnail_url = self.preload_data[i][0]
                video_real_url = 'https:'
                try:
                    with urllib.request.urlopen(video_api_url) as video_api_response:
                        print('Opening ' + video_api_url)
                        video_api_data = json.loads(video_api_response.read().decode('utf-8'))
                        video_real_url += video_api_data[0]['uri'] + '&.mp4'

                    print(video_api_url + ' - ' + thumbnail_url + ' - ' + video_real_url)
                    self.preload_data[i][1] = video_real_url
                except:
                    print('Bad structure.')

    def handle(self, caller):
        pass
