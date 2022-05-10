from .serializers import CustomerSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
import base.models as md
from django.utils import timezone as zt
from django.contrib.auth import authenticate, login, logout

# we use Q for combine two filter at the same time
# Q(name__icontains=search_param[0]) | Q(last__icontains=search_param[0]))
# it says either name or last check if containing the param
from django.db.models import Q


@api_view(["GET"])
def all_paths(request):

    print(request.user)
    context = [
        {"url": ["main screen", "homepage/"],"id": "1"},
        {"url": ["search", "search/"], "id": "2"},
        {"url": ["find_parent", "find_parent/pk/"], "id": "3"},
        {"url": ["profile", "profile/pk/"], "id": "4"},
        {"url": ["Order add", "add_order/pk/"], "id": "5"},
        {"url": ["Name change", "name_change/pk/"], "id": "6"},
        {"url": ["pay order", "order_pay/pk/payment_method"], "id": "7"},
        {"url": ["login", "login_page/"], "id": "8"},
        {"url": ["logout", "logout_page/"], "id": "9"},

    ]
    return Response(context)



@api_view(["GET"])
def homepage(request):
    # no paid money
    from django.db.models import Sum
    is_paid_False = md.Order.objects.filter(is_paid=False).aggregate(Sum('price'))
    # paid money
    is_paid_True = md.Order.objects.filter(is_paid=True).aggregate(Sum('price'))
    #### most recent Transactions
    most_recent_orders = md.Order.objects.order_by('-date_created')[0:10]
    #### mos recent Transactions
    ############## past Due
    past_due_days = datetime.timedelta(days=30)
    today_date = zt.now()
    past_due_date = today_date - past_due_days
    # print(past_due_date)
    past_due_orders = md.Order.objects.filter(date_created__lt=past_due_date)[0:10]
    # print(past_due_orders)
    ############# past due

    ###### common_usage
    from django.db.models import Count
    common_usage = md.Customer.objects.annotate(num_orders=Count("order"))
    common_usage = common_usage.order_by('-num_orders')[0:10]
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
def search(request):
    # get all the custumers on GET request
    customers = md.Customer.objects.all()
    if request.method == "POST":
        #split the search param  it maybe only name or both last and first
        search_param = request.data["search"].split()
        # get the length of the search param 
        # so we cacn decide if it only a name or full name
        search_param_len = len(request.data["search"].split())
        # if the lenght is 1 it means we are either searching for name or last
        if search_param_len == 1:
            # use Q filter method give you OR statement
            customers = md.Customer.objects.filter(
                # value__icontains is built-in method give you any string contain the value
                Q(name__icontains=search_param[0]) | Q(last__icontains=search_param[0]))
        # if the lenght is 2 it means we  are looking for full name
        elif search_param_len == 2:
            # get the first and last name from search param
            name, last = search_param
            #filter through customers  find name and last match at the same time
            # Q filter method gives you OR statement and filter gives you AND statement
            # it may be two customer have same full name 
            customers = md.Customer.objects.filter(name__icontains=name, last__icontains=last)
        # this is for customer has more than two names 
        # do it later
        else:
            pass
    # serialze all the customer after post or get method
    customers_api = CustomerSerializer(customers, many=True)
    # add it to the context
    context = {
        "customers": customers_api.data,
        "sample":{"search":"azra zelal"},   
    }
    return Response(context)


@api_view(["POST", "GET"])
def person_add(request):
    if request.method == "POST":
        name = request.data["name"]
        last = request.data["last"]
        # each created customer created with an order 
        description = request.data["description"]
        price = request.data["price"]
        print(price)
        customer = md.Customer.objects.create(name=name, last=last)
        order = md.Order.objects.create(customer=customer, 
                                        description=description,
                                        price=float(price),
                                        # customer total unpaid before the order was created
                                        customer_total_when_created=customer.total_owe[0],
                                        )
                                        
        customer_api = CustomerSerializer(customer)
        # after psot method return customer 
        return Response(customer_api.data)
    # test data
    return Response({"use for test": [{"name": "azra", "last": "zelal", "description": "clorofom", "price": "23.43"}]})

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request, pk):
    # get the custmer from url params
    customer = md.Customer.objects.get(pk=pk)
    # get all the customer orders 
    orders = customer.order_set.all().order_by("-date_modified")
    # if there is get all the children of customer
    children = list(customer.customer_set.all())
    # serialize the customer
    customer_api = CustomerSerializer(customer)
    # serialize the cgildren
    children_api = CustomerSerializer(children,many=True)
    # serialize all the orders of customer
    orders_api = OrderSerializer(orders, many=True)
    # add to context all data
    context = {
        "customer": customer_api.data,
        "orders": orders_api.data,
        "children": children_api.data
    }
    # responsethe data
    return Response(context)



