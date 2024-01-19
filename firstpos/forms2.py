from django import forms
from django.db import models
from django.contrib.auth.models import User
#from .models import ProductList,Measurement,Category,SalesReceipt,Payment,PaymentOptions
CATEGORY_LISTS= {
     ('No category','No category'),
     }

#class ProductUpdateForm(forms.ModelForm):
 #   class Meta:
       # model = ProductList
        #fields = ('product_name','sold_In','cost_price','selling_price','category','description')

        #widgets = {


    	'product_name':forms.TextInput(attrs={'class':'form-control'}),
    	'sold_In' : forms.Select( attrs={'class':'form-control'}),
    	'cost_price':forms.TextInput(attrs={'class':'form-control'}),
    	'selling_price':forms.TextInput(attrs={'class':'form-control'}),
    	'category': forms.Select(attrs={'class':'form-control'}),
    	'description' :forms.TextInput(attrs={'class':'form-control'}),
    	#}
    #def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProductUpdateForm, self).__init__(*args, **kwargs)
        self.fields['sold_In'].queryset = Measurement.objects.filter(user=user)
        self.fields['category'].queryset=Category.objects.filter(user=user)
#class ProductForm(forms.ModelForm):

 #   class Meta:
        model = ProductList
        fields = ('product_name','sold_In','cost_price','selling_price','category','description')


  #      widgets = {


		'product_name':forms.TextInput(attrs={'class':'form-control'}),
		'sold_In' : forms.Select( attrs={'class':'form-control'}),
		'cost_price':forms.TextInput(attrs={'class':'form-control'}),
		'selling_price':forms.TextInput(attrs={'class':'form-control'}),
		'category': forms.Select(attrs={'class':'form-control'}),
		'description' :forms.TextInput(attrs={'class':'form-control'}),
	#	}
    #def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['sold_In'].queryset = Measurement.objects.filter(user=user)
            self.fields['category'].queryset=Category.objects.filter(user=user)

        
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
        exclude = ('user', 'date', 'payment_option', 'payment')

        widgets = {

        'products' :forms.Select( attrs={'class':'form-control'}),
        #'Quantity' :
        'Remarks' : forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateReceiptForm, self).__init__(*args, **kwargs)
        self.fields['products'].queryset = ProductList.objects.filter(user=user)
class CreateReceiptFormUp(forms.ModelForm):
    class Meta:
        model = SalesReceipt
        exclude = ('user','date','payment_option','payment')

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