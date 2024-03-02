def make_pagination_range(page_range=list(range(1, 21)), qty_paginas=4, current_page=1):
    if (current_page < 4):
        return list(range(1, 10))
    return [1, 2, 3, 4]
