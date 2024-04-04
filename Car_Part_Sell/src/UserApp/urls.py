from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import SignupView,custom_logout,OrderView


app_name = "UserApp"

urlpatterns = [

    path('',include('django.contrib.auth.urls')),
    path("signup/", SignupView.as_view(), name="signup"),
    #path("signup/buyer", BuyerSignUpView.as_view(), name="buyer_signup"),
    #path("signup/seller",SellerSignUpView.as_view(), name="seller_signup"),
    path("login/", auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    #path("login_temp/", LoginTempView.as_view(), name='login_temp'),
    path("orderconfirm/", OrderView.as_view(), name='orderconfirm'),
    path("orderconfirm/<int:pk>", OrderView.as_view(), name='orderconfirm'),
  

]