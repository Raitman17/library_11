from rest_framework import serializers
from .models import Book, Genre, Author

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description',
            'volume', 'type', 'year',
            'created', 'modified',
        ]

class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'id', 'name', 'description',
            'created', 'modified',
        ]

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id', 'full_name',
            'created', 'modified',
        ]