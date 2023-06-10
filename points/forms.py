
from django import forms
from .models import Kid

class KidForm(forms.ModelForm):
    class Meta:
        model = Kid
        fields = ['name', 'points', 'points_from_cash', 'barcode', 'group', ]  


from django import forms

class AddPointsForm(forms.Form):
    barcode = forms.CharField(label='Barcode')

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['points'] = 1
        return cleaned_data

from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['barcode', 'name', 'points_value']
        from django import forms

class CheckoutForm(forms.Form):
    barcode = forms.CharField(label='Barcode', max_length=200)



from django import forms

class BarcodeForm(forms.Form):
    barcode = forms.CharField(max_length=200)

class PurchaseForm(forms.Form):
    product_barcode = forms.CharField(max_length=200)

from django import forms
from .models import Product

class PurchaseForm(forms.Form):
    product_barcode = forms.CharField()

class AddMoneyForm(forms.Form):
    cash = forms.DecimalField(required=False)
    
class ProductBarcodeForm(forms.Form):
    barcode = forms.CharField(max_length=200)


from .models import Kid, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['barcode', 'name', 'points_value']

from django import forms

class CheckoutForm(forms.Form):
    barcode = forms.CharField(label='Barcode', widget=forms.TextInput(attrs={'class': 'form-input'}))
    points_type = forms.ChoiceField(choices=[('points', 'Points'), ('points_from_cash', 'Points From Cash')], widget=forms.Select(attrs={'class': 'form-input'}))

from django import forms
from .models import Product

class PurchaseForm(forms.Form):
    product_barcode = forms.CharField(required=False)


class AddCashForm(forms.Form):
    amount = forms.DecimalField(initial=0, required=True)





