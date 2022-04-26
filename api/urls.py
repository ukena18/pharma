from django.urls import path
# import all the views
from . import views2


urlpatterns = [
    # overview
    path("all_paths/", views2.all_paths, name="all_paths"),
    # index page info will give you alot info
    path("", views2.index, name="index_api"),
    # search person api
    path("search_person/", views2.search_person, name="search_person_api"),
    # add person api
    path("add_person/", views2.add_person, name="add_person_api"),

]







