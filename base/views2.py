import datetime

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import Customer, Order
from users.models import User
from django.utils import timezone as zt
from django.contrib.auth.decorators import login_required


def homepage(request):
    # no paid money
    from django.db.models import Sum
    is_paid_False = Order.objects.filter(is_paid=False).aggregate(Sum('price'))
    # paid money
    is_paid_True = Order.objects.filter(is_paid=True).aggregate(Sum('price'))
    #### most recent Transactions
    most_recent_orders = Order.objects.order_by('-date_modified')
    #### mos recent Transactions
    ############## past Due
    past_due_days = datetime.timedelta(days=30)
    today_date = zt.now()
    past_due_date = today_date - past_due_days
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
        # we using Q for search in the database 
        # it is for filter more than one conditions
        from django.db.models import Q
        # get the search param and spilt it
        search_param = request.POST["search"].split()
        # get the len of search param so we can decide if it only a name or name and last 
        search_param_len = len(request.POST["search"].split())
        # print(search_param,search_param_len)
        # if length is only 1 that means either search for name or last  
        if search_param_len == 1:
            customers = Customer.objects.filter(Q(name__icontains=search_param[0]) | Q(last__icontains=search_param[0]))
            print(customers)
        # if length is more than 1 that means search full name 
        elif search_param_len >= 2:
            # print("two way")
            name, last = search_param
            customers = Customer.objects.filter(name__icontains=name, last__icontains=last)
        else:
            # other wise pass
            pass

    context = {
        "customers": customers
    }
    return render(request, 'base/search.html', context)


@login_required
def add_person(request):
    customers = Customer.objects.all()
    if request.method == "POST":
        print(request.POST)

        name = request.POST["name"]
        last = request.POST["last"]

        description = request.POST["description"]
        price = request.POST["price"]
        customer = Customer.objects.create(name=name, last=last)
        order = Order.objects.create(customer=customer, date_created=zt.now(), description=description,
                                     price=float(price))
        return redirect("profile", pk=customer.pk)
    return render(request, 'base/add_person.html', {})


@login_required
def profile(request, pk):
    customer = Customer.objects.get(pk=pk)
    orders = customer.order_set.all().order_by("-date_modified")
    print(orders)
    children = list(customer.customer_set.all())
    context = {
        "customer": customer,
        "orders": orders,
        "children": children
    }
    return render(request, 'base/profile.html', context)


@login_required
def add_order(request, pk):
    customer = Customer.objects.get(pk=pk)
    if request.method == "POST":
        description = request.POST['description']
        price = request.POST['price']
        order = Order.objects.create(customer=customer,
                                     date_created=zt.now(),
                                     description=description,
                                     price=float(price),
                                     customer_total_when_created=customer.total_owe[0]
                                     )
        try:
            is_paid = request.POST['is_paid']
            if is_paid == "on":
                who_paid = request.POST['who_paid']
                payment_method = request.POST['payment_method']
                who_took_money = request.user
                if who_paid == customer.name:
                    order.who_paid = customer
                elif who_paid == customer.parent:
                    order.who_paid = customer.parent
                order.payment_method = payment_method
                order.who_took_money = who_took_money
                order.date_paid = zt.now()
            order.save()

        except:
            print("no payment succeed")

        return redirect("profile", pk=pk)

    context = {
        "customer": customer,
    }
    return render(request, 'base/add_order.html', context)


@login_required
def person_name_change(request, pk):
    if request.method == "POST":
        print(request.POST)
        name = request.POST["name"]
        last = request.POST["last"]
        customer = Customer.objects.get(pk=pk)
        print(name)
        try:
            parent_id = request.POST["parent_id"]
            parent = Customer.objects.get(pk=parent_id)
            customer.parent = parent
        except:
            print("no parent id")
        customer.name = name
        customer.last = last
        customer.save()
    return redirect("profile", pk)


@login_required
def order_pay(request, pk, payment_method):
    order = Order.objects.get(pk=pk)
    customer = order.customer
    if order.is_paid == False:
        order.date_paid = zt.now()
        order.who_paid = order.customer
        order.who_took_money = request.user
        order.payment_method = payment_method.upper()
        order.customer_total_when_paid = customer.total_owe[0]
        order.is_paid = True
        order.save()

    return JsonResponse({"result": "success", "id": order.id, "total-amount": order.customer.total_owe})


@login_required
def child_pay(request, pk):
    customer = Customer.objects.get(pk=pk)
    print(customer.name)
    orders = customer.order_set.all()
    for order in orders:
        if order.is_paid == False:
            order.date_paid = zt.now()
            order.who_paid = order.customer
            order.is_paid = True
            order.save()

    return JsonResponse({"result": "success", "id": customer.id})


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
