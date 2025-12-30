from django.core.management.base import BaseCommand
from library.models import Category, Author, Book, Loan
from django.utils import timezone
import random
from datetime import date


def random_isbn(n):
    return ''.join(str((n + i) % 10) for i in range(13))


class Command(BaseCommand):
    help = 'Seed database with sample categories, authors, books and loans'

    def add_arguments(self, parser):
        parser.add_argument('--books', type=int, default=3, help='Number of books to create')
        parser.add_argument('--authors', type=int, default=5, help='Number of authors to create')

    def handle(self, *args, **options):
        count_books = options['books']
        count_authors = options['authors']

        self.stdout.write(f'Seeding database: {count_authors} authors, {count_books} books...')

        # Ensure categories
        default_cats = [
            ('fiction', 'Fiction générale'),
            ('sci-fi', 'Science Fiction'),
            ('history', 'Histoire'),
            ('programming', 'Informatique'),
        ]
        categories = []
        for slug, name in default_cats:
            obj, _ = Category.objects.get_or_create(name=slug, defaults={'description': name})
            categories.append(obj)

        # Create authors
        first_names = ['Jean', 'Marie', 'Paul', 'Luc', 'Anne', 'Pierre', 'Sofia', 'Marco', 'Lina', 'Omar']
        last_names = ['Dupont', 'Martin', 'Bernard', 'Durand', 'Petit', 'Leroy', 'Moreau', 'Rossi', 'Garcia', 'Khan']
        authors = []
        for i in range(count_authors):
            fn = random.choice(first_names)
            ln = random.choice(last_names)
            bd = date(1950 + random.randint(0, 50), random.randint(1, 12), random.randint(1, 28))
            obj, _ = Author.objects.get_or_create(first_name=fn, last_name=ln, defaults={'birth_date': bd, 'nationality': 'FR'})
            authors.append(obj)

        # Create books
        for i in range(count_books):
            title = f'Livre Exemple {i+1}'
            isbn = random_isbn(i+1)
            author = random.choice(authors) if authors else None
            category = random.choice(categories)
            pub_year = random.randint(1950, timezone.now().year)
            defaults = {
                'title': title,
                'publication_year': pub_year,
                'author': author,
                'category': category,
                'total_copies': random.randint(1, 10),
                'available_copies': random.randint(0, 5),
                'language': random.choice(['fr', 'en']),
                'pages': random.randint(50, 1000),
                'publisher': random.choice(['Penguin', 'Gallimard', 'O Reilly', 'Springer']),
            }
            Book.objects.get_or_create(isbn=isbn, defaults=defaults)

        # Optionally create a couple of loans
        book = Book.objects.first()
        if book:
            Loan.objects.get_or_create(book=book, card_number='CARD123', defaults={'borrower_name': 'Test User', 'borrower_email': 'test@example.com', 'due_date': timezone.now().date() + timezone.timedelta(days=14), 'status': 'ACTIVE'})

        self.stdout.write(self.style.SUCCESS('Seeding completed.'))
