from rest_framework import viewsets

from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    Supports filtering by category, author, or language using query parameters.
    Example: /books/?category=Fiction&author=John Doe&language=en
    """

    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()

        category = self.request.query_params.get("category", None)
        author = self.request.query_params.get("author", None)
        language = self.request.query_params.get("language", None)

        if category:
            queryset = queryset.filter(category=category)
        if author:
            queryset = queryset.filter(author=author)
        if language:
            queryset = queryset.filter(language=language)

        return queryset
