from django.urls import path
from . import views2

urlpatterns = [
    path("home/", views2.index, name="index"),
    path("search_person/", views2.search_person, name="search_person"),
    path("add_person/", views2.add_person, name="add_person"),
    path("person/<int:pk>/", views2.person, name="person"),
    path("add_order/<int:pk>/", views2.add_order, name="add_order"),
    path("person_name_change/<int:pk>/", views2.person_name_change, name="person_name_change"),
    path("order_pay/<int:pk>/<str:payment_method>",views2.order_pay,name="order_pay"),
    path("child_pay/<int:pk>/",views2.child_pay,name="child_pay"),

]
# urlpatterns = [
#     path("find_parent/<int:pk>/", views.find_parent, name="find_parent"),
#     path("register/", views.register_page, name="register"),
#     path("find_children/<int:pk>/", views.find_all_children, name="find_children"),
#     path("customer_total_debt/<int:pk>/", views.customer_total_debt, name="customer_total_debt"),
# ]