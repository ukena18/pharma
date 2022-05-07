from django.db import models
from users.models import User
from django.utils import timezone


# create the customer for pharmacy
class Customer(models.Model):
    # each customer can and user will have the onetoone field
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)

    name = models.CharField(max_length=200,blank=True,null=True)
    last = models.CharField(max_length=200,blank=True,null=True)
    # is parent  model is for put child customer inside parent customer
    is_parent = models.BooleanField(default=False, blank=True,null=True)

    password = models.IntegerField(blank=True,null=True)
    phone = models.BigIntegerField(blank=True,null=True)
    total = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    # foreign key to it self for parent class
    # if ahmet has parent nezire then he can pick other customer as parent
    parent=models.ForeignKey('self', on_delete=models.CASCADE,blank=True,null=True)

    @property
    def total_owe(self):
        order_list = list(self.order_set.all())
        children = list(self.customer_set.all())

        total_unpaid= 0
        total_paid= 0

        for single_order in list(self.order_set.all()):
            if not single_order.is_paid:
                total_unpaid += float(single_order.price)
            elif single_order.is_paid:
                total_paid += float(single_order.price)
        for child in children:
            order_list += list(child.order_set.all())
            for single_order in list(child.order_set.all()):
                if not single_order.is_paid:
                    total_unpaid += float(single_order.price)
                elif single_order.is_paid:
                    total_paid += float(single_order.price)
        return (round(total_unpaid,2),round(total_paid,2))
    def __str__(self):
        return f"{self.name} -- --{self.id}"


class Order(models.Model):
    payment_method_list = [("CASH","CASH"),("CARD","CARD")]
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True,)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    customer_total_when_created = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    is_paid = models.BooleanField(default=False, blank=True,null=True)
    payment_method = models.CharField(choices=payment_method_list,max_length=4,blank=True,null=True)
    who_paid = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True, related_name='who_paid')
    who_took_money = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True, related_name='who_took_money')
    customer_total_when_paid = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    date_paid = models.DateTimeField(blank=True,null=True)
    date_created = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    date_modified = models.DateTimeField(blank=True, null=True, auto_now=True)

   

    def __str__(self):
        return f"{self.description[0:12]} --{self.id}"



from django.db.models.signals import post_save
def update_total_owe_created_order(sender,instance,created,**kwargs):
    
    if created:
        order = instance
        customer = order.customer
        customer.total = customer.total_owe[0]
        customer.save()

post_save.connect(update_total_owe_created_order,sender=Order)

def update_total_owe_updated_order(sender,instance,created,**kwargs):
    if created==False:
        order = instance
        customer = order.customer
        customer.total = customer.total_owe[0]
        customer.save()
post_save.connect(update_total_owe_updated_order,sender=Order)