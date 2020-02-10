import sqlite3
from django.shortcuts import render
from libraryapp.models import Library
from ..connection import Connection


def list_libraries(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                b.id,
                b.title,
                b.address,
                b.librarian_id,
            from libraryapp_library b
            """)

            all_libraries = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                library = Library()
                library.id = row['id']
                library.title = row['title']
                library.address = row['address']
                library.librarian_id = row['librarian_id']

                all_libraries.append(library)

        template = 'libraries/list.html'
        context = {
            'all_libraries': all_libraries
        }

        return render(request, template, context)