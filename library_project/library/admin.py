from django.contrib import admin
from .models import Book, Author, Loan, Category
from django.utils import timezone
from django.contrib import admin



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'books_count')
    search_fields = ('name',)

    def books_count(self, obj):
        return obj.books.count()

    books_count.short_description = "Nombre de livres"

class BookInline(admin.TabularInline):
    model = Book
    extra = 0
    readonly_fields = ('title', 'isbn')
    can_delete = False


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'nationality', 'birth_date')
    search_fields = ('first_name', 'last_name')
    list_filter = ('nationality',)
    inlines = [BookInline]

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    full_name.short_description = "Nom complet"

class LoanInline(admin.TabularInline):
    model = Loan
    extra = 0
    readonly_fields = ('borrower_name', 'borrowed_at', 'status')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'isbn',
        'category',
        'available_copies',
    )

    list_filter = ('category', 'author', 'publication_year')
    search_fields = ('title', 'isbn', 'author__last_name')
    inlines = [LoanInline]

    readonly_fields = ('created_at',)

    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'isbn', 'author', 'category')
        }),
        ('Publication', {
            'fields': ('publication_year', 'publisher', 'language', 'pages')
        }),
        ('Stock', {
            'fields': ('total_copies', 'available_copies')
        }),
        ('Description', {
            'fields': ('description', 'cover_image')
        }),
        ('Métadonnées', {
            'fields': ('created_at',)
        }),
    )

    actions = ['mark_unavailable']

    def mark_unavailable(self, request, queryset):
        queryset.update(available_copies=0)

    mark_unavailable.short_description = "Marquer comme indisponible"

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        'book',
        'borrower_name',
        'borrowed_at',
        'due_date',
        'status',
        'is_overdue',
    )

    list_filter = ('status', 'borrowed_at')
    search_fields = ('borrower_name', 'borrower_email', 'card_number')

    actions = ['mark_returned']

    def mark_returned(self, request, queryset):
        for loan in queryset:
            loan.status = 'RETURNED'
            loan.returned_at = timezone.now()
            loan.book.increment_copies()
            loan.save()

    mark_returned.short_description = "Marquer comme retourné"

    def is_overdue(self, obj):
        return obj.returned_at is None and obj.due_date < timezone.now().date()

    is_overdue.boolean = True
    is_overdue.short_description = "En retard"

admin.site.site_header = "Administration de la Bibliothèque"
admin.site.site_title = "Bibliothèque"
admin.site.index_title = "Gestion du catalogue"
