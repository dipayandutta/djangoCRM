python manage.py shell

from accounts.models import *

#1 Return all the customers from the customer table
customers = Customer.objects.all()
# Display the customer using loop
for customer in customers:
    print(customer)

# Return the first customer in the table
firstCustomer = Customer.objects.first()

#Return the last customer in the table
lastCustomer = Customer.objects.last()

# Return Single customer by name
 

print(customerByName.email)

# Return single customer by ID
customerByID = Customer.objects.get(id=2)

#(7)***Returns orders customer name: (Query parent model values)
order = Order.objects.first() 
parentName = order.customer.name

#(8)***Returns products from products table with value of "Out Door" in category attribute
products = Product.objects.filter(category="Out Door")

#(9)***Order/Sort Objects by id
leastToGreatest = Product.objects.all().order_by('id') 
greatestToLeast = Product.objects.all().order_by('-id') 

#(10) Returns all products with tag of "Sports": (Query Many to Many Fields)
productsFiltered = Product.objects.filter(tags__name="Sports")

'''
(11)Bonus
Q: If the customer has more than 1 ball, how would you reflect it in the database?
A: Because there are many different products and this value changes constantly you would most 
likly not want to store the value in the database but rather just make this a function we can run
each time we load the customers profile
'''

#Returns the total count for number of time a "Ball" was ordered by the first customer
ballOrders = firstCustomer.order_set.filter(product__name="Ball").count()

#Returns total count for each product orderd
allOrders = {}

for order in firstCustomer.order_set.all():
	if order.product.name in allOrders:
		allOrders[order.product.name] += 1
	else:
		allOrders[order.product.name] = 1

#Returns: allOrders: {'Ball': 2, 'BBQ Grill': 1}


#RELATED SET EXAMPLE
class ParentModel(models.Model):
	name = models.CharField(max_length=200, null=True)

class ChildModel(models.Model):
	parent = models.ForeignKey(Customer)
	name = models.CharField(max_length=200, null=True)

parent = ParentModel.objects.first()
#Returns all child models related to parent
parent.childmodel_set.all()