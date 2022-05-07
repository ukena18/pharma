# get the models from base app
from base.models import Customer, Order
# serializers library
from rest_framework import serializers

# Customer serializers
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

# order serializers
class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Order
        fields = "__all__"