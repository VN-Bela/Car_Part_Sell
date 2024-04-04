from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView
from django.views import View
from django.contrib.auth import logout
from django.urls import reverse
from .forms import SellerSignUpFrom, BuyerSignupForm
from .models import User
from Car_Part_App.models import Cart
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
import razorpay



# Create your views here.
# Signup View
class SignupView(TemplateView):
    template_name = 'registration/signup.html'

# Userview
class BuyerSignUpView(CreateView,UserPassesTestMixin):

    model = User
    form_class = BuyerSignupForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_role'] = 'Buyer'
        return super().get_context_data(**kwargs)


    def test_func(self):
        role = self.get_object()
        if self.request.user == role.Buyer:
            return True
        return False


class LoginTempView(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.user_role == 0:
            return redirect(reverse('Car_Part_App:Data'))
        else:
            return redirect(reverse('Car_Part_App:Data'))


# seller Signup
class SellerSignUpView(CreateView):
    model = User
    form_class = SellerSignUpFrom
    template_name = "registration/signup.html"

    # to get user type
    def get_context_data(self, **kwargs):
        kwargs['user_role'] = 'Seller'
        return super().get_context_data(**kwargs)

    # def form_valid(self, form):
    #      user = form.save()
    #      return redirect('Car_Part_App:CarCreateView')
    def test_func(self):
        role = self.get_object()
        if self.request.user == role.Seller:
            return True
        return False

def custom_logout(request):
    print("====================")
    logout(request)
    print("====================")
    return HttpResponseRedirect("login/")  # Redirect to login page after logout


class OrderView(View):
    def get(self, request, pk):
        order = Cart.objects.filter(pk=pk).first()

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        data = {
            "amount": int(order.cart.get_cart_total())* 100,
            "currency": "INR",
            "receipt": "order_rcptid_11",
        }
        payment = client.order.create(data=data)
        print(payment)
        order.order_id = payment["id"]
        order.save()
        context = {"payment": payment}

        return render(request, "Buyer/cart.html", context=context)