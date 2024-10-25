from rest_framework import serializers

from .models import Book
from .schemas import BookCreate, BookResponse


class PydanticModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """Convert the model instance to Pydantic response schema"""
        response = BookResponse.model_validate(instance)
        return response.model_dump()

    def to_internal_value(self, data):
        """Validate input data using Pydantic create schema"""
        try:
            validated_data = BookCreate(**data)
            return validated_data.model_dump()
        except ValueError as e:
            raise serializers.ValidationError(str(e))


class BookSerializer(PydanticModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "year", "category", "language"]
