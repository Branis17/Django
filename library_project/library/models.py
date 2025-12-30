from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    death_date = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100)
    biography = models.TextField(blank=True)
    website = models.URLField(blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)

    class Meta:
        unique_together = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)

    publication_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1450),
            MaxValueValidator(timezone.now().year)
        ]
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name='books'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='books'
    )

    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()

    description = models.TextField(blank=True)
    language = models.CharField(max_length=50)
    pages = models.PositiveIntegerField()
    publisher = models.CharField(max_length=200)

    cover_image = models.ImageField(upload_to='books/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def clean(self):
        if self.available_copies > self.total_copies:
            raise ValidationError(
                "Les exemplaires disponibles ne peuvent pas dépasser le total."
            )

    def is_available(self):
        return self.available_copies > 0

    def decrement_copies(self):
        if not self.is_available():
            raise ValidationError("Aucun exemplaire disponible.")
        self.available_copies -= 1
        self.save()

    def increment_copies(self):
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            self.save()


class Loan(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Actif'),
        ('RETURNED', 'Retourné'),
        ('OVERDUE', 'En retard'),
    ]

    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
        related_name='loans'
    )

    borrower_name = models.CharField(max_length=200)
    borrower_email = models.EmailField()
    card_number = models.CharField(max_length=50)

    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateTimeField(blank=True, null=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.book.title} - {self.borrower_name}"

    def save(self, *args, **kwargs):
        if not self.pk:
            active_loans = Loan.objects.filter(
                card_number=self.card_number,
                status='ACTIVE'
            ).count()

            if active_loans >= 5:
                raise ValidationError("Limite de 5 emprunts atteinte.")

            if not self.book.is_available():
                raise ValidationError("Livre indisponible.")

            self.due_date = timezone.now().date() + timezone.timedelta(days=14)
            self.book.decrement_copies()

        super().save(*args, **kwargs)
