from datetime import datetime

from pydantic import BaseModel, Field

from .models import CATEGORIES, LANGUAGES


class BookBase(BaseModel):
    title: str = Field(..., max_length=100)
    author: str = Field(..., max_length=100)
    year: int | None = None
    category: str = Field(default="Fiction", max_length=100)
    language: str = Field(default="en", max_length=100)

    @property
    def category_choices(self):
        return [cat[0] for cat in CATEGORIES]

    @property
    def language_choices(self):
        return [lang[0] for lang in LANGUAGES]

    def validate_category(self, value):
        if value not in self.category_choices:
            raise ValueError(f"Category must be one of {self.category_choices}")
        return value

    def validate_language(self, value):
        if value not in self.language_choices:
            raise ValueError(f"Language must be one of {self.language_choices}")
        return value


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    created: datetime

    class Config:
        from_attributes = True
