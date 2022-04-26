from django.urls import path
from . import views2

urlpatterns = [
    path("", views2.homepage, name="homepage"),
    path("search/", views2.search, name="search"),
    path("add_person/", views2.add_person, name="add_person"),
    path("profile/<int:pk>/", views2.profile, name="profile"),
    path("add_order/<int:pk>/", views2.add_order, name="add_order"),
    path("person_name_change/<int:pk>/", views2.person_name_change, name="person_name_change"),
    path("order_pay/<int:pk>/<str:payment_method>",views2.order_pay,name="order_pay"),
    path("child_pay/<int:pk>/",views2.child_pay,name="child_pay"),
    path("login_page/",views2.login_page,name="login_page"),
    path("logout_page/",views2.logout_page,name="logout_page"),


]
