from django.shortcuts import render, HttpResponse
from .models import  Customer, Order
from django.contrib.auth.models import User
from .func_utils import find_children


def find_parent(request,pk):
    # find the customer
    customer = Customer.objects.get(pk=pk)
    # get the customer parent
    parent = customer.parent
    # return it
    return HttpResponse(parent)

def find_all_children(request,pk):
    my_html = find_children(request,pk)
    return HttpResponse(my_html)

def customer_total_debt(request,pk):
    customer = Customer.objects.get(pk=pk)
    order_list = list(customer.order_set.all())
    children = list(customer.customer_set.all())
    my_html = f"<h1>-->{customer}</h1>"
    for single_order in list(customer.order_set.all()):
        my_html = my_html + f"<h5>--------{single_order}__{single_order.price}$</h5>"
    for child in children:
        order_list += list(child.order_set.all())
        my_html = my_html +f"<h3>--->{child}</h3>"
        for single_order in list(child.order_set.all()):
            my_html = my_html + f"<h5>--------{single_order}__{single_order.price}$</h5>"

    print(order_list)



    return HttpResponse(my_html)

from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserCreationForm

def register_page(request):
    form = CreateUserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    context = {"form":form}
    return render(request, "base/register.html", context)
