import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from http.server import HTTPServer, SimpleHTTPRequestHandler

with open('books/meta_data.json', 'r', encoding="UTF-8") as meta_data:
    books_json = meta_data.read()


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    books = json.loads(books_json)
    rendered_page = template.render(books=books)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
