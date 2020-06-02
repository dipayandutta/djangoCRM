from django.shortcuts import render,redirect
from .models import *
# for multiple order from the single page
from django.forms import inlineformset_factory
from .forms import OrderForm

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

def createOrder(request,pk):

    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)#number of fields to display using extra
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)#Order.objects.none() will remove the initial field database value
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #form = OrderForm(request.POST) # this is due to the use of modelForm
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    #context = {'form':form}
    context = {'formset':formset}
    return render(request,'accounts/order_form.html',context)


def updateOrder(request,pk):
    # Pre fill the items in the list of Orders
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order) #instance =order this will show the data

    # Now save the Update Date in the Database
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order) # pass the new instance i.e. the updated data
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'accounts/order_form.html',context)


def deleteOrder(request,pk):

    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request,'accounts/delete.html',context)