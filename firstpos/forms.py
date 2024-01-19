from django import forms
from django.db import models
from django.contrib.auth.models import User
from .models import ProductList,ProductListO,Measurement,Category,SalesReceipt,Payment,PaymentOptions
from .fields import PositiveDecimalFromOneField
CATEGORY_LISTS= {
     ('No category','No category'),
     }

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = ProductList
        fields = ('product_name','cost_price','category',)

        widgets = {


    	'product_name':forms.TextInput(attrs={'class':'form-control'}),
    	#'sold_In' : forms.Select( attrs={'class':'form-control'}),
    	'cost_price':forms.TextInput(attrs={'class':'form-control'}),
    	#'selling_price':forms.TextInput(attrs={'class':'form-control'}),
    	'category': forms.Select(attrs={'class':'form-control'}),
    	#'description' :forms.TextInput(attrs={'class':'form-control'}),
    	}
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProductUpdateForm, self).__init__(*args, **kwargs)
        #self.fields['sold_In'].queryset = Measurement.objects.filter(user=user)
        self.fields['category'].queryset=Category.objects.filter(user=user)
class ProductForm(forms.ModelForm):

    class Meta:
        model = ProductList
        fields = ('product_name','cost_price','selling_price','category','sold_In', 'stock_inventory')


        widgets = {


		'product_name':forms.TextInput(attrs={'class':'form-control'}),
		'sold_In' : forms.Select( attrs={'class':'form-control'}),
		'cost_price':forms.TextInput(attrs={'class':'form-control'}),
		'selling_price':forms.TextInput(attrs={'class':'form-control'}),
		'category': forms.Select(attrs={'class':'form-control'}),
        'stock_inventory' : forms.NumberInput(attrs={'class':'form-control'}),
		#'description' :forms.TextInput(attrs={'class':'form-control'}),
		}
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        sold_in_queryset = Measurement.objects.filter(user=user)
        if not sold_in_queryset.filter(name='Each').exists():
        #if not sold_in_queryset.exists():
            default_measurement = Measurement(name='Each', user=user)
            default_measurement.save()
            sold_in_queryset = Measurement.objects.filter(user=user)

        if user:
            #self.fields['sold_In'].queryset = Measurement.objects.filter(user=user)
            self.fields['sold_In'].queryset = sold_in_queryset
            self.fields['category'].queryset=Category.objects.filter(user=user)


class ProductFormO(forms.ModelForm):

    class Meta:
        model = ProductListO
        fields = ('Quantity','description',)


        widgets = {


        #'product_name':forms.TextInput(attrs={'class':'form-control'}),
        #'sold_In' : forms.Select( attrs={'class':'form-control'}),
    #    'cost_price':forms.TextInput(attrs={'class':'form-control'}),
        #'selling_price':forms.TextInput(attrs={'class':'form-control'}),
        #'category': forms.Select(attrs={'class':'form-control'}),
        'description' :forms.TextInput(attrs={'class':'form-control'}),
        }
    #
        
class PayOptionsForm(forms.ModelForm):
    class Meta:
        model = PaymentOptions
        fields = ('name',)

        widgets = {


        'name':forms.TextInput(attrs={'class':'form-control'}),
            }
    
class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ('name','value','SI_Units')

        widgets = {


        'name':forms.TextInput(attrs={'class':'form-control'}),
        'value' : forms.TextInput(attrs={'class':'form-control'}),
        'SI_Units':forms.TextInput(attrs={'class':'form-control'}),
        }
class MeasureUpdateForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ('name','value','SI_Units')

        widgets = {


        'name':forms.TextInput(attrs={'class':'form-control'}),
        'value' : forms.TextInput(attrs={'class':'form-control'}),
        'SI_Units':forms.TextInput(attrs={'class':'form-control'}),
        }
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
    
        widgets = {
    

        'name':forms.TextInput(attrs={'class':'form-control'}),
        }
class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
    
        widgets = {
    

        'name':forms.TextInput(attrs={'class':'form-control'}),
        }
class CreateReceiptForm(forms.ModelForm):
    class Meta:
        model = SalesReceipt
        exclude = ('user', 'date','products', 'payment')

        widgets = {

        'products' :forms.Select( attrs={'class':'form-control'}),
        #'Quantity' :
        'Remarks' : forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateReceiptForm, self).__init__(*args, **kwargs)
        self.fields['products'].queryset = ProductList.objects.filter(user=user)
class ReceiptForm(forms.ModelForm):
    class Meta:
        model = SalesReceipt
        exclude = ('user', 'date','products', 'payment', 'Remarks', 'issued', 'Note','Amount_tenderd')

        widgets = {

        'payment_option' :forms.Select( attrs={'class':'form-control'}),
        #'Quantity' :
        'Remarks' : forms.TextInput(attrs={'class':'form-control'}),
        }

class ReceiptFormU(forms.ModelForm):   
    class Meta:
        model = SalesReceipt
        exclude = ('user', 'date','products', 'payment', 'Remarks', 'issued', 'Note','payment_option')

    

        
class CreateReceiptFormUp(forms.ModelForm):
    class Meta:
        model = SalesReceipt
        exclude = ('user','date','payment')

        widgets = {

        'products' :forms.Select( attrs={'class':'form-control'}),
        #'Quantity' :
        'Remarks' : forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateReceiptFormUp, self).__init__(*args, **kwargs)
        self.fields['products'].queryset = ProductList.objects.filter(user=user)


class PaymentFormUp(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ('user', 'date','products','amount')

        widgets = {

        'payment_option' :forms.Select( attrs={'class':'form-control'}),
        #'Quantity' :
        'amount' : forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PaymentFormUp, self).__init__(*args, **kwargs)
        self.fields['payment_option'].queryset = PaymentOptions.objects.filter(user=user)
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment

        exclude = ('user', 'date','products','amount',)

        widgets = {

        'payment_option' :forms.Select( attrs={'class':'form-control'}),
        #'Quantity' :
        'Amount_tenderd' : forms.NumberInput(attrs={'class':'form-control'}),
        }

class OutletStaffSignInForm(forms.Form):

    Unique_id=forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    

