from django.urls import path
# import all the views form api app
from . import views
# all login views apis
from . import auth_views
#rest frame work login simple jwt login
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # overview
    path("", views.all_paths, name="all_paths"),
    # index page info will give you alot info
    path("homepage/", views.homepage, name="homepage_api"),
    # search person api
    path("search/", views.search, name="search_api"),
    # add person api

    path("person_add/", views.person_add, name="person_add_api"),
    path("profile/<int:pk>", views.profile, name="profile_api"),
    path("order_add/<int:pk>", views.order_add, name="order_add_api"),
    path("name_change/", views.name_change, name="name_change_api"),
    path("order_pay/", views.order_pay, name="order_pay_api"),
    path("child_pay/", views.child_pay, name="child_pay_api"),


    # login and log out page
    #check login_views
    path("login_page/", auth_views.login_page, name="login_page_api"),
    path("logout_page/", auth_views.logout_page, name="logout_page_api"),


    # simple jwt-token access token refresh
    # i customize it check auth_views.py of api app
    path('token/', auth_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # this one from django i did not write code for that 
    # it is biult-in
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]







