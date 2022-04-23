from django.urls import path
from . import views2

urlpatterns = [

    path("all_paths/", views2.all_paths, name="all_paths"),
    path("", views2.index, name="index_api"),
    path("search_person/", views2.search_person, name="search_person_api"),
    path("add_person/", views2.add_person, name="add_person_api"),
]






# urlpatterns = [
#
#     path("", views.all_paths, name="all_paths"),
#     path("find_parent/<int:pk>/", views.find_parent, name="find_parent"),
#
#     path("find_children/<int:pk>/", views.find_all_children, name="find_children"),
#     path("customer_total_debt/<int:pk>/", views.customer_total_debt, name="customer_total_debt"),
# ]