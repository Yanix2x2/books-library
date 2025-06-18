import os
import json
from pprint import pprint
import math

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

with open('books/meta_data.json', 'r', encoding="UTF-8") as meta_data:
    books_json = meta_data.read()


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    books = json.loads(books_json)

    os.makedirs('pages', exist_ok=True)

    books_per_page = 20
    pages = list(chunked(books, books_per_page))
    page_amount = math.ceil(len(books) / books_per_page)
    for page_num, books_chunk in enumerate(pages, start=1):
        page = list(chunked(books_chunk, 2))
        rendered_page = template.render(
            books=page,
            page_number=page_num,
            page_amount=page_amount
        )

        filename = os.path.join('pages', f'index{page_num}.html')
        with open(filename, 'w', encoding='utf8') as file:
            file.write(rendered_page)


server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')

if __name__ == '__main__':
    on_reload()
