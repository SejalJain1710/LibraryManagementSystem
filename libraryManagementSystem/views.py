from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BookCopy, Book, CustomUser, Transaction
from .serializer import BookSerializer, BookCopySerializer, CustomUserSerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsLibrarian

class BookAddView(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            quantity = request.data.get('quantity', 1)

            if not isinstance(quantity, int) or quantity <= 0:
                return Response({"error": "Number of copies must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookUpdateView(APIView):
    def patch(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = BookCopy.objects.prefetch_related('book').all()
        serializer = BookCopySerializer(queryset, many=True)
        return Response(serializer.data)

class BookDetailView(APIView):
    def get(self, request, book_id):
        queryset = Book.objects.get(id=book_id)
        serializer = BookSerializer(queryset)
        return Response(serializer.data)
    
class BookDeleteView(APIView):

    # permission_classes = [IsAuthenticated, IsLibrarian]
    def delete(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            book.delete()  # This will cascade delete all related BookCopy instances
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Book and its copies deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        
class BookCopyDeleteView(APIView):
    def delete(self, request, copy_id):
        try:
            book_copy = BookCopy.objects.get(id=copy_id)
            book_copy.delete()
        except BookCopy.DoesNotExist:
            return Response({"error": "Book copy not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Book copy deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class BookCopyAddView(APIView):
    def post(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        additional_quantity = request.data.get('quantity', 0)
        if additional_quantity <= 0:
            return Response({"error": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

        book_copy_serializer = BookCopySerializer()
        copies_created = book_copy_serializer.create_copies(book, additional_quantity)

        return Response({"message": f"{additional_quantity} copies added.", "copies": [{"copy_number": copy.copy_number} for copy in copies_created]}, status=status.HTTP_201_CREATED)
    
class UserAddView(APIView):
    def post(self, request):        
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDeleteView(APIView):
    def delete(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        user.is_active = False
        user.save()
        return Response({"message": "User deactivated successfully."}, status=status.HTTP_200_OK)
        
class UserUpdateView(APIView):
    def patch(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)
    
class UserDetailView(APIView):
    def get(self, request, user_id):
        queryset = CustomUser.objects.get(id=user_id)
        serializer = CustomUserSerializer(queryset)
        return Response(serializer.data)
    
class ActiveUserListView(APIView):
    def get(self, request):
        users = CustomUser.objects.filter(is_active=True)
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    
class UserHistoryView(APIView):
    def get(self, request, user_id):
        transaction = Transaction.objects.filter(issued_to=user_id)
        serializer = TransactionSerializer(transaction, many=True)
        return Response(serializer.data)

class BookIssueView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookReturnView(APIView):
    def patch(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)
       
        serializer = TransactionSerializer(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
