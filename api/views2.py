from django.shortcuts import render, HttpResponse
from base.models import Customer, Order

from django.contrib.auth.models import User
from .serializers import CustomerSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

import datetime

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from base.models import Customer, Order
from django.contrib.auth.models import User
from base.func_utils import find_children
from datetime import datetime as dt


@api_view(["POST", "GET"])
def all_paths(request):
    context = {
        "main screen": "",
        "find_parent": "find_parent/<int:pk>/",
        "customer_total_debt": "customer_total_debt/<int:pk>/",
    }
    return Response(context)

@api_view(["POST", "GET"])
def index(request):
    # no paid money
    from django.db.models import Sum
    is_paid_False = Order.objects.filter(is_paid=False).aggregate(Sum('price'))
    # paid money
    is_paid_True = Order.objects.filter(is_paid=True).aggregate(Sum('price'))
    #### most recent Transactions
    most_recent_orders = Order.objects.order_by('-date_created')
    #### mos recent Transactions
    ############## past Due
    past_due_days = datetime.timedelta(days=30)
    today_date = dt.now()
    past_due_date = today_date - past_due_days
    # print(past_due_date)
    past_due_orders = Order.objects.filter(date_created__lt=past_due_date)
    # print(past_due_orders)
    ############# past due

    ###### common_usage
    from django.db.models import Count
    common_usage = Customer.objects.annotate(num_orders=Count("order"))
    common_usage = common_usage.order_by('-num_orders')
    print(common_usage)

    most_recent_orders_api = OrderSerializer(most_recent_orders, many=True)
    past_due_orders_api = OrderSerializer(past_due_orders, many=True)
    common_usage_api = CustomerSerializer(common_usage, many=True)
    ###### common usage
    context = {
        "is_paid_True": is_paid_True['price__sum'],
        "is_paid_False": is_paid_False['price__sum'],
        "most_recent_orders": most_recent_orders_api.data,
        "past_due_orders": past_due_orders_api.data,
        "common_usage": common_usage_api.data,

    }
    return Response(context)

@api_view(["POST", "GET"])
def search_person(request):
    customers = Customer.objects.all()
    if request.method=="POST":

         from django.db.models import Q
         search_param =request.data

         search_param=request.data["search"].split()
         search_param_len= len(request.data["search"].split())
         print(search_param,search_param_len)
         if search_param_len == 1:

             customers = Customer.objects.filter(Q(name__icontains=search_param[0]) | Q(last__icontains=search_param[0]))
             print(customers)
         elif search_param_len == 2:
             print("two way")
             name , last = search_param
             customers = Customer.objects.filter(name__icontains=name, last__icontains=last)
         else:
             pass

    customers_api = CustomerSerializer(customers,many=True)

    context = {
        "customers": customers_api.data
    }
    return Response(context)

@api_view(["POST", "GET"])
def add_person(request):
    if request.method=="POST":
        name = request.data["name"]
        last = request.data["last"]

        description = request.data["description"]
        price = request.data["price"]
        customer = Customer.objects.create(name=name,last=last)
        order=Order.objects.create(customer=customer, date_created=dt.now(),description=description,price=int(price))
        customer_api = CustomerSerializer(customer)

        return  Response(customer_api.data)
    return Response({})