@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def order_add(request,pk):
    # get the customer 
    customer = md.Customer.objects.get(pk=pk)
    customer_api = CustomerSerializer(customer)
    result = {"result":"it is get moethod", "customer":customer_api.data} 
    #  if it post tequest
    if request.method == "POST":
        # get the description from the post data
        # in django we use request.POST but in djangorestframework we use request.data
        description = request.data['description']
         # get the price from the post data
        price = request.data['price']
        
        
        # create order with data we have
        order = md.Order.objects.create(customer=customer,        
                                        # description for this order
                                        description=description,
                                        # price of this order
                                        price=float(price),
                                        # customer total unpaid before the order was created
                                        customer_total_when_created=customer.total_owe[0]
                                        )

        
        try:
            is_paid = request.data['is_paid']
            
            if is_paid or is_paid=="on":
                who_paid = request.data['who_paid']
                payment_method = request.data['payment_method']
                if who_paid == customer.name or who_paid==customer.id:
                    order.who_paid = customer
                elif who_paid == customer.parent.name or who_paid==customer.parent.id:
                    order.who_paid = customer.parent
                order.payment_method = payment_method

                order.who_took_money = request.user
                print(request.user)
                order.date_paid = zt.now()
                print(zt.now())
                order.is_paid =True
            
            order.save()

        except Exception as e:
	        print("no paymnet success, ERROR : "+str(e))
        customer.total = customer.total_owe[0]
        customer.save()
        customer_api = CustomerSerializer(customer)
        parent_api = CustomerSerializer(customer.parent)
        order_api = OrderSerializer(order)
        result = {"result":"success","customer": customer_api.data,"parent":parent_api.data,"order":order_api.data}   
    context = {
        "result": result,
        "sample": [
            {"method":"prepaid","description": "secreal", "price": "12.21", "is_paid": "on", "who_paid": "azra", "payment_method": "CARD"},
            {"method":"unpaid","description": "secreal", "price": "12.21"},
        ]
    }
    return Response(context)


@api_view(["POST", "GET"])
def name_change(request):
    result = {"result":"it is get moethod"} 
    #  if it is post request
    if request.method == "POST":
        # get the name and lastname from post data
        # in django we use request.POST but in djangorestframework we use request.data
        name = request.data["name"]
        last = request.data["last"]
        pk = request.data["pk"]
        # get the customer 
        customer = md.Customer.objects.get(pk=pk)
    
        # try to change aprent id to
        try:
            # get parent_id param from post data
            parent_id = int(request.data["parent_id"])
            print(parent_id)
            # check db if there is  customer  with that id
            parent = md.Customer.objects.get(pk=parent_id)
            # if there is customer with that id then update parent of customer
            customer.parent = parent
        except:
            raise ValueError("there is no such parent id")
        # update customer name and last name from post data
        customer.name = name
        customer.last = last
        # save the customer
        customer.save()
        # serialize customer either post or get request 
        customer_api = CustomerSerializer(customer)
        result = {"result":customer_api.data}
    # context has customer and  a ssample if you want to replicate
    context = {
        "sample": [{"pk":"12","name": "azram", "last": "zelalim", "parent_id": "2"}],
        #updated customer as an json data
        "result" :result,
        
    }
    # send context data
    return Response(context)


@api_view(["GET","POST"])
def order_pay(request):
    result = {"result":"it is get method"} 
    if request.method == "POST":
        # get the order from post data
        pk = request.data["pk"]    
        payment_method = request.data["payment_method"]
        #find the order
        order = md.Order.objects.get(pk=pk)
        # find customer for this order
        customer = order.customer
        # check if order is paid or not
        if order.is_paid == False:
            # date_paid = right_now
                order.date_paid = zt.now()
                #  just check if admin logged in
                try :
                    # if admin logged in then he took the money
                    order.who_took_money = request.user
                except:
                    #otherwise print error
                    raise ValueError("admin is not logged in")
                # get the payment method from url param 
                # incase we just uppercase payment method
                order.payment_method = payment_method.upper()
                #since it ischild payment it is obviously parent pay for orders
                order.who_paid = order.customer
                #customer total when he paid this order 
                #total owe return 2 variable one is unpaid total of customer
                # second paid total of customer
                order.customer_total_when_paid = customer.total_owe[0]
                # then is_paid =True
                order.is_paid = True
                # save the order
                order.save()
                result = {"result":"success","id":order.id,"total-amount":order.customer.total_owe}
        else:
            raise ValueError("order is already paid")
    context = {
        "sample":{
            "pk":"8",
            "payment_method":"CARD",
        },
        "result":result,
    }
        
    #send response with the order.id and customer total_owe send paid and unpaid of customer
    return Response(context)


@api_view(["POST","GET"])
def child_pay(request):
    result = {"result":"it is get moethod"} 
    if request.method == "POST":
        pk = request.data["pk"]
        payment_method = request.data["payment_method"]
        # get the customer from url param
        customer = md.Customer.objects.get(pk=pk)
        # get all the orders from current customer
        orders = customer.order_set.all()
        
        # loop through the orders
        for order in orders:
            # if order is not paid then try to pay for the order
            if not order.is_paid:
                # date_paid = right_now
                order.date_paid = zt.now()
                # add payment method
                order.payment_method = payment_method
                # customer total owe before payment 
                order.customer_total_when_paid = customer.total
                #  just check if admin logged in
                try :
                    # if admin logged in then he took the money
                    order.who_took_money = request.user
                except:
                    #otherwise print error
                    raise ValueError(f"admin is not logged in {request.user}")
                #since it ischild payment it is obviously parent pay for orders
                order.who_paid = order.customer
                # then is_paid =True
                order.is_paid = True
                # save the order
                order.save()
            result = {"result":"success","id":customer.id}
    context = {
        "sample":{
            "pk":"8",
            "payment_method":"CARD",
        },
        "result":result,
    }
    # send response of succes and id number of customer 
    return Response(context)


