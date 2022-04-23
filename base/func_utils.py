from .models import  Customer, Order
from django.contrib.auth.models import User


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
