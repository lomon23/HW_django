from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Book
from ..serializers import BookSerializer
from ..permissions import IsAdminUser, IsManagerUser
import json

# API v1 using Django standard views
class BookListView(View):
    def get(self, request):
        books = Book.objects.all()
        data = [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': str(book.price),
            'inventory': book.inventory
        } for book in books]
        return JsonResponse(data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        book = Book.objects.create(
            title=data['title'],
            author=data['author'],
            price=data['price'],
            inventory=data['inventory']
        )
        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': str(book.price),
            'inventory': book.inventory
        }, status=201)

class BookDetailView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': str(book.price),
            'inventory': book.inventory
        })

    def delete(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return JsonResponse({}, status=204)

    def patch(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        data = json.loads(request.body)
        
        for key, value in data.items():
            setattr(book, key, value)
        book.save()

        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': str(book.price),
            'inventory': book.inventory
        })

# API v2 using DRF
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated, IsManagerUser]
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        book = self.get_object()
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        book = self.get_object()
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, pk=None):
        book = self.get_object()
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)