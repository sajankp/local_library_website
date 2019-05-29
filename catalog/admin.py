from django.contrib import admin

from catalog.models import Author, Genre, Book, BookInstance ,Language

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)

# Define the admin class
class BookInline(admin.TabularInline):
    model = Book
    extra = 0
    # fields = ['title', 'isbn','genre']
    exclude = ['summary']
    def has_change_permission(self,request, obj=None):
        return False

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

admin.site.register(Author, AuthorAdmin)


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
    def has_change_permission(self,request, obj=None):
        return False


# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ("book","status","id","due_back")
    fieldsets = (
        (None,{
            'fields':('book','imprint','id')
        }),
        ("Availability",{
            'fields':("status", "due_back")
        })
    )
