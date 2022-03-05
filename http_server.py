#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

# Config
from file_wrapper import FileWrapper
from iwara_wrapper import IwaraWrapper
from test_wrapper import TestWrapper
data_wrapper = FileWrapper('/mnt/e/MEGA/Pictures')

current_tag = ''
current_list = []

class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global current_tag
        global current_list
        global data_wrapper

        # Parse path
        parsed_url = urlparse(self.path)
        parsed_query = parse_qs(parsed_url.query)

        if parsed_url.path == '/posts.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()

            # Interpret query
            new_tag = ''
            if 'tags' in parsed_query:
                new_tag = parsed_query['tags'][0]
            query_page = int(parsed_query['page'][0])
            query_limit = int(parsed_query['limit'][0])
            first_post = (query_page - 1) * query_limit

            if current_tag != new_tag:
                print("New tag, purging list...")
                current_tag = new_tag
                current_list = []

            # Extend list if needed
            if len(current_list) < query_page * query_limit:
                current_list += data_wrapper.get_batch(current_tag, query_page, query_limit, first_post, self)

            # Send back results
            self.wfile.write(json.dumps(current_list[first_post:first_post+query_limit]).encode('utf-8'))
        elif parsed_url.path.startswith('/plugin/'):
            data_wrapper.handle(self)

if __name__ == '__main__':
    server_address = ('', 80)
    httpd = HTTPServer(server_address, CustomHandler)
    try:
        print("Starting server...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    print("Stopping server...")
    httpd.server_close()
