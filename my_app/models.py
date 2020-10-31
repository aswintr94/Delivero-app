from django.db import models
import uuid
from django.utils import timezone

# Create your models here.
class Admin_Register(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    image = models.ImageField(upload_to='admin')

class Driver_Register(models.Model):
    driver_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    mobile = models.IntegerField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class Tasks(models.Model):
    admin_id = models.ForeignKey(Admin_Register,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    order_id = models.CharField(max_length=20)
    invoice_no = models.CharField(max_length=20)
    product = models.CharField(max_length=50)
    driver_code = models.CharField(max_length=10)
    customer_name = models.CharField(max_length=30)
    customer_mobile = models.IntegerField()
    shipping_name = models.CharField(max_length=30)
    customer_address = models.CharField(max_length=100)
    district = models.CharField(max_length=20)
    pin_code = models.IntegerField()
    alt_contact_no = models.IntegerField()
    client = models.CharField(max_length=20)
    preference = models.IntegerField()
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)
    status = models.CharField(max_length=20,default=True)

class Delivered(models.Model):
    creator = models.CharField(max_length=20)
    delivered_date = models.DateField(auto_now_add=True)
    delivered_time = models.TimeField(default=timezone.now())
    task_created_date = models.DateField()
    task_id = models.IntegerField()
    serial_no = models.IntegerField()
    pod_type = models.CharField(max_length=20)
    id_card_no = models.CharField(max_length=20)
    order_id = models.CharField(max_length=20)
    driver_code = models.CharField(max_length=20)
    invoice_no = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=20)
    client_name = models.CharField(max_length=20)
    comment = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)

class Returned(models.Model):
    creator = models.CharField(max_length=20)
    returned_date = models.DateField(auto_now_add=True)
    returned_time = models.TimeField(default=timezone.now())
    task_created_date = models.DateField()
    task_id = models.IntegerField()
    order_id = models.CharField(max_length=20)
    driver_code = models.CharField(max_length=20)
    invoice_no = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=20)
    client_name = models.CharField(max_length=20)
    reason = models.CharField(max_length=100)
    comment = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)

class Delivery_Documents(models.Model):
    task_id = models.IntegerField()
    signature = models.FileField(upload_to='delivered_doc')
    document1 = models.FileField(upload_to='delivered_doc')
    document2 = models.FileField(upload_to='delivered_doc',null=True)
    document3 = models.FileField(upload_to='delivered_doc',null=True)

class Delivery_Docs_by_admin(models.Model):
    task_details = models.ForeignKey(Delivered,on_delete=models.CASCADE)
    document = models.FileField(upload_to='delivery_docs_by_admin',null=True)

class Return_Documents(models.Model):
    return_item_details = models.ForeignKey(Returned,on_delete=models.CASCADE,null=True)
    document = models.FileField(upload_to='returned_doc',null=True)

class Statistics(models.Model):
    admin = models.ForeignKey(Admin_Register,on_delete=models.CASCADE,null=True)
    pending_tasks = models.IntegerField()
    delivered_tasks = models.IntegerField()
    returned_tasks = models.IntegerField()
    