from datetime import timedelta
import uuid
from rest_framework import serializers
from .models import *

class BookCopySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='book.name', read_only=True)
    book_id = serializers.IntegerField(source='book.id', read_only=True)
    copy_id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = BookCopy
        fields = ['name','status', 'copy_number', 'book_id', 'copy_id']

    def create_copies(self, book, quantity):
        if quantity <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        
        copies_created = []
        for _ in range(quantity):
            copy_number = f"{book.isbn}-{uuid.uuid4()}"
            book_copy = BookCopy.objects.create(book=book, copy_number=copy_number)
            copies_created.append(book_copy)

        return copies_created

class BookSerializer(serializers.ModelSerializer):
    copy = BookCopySerializer(many=True, read_only=True) 
    quantity = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'isbn', 'quantity', 'copy']

    def validate_isbn(self, value):
        # For update: make ISBN read-only by raising a validation error if an attempt to update it is made
        if self.instance:
            if self.instance.isbn != value:
                raise serializers.ValidationError("ISBN cannot be updated.")
        else: # For create: check if a book with the same ISBN already exists
            if Book.objects.filter(isbn=value).exists():
                raise serializers.ValidationError("A book with this ISBN already exists.")
        return value
    def create(self, validated_data):
        quantity = validated_data.pop('quantity')
        existing_book = Book.objects.filter(isbn=validated_data['isbn']).first()
        if existing_book:
            raise serializers.ValidationError("A book with this ISBN already exists. Details: " + str(existing_book))
    
        book = Book.objects.create(**validated_data)

        book_copy_serializer = BookCopySerializer()
        book_copy_serializer.create_copies(book, quantity)

        return book

    def to_representation(self, instance):
        """Custom method to represent the response."""
        data = super().to_representation(instance)
        data['copies'] = BookCopySerializer(instance.bookcopy_set.all(), many=True).data
        return data
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        date_due = validated_data.get('date_due', None)
        date_issued = validated_data.get('date_issued')
        if date_due and date_due > date_issued:
            return Transaction.objects.create(**validated_data)
        date_due = date_issued + timedelta(days=180)
        validated_data['date_due'] = date_due

        book_copy_id = validated_data['book_copy'].id
        try:
            book_copy = BookCopy.objects.get(id=book_copy_id)
        except BookCopy.DoesNotExist:
            raise serializers.ValidationError({"book_copy": "This BookCopy does not exist."})
        
        book_copy.status = BookCopy.Status.ISSUED
        book_copy.save()
        return Transaction.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if 'date_returned' not in validated_data:
            instance.book_copy.status = BookCopy.Status.ISSUED
            instance.book_copy.save()
        else:
            instance.book_copy.status = BookCopy.Status.AVAILABLE # [revisit]
            instance.book_copy.save()
        return instance