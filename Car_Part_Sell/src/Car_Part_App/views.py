from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, TemplateView, View
from django.core.mail import send_mail
from .models import CarModel, CarPart, CarPartCategory, Cart, Cart_Product
from .forms import Car_Part_Form
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import login


# class based View
class CarListView(ListView):
    model = CarPart
    context_object_name = "parts"
    paginate_by = 2
    queryset = CarPart.objects.all()
    template_name = "Car/PartList.html"

    def get(self, request):
        category_name = request.GET.get("category_name", None)
        print(category_name)
        if category_name == None:
            parts = CarPart.objects.all()
        else:
            parts = CarPart.objects.filter(category=category_name)
        categories = CarPartCategory.objects.all()
        car_model=CarModel.objects.all()
        print(car_model)
        context = {"parts": parts, "categories": categories,"car_model":car_model}
        return render(request, self.template_name, context)


class CarCreateView(CreateView):
    model = CarModel
    template_name = "Car/CarHome.html"
    form_class = Car_Part_Form

    def post(self, request, *args, **kwargs):
        form = Car_Part_Form(request.POST or None, request.FILES)
        if form.is_valid():
            car_part = form.save(commit=False)
            car_part.seller = request.user
            car_part.save()

        return redirect(reverse("Car_Part_App:parts_data"))

    def get(self, request, *args, **kwargs):
        # return redirect(reverse('Car_Part_App:parts_data'))
        if request.user.user_role == 0:
            form = Car_Part_Form()
            context = {"form": form}
            return render(request, self.template_name, context=context)
        else:
            return redirect(reverse("Car_Part_App:index"))


class CarDetailView(DetailView):
    model = CarPart
    template_name = "Car/Car_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        pk = kwargs.get("car_part_id")
        print(pk)
        car_part = CarPart.objects.filter(pk=pk).first()
        if not cart:
            cart = Cart.objects.create(user=user)
        cart_product = Cart_Product.objects.filter(cart=cart, car_part=car_part).first()
        if cart_product:
            cart_product.quantity += 1
            cart_product.save()
        else:
            Cart_Product.objects.create(cart=cart, car_part=car_part)
        return HttpResponseRedirect(
            request.META.get("HTTP_REFERER")
        )  # same page redirect with id:


class shopDetailsView(ListView):
    model = Cart_Product
    context_object_name = "cart_products"
    template_name = "Buyer/shop.html"

    def get_queryset(self):
        cart_id = self.kwargs.get("cart_id")
        cart = get_object_or_404(Cart, id=cart_id)
        return cart.cart_products.all()


# class OrderConfrimView(ListView):
#     model = CarPart
#     template_name = "Buyer/orderconfirm.html"


# def sendmail(request, pk):
#     post = CarModel.objects.get(pk=pk)
#     user = request.user
#     subject = "Order Received"
#     messege = f"Your {post.Car_Part_Name} Part has been Purchased By {user.username}"
#     sender = settings.EMAIL_HOST_USER
#     reciver = {"bela.vnurture@gmail.com"}
#     send_mail(subject, messege, sender, reciver)
#     return render(request, "Buyer/orderconfirm.html")


class IndexView(TemplateView):
    template_name = "Car/index.html"


# class CarModelView(ListView):
#     model = CarModel
#     template_name = "Car/PartList.html"
#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         car_data=CarModel.objects.all()
#         context=super().get_context_data(**kwargs)
#         context["car_data"]=car_data
#         print("=====")
#         print(context)
#         return context

class CartView(TemplateView):
    template_name = "Buyer/cart.html"
    
    def get_context_data(self, **kwargs):
        cart_products = Cart_Product.objects.filter(cart__user=self.request.user, cart__is_paid=False)
        
        context = super().get_context_data(**kwargs)
        context["cart_products"] = cart_products  # Pass the list of cart products to the template
        context["cart_total"]=Cart.objects.filter(user=self.request.user,is_paid=False).first().get_cart_total()
        return context
