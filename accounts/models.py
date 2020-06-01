from django.db import models

# Create your models here.
class Customer(models.Model):
    name    = models.CharField(max_length=200,null=True)
    phone   = models.CharField(max_length=200,null=True)
    email   = models.CharField(max_length=200,null=True)
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


# For many to many relationship

class Tag(models.Model):
    name = models.CharField(max_length=200,null=True)

    def __str__(sellf):
        return self.name


class Product(models.Model):
    CATEGORY = (
            ('Indoor','Indoor'),
            ('Out Door','Out Door'),
            )
    name        = models.CharField(max_length=200,null=True) 
    price       = models.FloatField(null=True)
    category    = models.CharField(max_length=200,null=True,choices=CATEGORY)
    description = models.CharField(max_length=200,null=True)
    date_created= models.DateTimeField(auto_now_add=True,null=True)
    # Add the Many to Many Relationship
    tags = models.ManyToManyField(Tag)




class Order(models.Model):
    '''
        For Drop Down Menu
    '''
    STATUS = (
            ('Pending','Pending'),
            ('Out for Delivery','Out for Delivery'),
            ('Delivered','Delivered'),
            )
    #One to Many Relaionship
    customer = models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product  = models.ForeignKey(Product,null=True,on_delete=models.SET_NULL) 

    date_created = models.DateTimeField(auto_now_add=True,null=True)
    status       = models.CharField(max_length=200,null=True,choices=STATUS)

   