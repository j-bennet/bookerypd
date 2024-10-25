from rest_framework import generics, mixins

from .models import Book
from .serializers import BookSerializer


class BookList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    API endpoint that allows books to be viewed or created.
    Supports:
    - Filtering by category, author, or language using query parameters
      Example: /books/?category=Fiction&author=John Doe&language=en
    - Text search in title and author fields using 'search' parameter
      Example: /books/?search=harry potter
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_fields = ["category", "language", "author"]
    search_fields = ["title", "author"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    API endpoint that allows a specific book to be retrieved, updated, or deleted.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
