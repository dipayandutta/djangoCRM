from django.shortcuts import render,redirect
from .models import *
# for multiple order from the single page
from django.forms import inlineformset_factory
from .forms import OrderForm,CreateUserForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm

#flash message import for showing register or login message
from django.contrib import messages
# importing for user authentication , login and logout
from django.contrib.auth import authenticate , login , logout
# login Restriction import
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user,allowed_user,admin_only

# Registration View
@unauthenticated_user
def registerPage(request):
    '''
    #form = UserCreationForm()
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
    '''
    form = CreateUserForm()
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            #get the username
            username = form.cleaned_data.get('username')

            # Automatically associated as customer
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request,'Account is created for User '+ username)
            return redirect('login')

    context = {'form':form}
    return render(request,'accounts/register.html',context)

# Login View
@unauthenticated_user
def loginPage(request):
    '''
    if request.user.is_authenticated:
        return redirect('home')
    else:'''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or password is incorrect!')
    context = {}
    return render(request,'accounts/login.html',context)

# Logout View

def logoutUser(request):
    logout(request)

    return redirect ('login')


@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def userPage(request):
    #get all the customer orders
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = Order.objects.all().filter(status='Delivered').count()
    pending   = orders.filter(status='Pending').count()
    print(orders)
    context = {'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'accounts/user.html',context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def products(request):
    template_name = 'accounts/Products.html'
    products = Product.objects.all()
    return render(request,template_name,{'products':products})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}

    template_name = 'accounts/customer.html'
    return render(request,template_name,context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request,pk):

    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request,'accounts/delete.html',context)