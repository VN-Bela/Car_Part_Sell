from . import views

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Car_Part_App'

urlpatterns = [

    path('', views.IndexView.as_view(), name="index"),
    path('part_list/', views.CarListView.as_view(), name="Data"),
   # path('car_model/', views.CarModelView.as_view() ,name="car_model"),
    path('parts_data/', views.CarCreateView.as_view(), name='parts_data'),
    path("car_detail/<int:pk>/", views.CarDetailView.as_view(), name="car_detail"),
    path("addcart/<int:car_part_id>/", views.AddToCartView.as_view(), name="addcart"),
    path("shop/<int:cart_id>/", views.shopDetailsView.as_view(), name="shop"),
    #path("Orderconfirm/<int:pk>", views.sendmail, name="Orderconfirm"),
    path("cart/", views.CartView.as_view(), name="cart"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
