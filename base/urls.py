from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("search/", views.search, name="search"),
    path("person_add/", views.person_add, name="person_add"),
    path("profile/<int:pk>/", views.profile, name="profile"),
    path("add_order/<int:pk>/", views.order_add, name="order_add"),
    path("name_change/", views.name_change, name="name_change"),
    path("order_pay/",views.order_pay,name="order_pay"),
    path("child_pay/",views.child_pay,name="child_pay"),


    path("login_page/",views.login_page,name="login_page"),
    path("logout_page/",views.logout_page,name="logout_page"),


]
