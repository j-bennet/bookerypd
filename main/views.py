from typing import Any

from django.db.models import QuerySet
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.request import Request

from .models import Book
from .schemas import BookCreate, BookResponse


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    Supports filtering by category, author, or language using query parameters.
    Example: /books/?category=Fiction&author=John Doe&language=en
    """

    # pylint: disable=no-member
    queryset: QuerySet[Book] = Book.objects.all()

    def get_queryset(self) -> QuerySet[Book]:
        queryset = self.queryset

        # Type ignore comments below are safe because DRF's Request includes query_params
        category = self.request.query_params.get("category", None)  # type: ignore
        author = self.request.query_params.get("author", None)  # type: ignore
        language = self.request.query_params.get("language", None)  # type: ignore

        if category:
            queryset = queryset.filter(category=category)
        if author:
            queryset = queryset.filter(author=author)
        if language:
            queryset = queryset.filter(language=language)

        return queryset

    def create(self, request: Request, *args: Any, **kwargs: Any) -> JsonResponse:
        try:
            # Validate input data using Pydantic
            book_data = BookCreate(**request.data)

            # Create book instance
            book = Book.objects.create(**book_data.model_dump())  # pylint: disable=no-member

            # Return response using Pydantic response model
            response = BookResponse.model_validate(book)
            return JsonResponse(response.model_dump(), status=201)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> JsonResponse:
        queryset = self.get_queryset()
        books = [BookResponse.model_validate(book) for book in queryset]
        return JsonResponse([book.model_dump() for book in books], safe=False)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> JsonResponse:
        book = self.get_object()
        response = BookResponse.model_validate(book)
        return JsonResponse(response.model_dump())

    def update(self, request: Request, *args: Any, **kwargs: Any) -> JsonResponse:
        try:
            book = self.get_object()
            book_data = BookCreate(**request.data)

            for key, value in book_data.model_dump().items():
                setattr(book, key, value)
            book.save()

            response = BookResponse.model_validate(book)
            return JsonResponse(response.model_dump())
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

    def partial_update(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        try:
            book = self.get_object()
            # For partial updates, exclude_unset=True to only update provided fields
            book_data = BookCreate(**request.data, exclude_unset=True)

            for key, value in book_data.model_dump(exclude_unset=True).items():
                setattr(book, key, value)
            book.save()

            response = BookResponse.model_validate(book)
            return JsonResponse(response.model_dump())
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
