#!/usr/bin/env python3

import os

class FileWrapper:
    def __init__(self, local_dir):
        self.dir_path = local_dir
        self.dir_list = [f for f in os.listdir(local_dir) if os.path.isfile(os.path.join(local_dir, f))]

    def get_batch(self, current_tag, query_page, query_limit, first_post, caller):
        item_list = []

        for i in range(first_post, min(first_post + query_limit, len(self.dir_list))):
            host_address = caller.headers['Host']
            item_fn = self.dir_list[i]
            item_url = 'http://' + host_address + '/plugin/s:f/' + str(i) + item_fn[item_fn.rfind('.'):]
            item_data = {'rating': 's',
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
                         'preview_file_url': item_url,
                         'large_file_url': item_url,
                         'file_url': item_url,
                         'id': i
                        }
            item_list.append(item_data)

        return item_list

    def handle(self, caller):
        file_id = int(caller.path[len('/plugin/s:f/'):caller.path.rfind('.')])

        caller.send_response(200)
        caller.send_header('Content-type', 'application/octet-stream')
        caller.end_headers()
        f = open(os.path.join(self.dir_path, self.dir_list[file_id]), 'rb')
        caller.wfile.write(f.read())
        f.close()
