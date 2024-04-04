from django.forms.utils import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User
from django import forms


# seller signup form

class SellerSignUpFrom(UserCreationForm):
    email = forms.EmailField(max_length=255)

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_role = 0
        user.email = self.cleaned_data.get('email')
        user.save()
        if commit:
            user.save()
        return user


# UserApp signup from
class BuyerSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=255)
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self):
        with transaction.atomic():
            user = super().save(commit=False)
            user.user_role = 1
            user.email = self.cleaned_data.get('email')
            user.save()
            # UserApp = Buyer.objects.create(UserApp=UserApp)
            # email
            return user
        # car=Car.objects.create(UserApp=UserApp)
        # car.interests.add(*self.cleaned_data.get('interests'))
