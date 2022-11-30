from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets

from book.models import Book
from book.permissions import IsAdminOrIfNotReadOnly
from book.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrIfNotReadOnly, )

    def get_queryset(self):
        """Retrieve the movies with filters"""
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if author:
            queryset = queryset.filter(author__icontains=author)

        return queryset.distinct()

    # For documentation purposes
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                type=str,
                description="Filter by book title ex.(?title='Harry Potter')",
            ),
            OpenApiParameter(
                "author",
                type=str,
                description="Filter by book author ex.(?title='J. K. Rowling')",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super(BookViewSet, self).list(request, *args, **kwargs)
