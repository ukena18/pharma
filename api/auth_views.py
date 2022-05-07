# for api views
from rest_framework.decorators import api_view
# to response with json format
from rest_framework.response import Response
# all authentication built-in funcs provided by django
from django.contrib.auth import authenticate, login, logout
# simple-jwt authentication it gives you tokens they are pre-built class-base views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView




@api_view(["POST", "GET"])
def login_page(request):
    # post request for login page
    if request.method == "POST":
        # get the email and password from post data
        email = request.data["email"]
        password = request.data["password"]
        # try to authenticate and login
        try:
            # authenticate check if the email and password is valid
            user = authenticate(request, email=email, password=password)
            if user:
                try:
                    #login the user
                    login(request, user)
                    return Response({"response": "successful login", "status": "true"})
                except :
                    return Response({"response": "fail to login", "status": "false"})
        except:
            return Response({"response": "fail to authenticate", "status": "false"})

    return Response({"login": "login Required",
                     "sample": {"email": "zackberge18@gmail.com", "password": "zackme12"}})


@api_view(["GET"])
def logout_page(request):

    # logout the user
    # is authenticated means if user logged in or not
    # if you use request.user only it will give anonymoususer so this means there is user 
    # just don't use request.user
    if request.user.is_authenticated:
        # it is pre-built func just logut(request)
        # django automatically logout the user
        logout(request)
        return Response({"response": "success to logout", "status": "true"})

    # if there is no authenticated user it gives error 
    return Response({"response": "fail to logout", "status": "false"})



# pre-vuilt class base views
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # to configure the token 
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.user_name
        

        return token

# that is what we will use for custom tokens
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer