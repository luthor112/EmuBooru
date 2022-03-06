#!/usr/bin/env python3

from concurrent.futures.thread import ThreadPoolExecutor
import json
import urllib.request

class ChobitWrapper:
    def __init__(self):
        self.preload_tag = '_placeholder_'
        self.preload_data = []
        self.latest_page = 0

    def get_batch(self, current_tag, query_page, query_limit, first_post, caller):
        item_list = []

        # Check if new search needs to be conducted
        wanted_tag = current_tag.replace('%20', ' ').replace('+', ' ')
        if self.preload_tag != wanted_tag:
            self.preload_tag = wanted_tag
            self.preload_data = []
            self.latest_page = 0

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
        site_url = 'https://chobit.cc/'
        search_url = 'https://chobit.cc/s?f_category='
        if self.preload_tag.startswith('c:vid'):
            search_url += 'vd'
            search_url += '&q_keyword='
            search_url += self.preload_tag[len('c:vid '):].replace(' ', '+')
        elif self.preload_tag.startswith('c:v3d'):
            search_url += 'vd_3d'
            search_url += '&q_keyword='
            search_url += self.preload_tag[len('c:v3d '):].replace(' ', '+')
        else:
            search_url += '&q_keyword='
            search_url += self.preload_tag.replace(' ', '+')
        search_url += '&s_page='
        search_url += str(page_number)

        # Parse response
        with urllib.request.urlopen(search_url) as search_response:
            search_html = search_response.read().decode('utf-8')
            thumbnail_marker = '<img src="https://media.dlsite.com/chobit/contents/'
            video_marker = '<a href="/'

            thumbnail_idx = search_html.find(thumbnail_marker, 0)
            if thumbnail_idx == -1:
                return False

            while thumbnail_idx != -1:
                thumbnail_end_idx = search_html.find('"', thumbnail_idx+len(thumbnail_marker))
                thumbnail_url = search_html[thumbnail_idx+len('<img src="'):thumbnail_end_idx]

                video_idx = search_html.rfind(video_marker, 0, thumbnail_idx)
                video_end_idx = search_html.find('"', video_idx+len(video_marker))
                video_api_url = site_url + search_html[video_idx+len(video_marker):video_end_idx]

                print(video_api_url + ' - ' + thumbnail_url + ' - ' + 'URL not loaded')
                self.preload_data.append([thumbnail_url, None, video_api_url])

                thumbnail_idx = search_html.find(thumbnail_marker, thumbnail_end_idx+1)
            return True

    def do_load_urls(self, max_video_id):
        with ThreadPoolExecutor(max_workers=4) as executor:
            for i in range(0, min(max_video_id, len(self.preload_data))):
                if self.preload_data[i][1] is None:
                    executor.submit(self.do_load_single_url, i)

    def do_load_single_url(self, video_id):
        # Query site for video URL
        video_page_url = self.preload_data[video_id][2]
        thumbnail_url = self.preload_data[video_id][0]

        try:
            with urllib.request.urlopen(video_page_url) as video_page_response:
                print('Opening ' + video_page_url)
                video_page_html = video_page_response.read().decode('utf-8')
                video_marker = '<meta itemprop="contentUrl" content="'

                video_url_idx = video_page_html.find(video_marker, 0)
                video_url_end_idx = video_page_html.find('"', video_url_idx+len(video_marker))
                video_url = video_page_html[video_url_idx+len(video_marker):video_url_end_idx]

                print(video_page_url + ' - ' + thumbnail_url + ' - ' + video_url)
                self.preload_data[video_id][1] = video_url
        except:
            print('Bad structure.')

    def handle(self, caller):
        pass
