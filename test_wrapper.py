#!/usr/bin/env python3

class TestWrapper:
    def get_batch(self, query_page, query_limit, first_post):
        if first_post == 0:
            test_data = [{'a': 'b',
                          'c': 4}]
            return test_data
        else:
            return []
