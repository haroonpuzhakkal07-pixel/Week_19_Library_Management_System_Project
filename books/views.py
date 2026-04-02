from rest_framework import viewsets
from .models import Book, BorrowRecord
from .serializers import BookSerializer, BorrowRecordSerializer, RegisterSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

# Create your views here.

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User Created Successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def borrow_book(request, book_id):
    user = request.user
    book = get_object_or_404(Book, id=book_id)

    # Check Availability
    if not book.available:
        return Response(
            {'error': 'Book is not available'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Create Borrow Record
    BorrowRecord.objects.create(user=user, book=book)
    # Mark Book Unavailable
    book.available = False
    book.save()
    return Response({'Message': 'Book borrowed succesfully'})
    
@api_view(['POST'])
def return_book(request, book_id):
    user = request.user
    book = get_object_or_404(Book, id=book_id)
    # Find Active Borrow Record
    record = BorrowRecord.objects.filter(
        user=user,
        book=book,
        returned=False
    ).first()
    
    if not record:
        return Response(
            {'error': 'No active borrow record found'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Mark as returned
    record.returned = True
    record.save()

    # Make book available again
    book.available = True
    book.save()

    return Response(
        {'message': 'Book returned successfully'}
    )