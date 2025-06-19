import os
import json
import math
import argparse

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
from dotenv import load_dotenv


def on_reload(books):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    os.makedirs('pages', exist_ok=True)

    books_per_page = 20
    columns = 2
    pages = list(chunked(books, books_per_page))
    page_amount = math.ceil(len(books) / books_per_page)
    for page_num, books_chunk in enumerate(pages, start=1):
        page = list(chunked(books_chunk, columns))
        rendered_page = template.render(
            books=page,
            page_number=page_num,
            page_amount=page_amount
        )

        filename = os.path.join('pages', f'index{page_num}.html')
        with open(filename, 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--path', 
        help='Путь до json файла', 
        default=os.getenv('BOOKS_PATH', 'media/meta_data.json')
    )
    args = parser.parse_args()

    with open(args.path, 'r', encoding="UTF-8") as file:
        books = json.load(file)

    on_reload(books)

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
