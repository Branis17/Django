from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, Author, Category, Loan


def home(request):
	return render(request, 'library/home.html')


def about(request):
	return HttpResponse("À propos")


def contact(request):
	return HttpResponse("Contact")


def book_list(request, page: int = 1):
	# simple listing stub — later replace with pagination and template
	books = Book.objects.all()[:50]
	titles = ', '.join([b.title for b in books])
	return HttpResponse(f"Liste des livres (page {page}): {titles}")


def book_detail(request, pk: int):
	book = get_object_or_404(Book, pk=pk)
	return HttpResponse(f"Détail du livre #{book.pk} — {book.title}")


def book_search(request):
	q = request.GET.get('q', '')
	results = Book.objects.filter(title__icontains=q)[:20]
	titles = ', '.join([b.title for b in results])
	return HttpResponse(f"Recherche livres '{q}': {titles}")


def books_by_category(request, category_slug: str):
	cat = get_object_or_404(Category, name=category_slug)
	books = cat.books.all()[:50]
	titles = ', '.join([b.title for b in books])
	return HttpResponse(f"Livres dans la catégorie {cat.name}: {titles}")


def books_by_author(request, author_id: int):
	author = get_object_or_404(Author, pk=author_id)
	books = author.books.all()[:50]
	titles = ', '.join([b.title for b in books])
	return HttpResponse(f"Livres de {author}: {titles}")


def author_list(request):
	authors = Author.objects.all()[:50]
	names = ', '.join([str(a) for a in authors])
	return HttpResponse(f"Liste des auteurs: {names}")


def author_detail(request, pk: int):
	author = get_object_or_404(Author, pk=pk)
	books = author.books.all()[:20]
	titles = ', '.join([b.title for b in books])
	return HttpResponse(f"Détail auteur {author}: {titles}")


def author_search(request):
	q = request.GET.get('q', '')
	results = Author.objects.filter(first_name__icontains=q) | Author.objects.filter(last_name__icontains=q)
	names = ', '.join([str(a) for a in results[:20]])
	return HttpResponse(f"Recherche auteurs '{q}': {names}")


def loans_active(request):
	loans = Loan.objects.filter(status='ACTIVE')[:50]
	items = ', '.join([str(l) for l in loans])
	return HttpResponse(f"Emprunts actifs: {items}")


def loans_overdue(request):
	loans = Loan.objects.filter(status='OVERDUE')[:50]
	items = ', '.join([str(l) for l in loans])
	return HttpResponse(f"Emprunts en retard: {items}")


def loans_user_history(request, user_id: int):
	loans = Loan.objects.filter(card_number=user_id)[:100]
	items = ', '.join([str(l) for l in loans])
	return HttpResponse(f"Historique emprunts pour {user_id}: {items}")


def loan_create(request):
	return HttpResponse("Formulaire de création d'emprunt (stub)")


def loan_return(request, loan_id: int):
	return HttpResponse(f"Formulaire de retour pour emprunt {loan_id} (stub)")
