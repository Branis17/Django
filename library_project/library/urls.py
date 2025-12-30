from django.urls import path, include
from . import views

app_name = 'library'

# Books
books_patterns = ([
	path('', views.book_list, name='list'),
	path('page/<int:page>/', views.book_list, name='list_page'),
	path('search/', views.book_search, name='search'),
	path('category/<slug:category_slug>/', views.books_by_category, name='by_category'),
	path('author/<int:author_id>/', views.books_by_author, name='by_author'),
	path('<int:pk>/', views.book_detail, name='detail'),
], 'books')

# Authors
authors_patterns = ([
	path('', views.author_list, name='list'),
	path('search/', views.author_search, name='search'),
	path('<int:pk>/', views.author_detail, name='detail'),
], 'authors')

# Loans
loans_patterns = ([
	path('active/', views.loans_active, name='active'),
	path('overdue/', views.loans_overdue, name='overdue'),
	path('user/<int:user_id>/', views.loans_user_history, name='user_history'),
	path('create/', views.loan_create, name='create'),
	path('return/<int:loan_id>/', views.loan_return, name='return'),
], 'loans')

# Pages
pages_patterns = ([
	path('', views.home, name='home'),
	path('about/', views.about, name='about'),
	path('contact/', views.contact, name='contact'),
], 'pages')

urlpatterns = [
	path('books/', include((books_patterns[0], books_patterns[1]), namespace='books')),
	path('authors/', include((authors_patterns[0], authors_patterns[1]), namespace='authors')),
	path('loans/', include((loans_patterns[0], loans_patterns[1]), namespace='loans')),
	path('', include((pages_patterns[0], pages_patterns[1]), namespace='pages')),
]
