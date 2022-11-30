# from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from book.models import Book
from book.serializers import BookSerializer, BookCreateSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the movies with filters"""
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")
        inventory = self.request.query_params.get("inventory")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if author:
            queryset = queryset.filter(author__icontains=author)

        if inventory:
            queryset = queryset.filter(inventory=inventory)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "create":
            return BookCreateSerializer
        return BookSerializer

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
