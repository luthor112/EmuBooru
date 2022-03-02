#!/usr/bin/env python3

from copy import copy

class TestWrapper:
    def get_batch(self, current_tag, query_page, query_limit, first_post):
        if first_post == 0:
            test_data = {'rating': 's',
                         'score': 0,
                         'fav_count': 0,
                         'image_height': 0,
                         'image_width': 0,
                         'file_size': 0,
                         'tag_string': '',
                         'tag_string_artist': '',
                         'tag_string_character': '',
                         'tag_string_copyright': '',
                         'tag_string_general': '',
                         'tag_string_meta': '',
                         'created_at': '2022-03-01T13:35:13.654-05:00',
                         'updated_at': '2022-03-01T13:35:13.654-05:00',
                         'source': '',
                         'preview_file_url': 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_light_color_272x92dp.png',
                         'large_file_url': 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_light_color_272x92dp.png',
                         'file_url': 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_light_color_272x92dp.png',
                         'id': 0
                        }

            test_data_b = copy(test_data)
            test_data_b['id'] = 1

            test_data_c = copy(test_data)
            test_data_c['id'] = 2

            return [test_data, test_data_b, test_data_c]
        else:
            return []

    def handle(self, caller):
        pass
