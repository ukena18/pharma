import datetime

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import Customer, Order
from users.models import User
from django.utils import timezone as zt
from django.contrib.auth.decorators import login_required
# for json.parse we will use json.loads 
import json

# we use Q for combine two filter at the same time
# Q(name__icontains=search_param[0]) | Q(last__icontains=search_param[0]))
# it says either name or last check if containing the param
from django.db.models import Q


def homepage(request):
    print(request.user)
    # no paid money
    from django.db.models import Sum
    is_paid_False = Order.objects.filter(is_paid=False).aggregate(Sum('price'))
    # paid money
    is_paid_True = Order.objects.filter(is_paid=True).aggregate(Sum('price'))
    #### most recent Transactions
    most_recent_orders = Order.objects.order_by('-date_modified')[:10]
    #### mos recent Transactions
    ############## past Due
    past_due_days = datetime.timedelta(days=30)
    today_date = zt.now()
    past_due_date = today_date - past_due_days
    # print(past_due_date)
    past_due_orders = Order.objects.filter(date_created__lt=past_due_date)[:10]
    # print(past_due_orders)
    ############# past due

    ###### common_usage
    from django.db.models import Count
    common_usage = Customer.objects.annotate(num_orders=Count("order"))
    common_usage = common_usage.order_by('-num_orders')[:10]
    ###### common usage
    context = {
        "is_paid_True": is_paid_True['price__sum'],
        "is_paid_False": is_paid_False['price__sum'],
        "most_recent_orders": most_recent_orders,
        "past_due_orders": past_due_orders,
        "common_usage": common_usage,
    }
    return render(request, 'base/homepage.html', context)


# search customers
def search(request):
    # first show all the customers
    customers = Customer.objects.all()
    # if it is post method
    if request.method == "POST":
        # get the search param and spilt it
        search_param = request.POST["search"].split()
        # get the len of search param so we can decide if it only a name or name and last 
        search_param_len = len(request.POST["search"].split())
        
        # if length is only 1 that means either search for name or last  
        if search_param_len == 1:
            # use Q filter method give you OR statement
            customers = Customer.objects.filter(
                # value__icontains is built-in method give you any string contain the value
                Q(name__icontains=search_param[0]) | Q(last__icontains=search_param[0]))
        # if the lenght is 2 it means we  are looking for full name
        elif search_param_len == 2:
            # get the first and last name from search param
            name, last = search_param
            #filter through customers  find name and last match at the same time
            # Q filter method gives you OR statement and filter gives you AND statement
            # it may be two customer have same full name 
            customers = Customer.objects.filter(name__icontains=name, last__icontains=last)
        # this is for customer has more than two names 
        # do it later
        else:
            pass

    context = {
        "customers": customers
    }
    return render(request, 'base/search.html', context)


@login_required
def person_add(request): 
    if request.method == "POST":
        name = request.POST["name"]
        last = request.POST["last"]
        description = request.POST["description"]
        price = request.POST["price"]
        # first create customer
        customer = Customer.objects.create(name=name, last=last)
        #create order
        order = Order.objects.create(customer=customer, 
                                        description=description,
                                        price=float(price),
                                        # customer total unpaid before the order was created
                                        customer_total_when_created=customer.total_owe[0],
                                        )
        # redirect to the profile
        return redirect("profile", pk=customer.pk)
    return render(request, 'base/person_add.html', {})


@login_required
def profile(request, pk):
    customer = Customer.objects.get(pk=pk)
    orders = customer.order_set.all().order_by("-date_modified")
    children = list(customer.customer_set.all())
    context = {
        "customer": customer,
        "orders": orders,
        "children": children
    }
    return render(request, 'base/profile.html', context)


