from django.db import models
from django.urls import reverse
import uuid  # required for unique book instances


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200,
        help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Book(models.Model):
    """Model representing a specific book(not a specific copy)"""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author,
    # but authors can have multiple books
    # Author as a string rather than object
    # because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(
        max_length=1000,
        help_text="Enter a brief decription of the book")
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        help_text="13 Character <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>")

    # ManyToManyField used because genre can contain many books.
    # Books can cover many genres.
    # Genre class has already been defined
    # so we can specify the object above.
    genre = models.ManyToManyField(
        Genre,
        help_text="Select a genre for this book")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String representation of the Book model"""
        return self.title

    def get_absolute_url(self):
        """Return the url to access detail record for each book"""
        return reverse('book-detail', args=[self.id])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model to represent the specific copy of book
    (ie that can be borrowed from the library)"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for particular book across whole library")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text="Book Availability"
        )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing object"""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name} {self.last_name}'


class Language(models.Model):
    """Model representing the different languages"""
    name=models.CharField(
        max_length=50,
        help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)",
        )

    def __str__(self):
        return f'{self.name}'
