from django.shortcuts import render

from .models import *
# Create your views here.
def home(request):
    order = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = order.count()
    delivered = Order.objects.all().filter(status='Delivered').count()
    pending   = order.filter(status='Pending').count()

    context = {'orders':order,'customers':customers,'total_customers':total_customers,'total_orders':total_orders,
        'Delivered':delivered,'Pending':pending
    }
    template_name='accounts/dashboard.html'
    return render(request,template_name,context)


def products(request):
    template_name = 'accounts/Products.html'
    products = Product.objects.all()
    return render(request,template_name,{'products':products})

def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer':customer,'orders':orders,'order_count':order_count}

    template_name = 'accounts/customer.html'
    return render(request,template_name,context)