@login_required
def order_add(request, pk):
    # get the customer from url param
    # we wanna prefill name and last
    customer = Customer.objects.get(pk=pk)
    # if request is post
    if request.method == "POST":
        # get the description and price from post data
        description = request.POST['description']
        price = request.POST['price']
        # create order with data we have
        order = Order.objects.create(customer=customer,        
                                        # description for this order
                                        description=description,
                                        # price of this order
                                        price=float(price),
                                        # customer total unpaid before the order was created
                                        customer_total_when_created=customer.total_owe[0]
                                        )

        try:
            is_paid = request.POST['is_paid']
            if is_paid == "on":
                who_paid = request.POST['who_paid']
                payment_method = request.POST['payment_method']
                
                if who_paid == customer.name:
                    order.who_paid = customer
                elif who_paid == customer.parent.name:
                    order.who_paid = customer.parent
                order.payment_method = payment_method
                order.who_took_money = request.user
                order.date_paid = zt.now()
                order.is_paid = True
            order.save()

        except Exception as e:
	        print("no paymnet success, ERROR : "+str(e))

        return redirect("profile", pk=pk)

    context = {
        "customer": customer,
    }
    
    return render(request, 'base/order_add.html', context)


@login_required
def name_change(request):
    # get the data from page using ajax post request
    # all info should be inside body
    # then decode info and parse from json to python dict
    data = json.loads(request.body.decode('utf-8'))
    #get the pk  of child
    pk = data["pk"]
    name = data["name"]
    last = data["last"]
    #find the customer
    customer = Customer.objects.get(pk=pk)
    # try to add parent id 
    try:
        # get the parent id
        parent_id = data["parent_id"]
        # check if there is parent with this id
        parent = Customer.objects.get(pk=parent_id)
        # if there is one then add customer to parent of curretn customer
        customer.parent = parent
    except:
        print("no parent id")
    # then save the customer name and last
    customer.name = name
    customer.last = last
    customer.save()
    if customer.parent:
        parent_id = customer.parent.id
    else:
        parent_id = None

    return JsonResponse({"result":"success","name":customer.name,"last":customer.last,"parent_id":parent_id})


@login_required
def order_pay(request):
    # get the data from page using ajax post request
    # all info should be inside body
    # then decode info and parse from json to python dict
    data = json.loads(request.body.decode('utf-8'))
    #get the pk  of child
    pk = data["pk"]
    payment_method = data["payment_method"]
    #get the order
    order = Order.objects.get(pk=pk)
    # find the customer
    customer = order.customer
    if order.is_paid == False:
            # set time for date_paid
            order.date_paid = zt.now()
            # add payment method
            order.payment_method = payment_method
            # since customer pay for children payer is obvious
            # customer total owe before payment 
            order.customer_total_when_paid = customer.total
            try :
                # if admin logged in then he took the money
                order.who_took_money = request.user
            except:
                #otherwise print error
                raise ValueError(f"admin is not logged in {request.user}")
            order.who_paid = order.customer
            # order.is_paid equal to true
            order.is_paid = True
            # save the order
            order.save()
    print(order.customer.total_owe)
    return JsonResponse({"result": "success", "id": order.id, "total-amount": order.customer.total_owe[0]})


@login_required
def child_pay(request):
    # get the data from page using ajax post request
    # all info should be inside body
    # then decode info and parse from json to python dict
    data = json.loads(request.body.decode('utf-8'))
    #get the pk  of child
    pk = data["pk"]
    payment_method = data["payment_method"]
    # find the child
    customer = Customer.objects.get(pk=pk)
    # get all othe orders 
    orders = customer.order_set.all()
    # loop through all orders
    for order in orders:
        # check unpaid orders
        if order.is_paid == False:
            # set time for date_paid
            order.date_paid = zt.now()
            # add payment method
            order.payment_method = payment_method
            # since customer pay for children payer is obvious
            # customer total owe before payment 
            order.customer_total_when_paid = customer.total
            try :
                # if admin logged in then he took the money
                order.who_took_money = request.user
            except:
                #otherwise print error
                raise ValueError(f"admin is not logged in {request.user}")
            order.who_paid = order.customer
            # order.is_paid equal to true
            order.is_paid = True
            # save the order
            order.save()
        \
    return JsonResponse({"result": "success", "id": customer.id,"total__amount":customer.total_owe})
    


from django.contrib.auth import authenticate, login, logout


def login_page(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            print("tried")
            user = authenticate(request, email=email, password=password)
            print(user)
            if user:
                login(request, user)
                return redirect("homepage")
        except:
            pass

    return render(request, "base/login_page.html", {})


def logout_page(request):
    try:
        if request.user:
            logout(request)

    except:
        pass

    return redirect("login_page")
