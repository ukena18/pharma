from django.shortcuts import render, HttpResponse
from base.models import  Customer, Order

from django.contrib.auth.models import User
from .serializers import CustomerSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

@api_view(["POST","GET"])
def all_paths(request):
    context ={
        "find_children": "find_children/<int:pk>/",
        "find_parent": "find_parent/<int:pk>/",
        "customer_total_debt" :"customer_total_debt/<int:pk>/",
    }
    return  Response(context)

@api_view(["POST","GET"])
def find_children(request,pk):
    # get the customer
    customer = Customer.objects.get(pk=pk)
    # get all the children and put them to the list
    children = list(customer.customer_set.all())
    my_html = f"<h1>--{customer}</h1>"
    for child in children:
        if child.is_parent:
          my_html =my_html+ find_children(request,child.pk)
        else:
            my_html = my_html +f"<h3>------->{child}</h3>"
    return my_html


@api_view(["POST","GET"])
def find_parent(request,pk):
    # find the customer
    customer = Customer.objects.get(pk=pk)
    # get the customer parent
    parent = customer.parent
    # return it
    serializer = CustomerSerializer(parent)
    return Response(serializer.data)

@api_view(["POST","GET"])
def find_all_children(request,pk):
    my_html = find_children(request,pk)
    return Response(my_html)

@api_view(["POST","GET"])
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



    return Response(my_html)
#
# from django.contrib.auth.forms import UserCreationForm
# from .forms import CreateUserCreationForm
#
# def register_page(request):
#     form = CreateUserCreationForm()
#
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#     context = {"form":form}
#     return render(request, "base/register.html", context)
