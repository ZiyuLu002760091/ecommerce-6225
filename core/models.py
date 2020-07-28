from common.models import BaseCustomer, AutoCreateUpdatedMixin
from auth_core.models import UserClient
from django.conf import settings
from django.db import models
import uuid
import os

class Customer(BaseCustomer):
    user = models.OneToOneField(UserClient, on_delete=models.CASCADE, related_name='user_client')
    phone = models.CharField(max_length=12)

    class Meta:
        verbose_name = 'client'

class Address(models.Model, AutoCreateUpdatedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='user_client_address')
    street = models.CharField(max_length=200)
    suite = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'address'

class CreditCard(models.Model, AutoCreateUpdatedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='user_client_creditcard')
    owner = models.CharField(max_length=60)
    flag = models.CharField(max_length=60)
    number = models.CharField(max_length=60)
    number_security = models.CharField(max_length=3)

    class Meta:
        verbose_name = 'creditcard'

class Status(models.Model, AutoCreateUpdatedMixin):

    STATUS = (
        (0, 'Processing Purchase'),
        (1', 'Approved Purchase'),
        (2', 'Purchase Denied'),
        (3', 'Purchase sent'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.CharField(max_length=30, default=0, choices=STATUS)
    
    class Meta:
        verbose_name = 'status'

class Order(models.Model, AutoCreateUpdatedMixin):

    CALC = (
       (0, 0.0),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='user_client_order')
    status = models.OneToOneField(Status, on_delete=models.PROTECT, null=True, related_name="status")
    total = models.FloatField(default=0, choices=CALC)

    class Meta:
        verbose_name = 'order'
    
    @property
    def get_status(self):
        return self.status.message
        
class Author(models.Model, AutoCreateUpdatedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60)
    email = models.EmailField()

    class Meta:
        verbose_name = 'author'

class Category(models.Model, AutoCreateUpdatedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField()
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'category'

def hash_filename_to_uuid(instance, filename):
    ext = os.path.splitext(filename)
    new_filename = "{0}{1}".format(uuid.uuid4(), ext)
    return new_filename

def upload_to(instance, filename):
    new_filename = hash_filename_to_uuid(instance, filename)
    return os.path.join(settings.MEDIA_BASE_PATH + '/books/', new_filename)

class Book(models.Model, AutoCreateUpdatedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=60)
    prince = models.FloatField()
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories_books")
    image = models.ImageField(max_length=255, upload_to=upload_to)
    
    class Meta:
        verbose_name = 'books'

class Write(models.Model, AutoCreateUpdatedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="writes")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'writes'

class ItemOrder(models.Model, AutoCreateUpdatedMixin):

    CALC = (
       (0, 0.0),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="item_order")
    amount = models.IntegerField()
    subtotal = models.FloatField(default=0, choices=CALC)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'item order'