import datetime

from django.shortcuts import render, HttpResponse,redirect
from django.http import JsonResponse
from .models import Customer, Order
from django.contrib.auth.models import User
from .func_utils import find_children
from datetime import datetime as dt

def index(request):
    #no paid money
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
    past_due_date= today_date - past_due_days
    # print(past_due_date)
    past_due_orders = Order.objects.filter(date_created__lt=past_due_date)
    # print(past_due_orders)
    ############# past due

    ###### common_usage
    from django.db.models import Count
    common_usage = Customer.objects.annotate(num_orders=Count("order"))
    common_usage = common_usage.order_by('-num_orders')
    ###### common usage
    context = {
        "is_paid_True":is_paid_True['price__sum'],
        "is_paid_False":is_paid_False['price__sum'],
        "most_recent_orders": most_recent_orders,
        "past_due_orders":past_due_orders,
        "common_usage":common_usage,
    }
    return render(request, 'base/index.html', context)

def search_person(request):
    customers = Customer.objects.all()
    if request.method=="POST":
         from django.db.models import Q
         search_param=request.POST["search"].split()
         search_param_len= len(request.POST["search"].split())
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


    context = {
        "customers": customers
    }
    return render(request, 'base/search_person.html', context)






def add_person(request):
    customers = Customer.objects.all()
    if request.method=="POST":
        print(request.POST)

        name = request.POST["name"]
        last = request.POST["last"]

        description = request.POST["description"]
        price = request.POST["price"]
        customer = Customer.objects.create(name=name,last=last)
        order=Order.objects.create(customer=customer, date_created=dt.now(),description=description,price=int(price))
        return redirect("person", pk=customer.pk)
    return render(request, 'base/add_person.html', {})

def person(request,pk):
    customer = Customer.objects.get(pk=pk)
    orders= customer.order_set.all().order_by("-date_created")
    print(orders)
    children = list(customer.customer_set.all())
    context = {
        "customer": customer,
        "orders":orders,
        "children":children
    }
    return render(request, 'base/person.html', context)

def add_order(request,pk):
    customer = Customer.objects.get(pk=pk)
    if request.method=="POST":
        description = request.POST['description']
        price = request.POST['price']
        order = Order.objects.create(customer=customer,
                                     date_created=dt.now(),
                                     description=description,
                                     price=int(price),
                                     customer_total_when_created=customer.total_owe[0]
                                     )

        return redirect("person", pk=pk)

    context = {
        "customer": customer,
    }
    return render(request, 'base/add_order.html', context)



def person_name_change(request,pk):
    if request.method == "POST":
        print(request.POST)
        name = request.POST["name"]
        last = request.POST["last"]
        parent_id = request.POST["parent_id"]
        customer = Customer.objects.get(pk=pk)
        try:
            parent = Customer.objects.get(pk=parent_id)
            customer.parent = parent
        except:
            print("no parent id")
        customer.name=name
        customer.last=last
        customer.save()
    return redirect("person",pk)

def order_pay(request,pk,payment_method):
    order = Order.objects.get(pk=pk)
    customer = order.customer
    if order.is_paid == False:
        order.date_paid = dt.now()
        order.who_paid = order.customer
        order.payment_method = payment_method.upper()
        order.customer_total_when_paid = customer.total_owe[0]
        order.is_paid= True
        order.save()

    return JsonResponse({"result":"success","id":order.id,"total-amount":order.customer.total_owe})


def child_pay(request,pk):
    customer = Customer.objects.get(pk=pk)
    print(customer.name)
    orders = customer.order_set.all()
    for order in orders:
        if order.is_paid == False:
            order.date_paid = dt.now()
            order.who_paid = order.customer
            order.is_paid= True
            order.save()

    return JsonResponse({"result":"success","id":customer.id})