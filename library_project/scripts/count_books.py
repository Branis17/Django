import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()
from library.models import Book

print('books_count', Book.objects.count())
for b in Book.objects.all()[:10]:
    print(b.pk, b.title, b.isbn)
