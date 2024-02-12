from django import forms
from django.db import models
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.core.exceptions import ValidationError
#from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import Outlets, OutletStaff, OutletStaffLogin

class EmailAuthenticationForm(AuthenticationForm):
   # email = forms.EmailField(label='Email', required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    def __init__(self, *args, **kwargs):
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)

        
        

        self.fields['username']=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
        self.fields['username'].label = ''
        #self.fields['username'].widget.attrs.update({
         #   'class': 'form-control',
          #  'placeholder': 'Email',  
        #})

        self.fields['password'].label = ''
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',  
        })


    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
   


class UserRegisterForm(UserCreationForm):
    first_name=forms.CharField(max_length=20,label='First Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name =forms.CharField(max_length=20,label='Last Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    email =forms.EmailField(label='Email',required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    
    
    class Meta:
        model = get_user_model()
        fields = ('first_name','last_name','email','username','password1','password2')

    #def save(self, commit=True):
     #   user = super(UserRegisterForm, self).save(commit=False)
      #  user.email = self.cleaned_data['email']
       # if commit:
        #    user.save()

        #return user


    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
class UserUpadetEmailForm(UserChangeForm):
    #first_name=forms.CharField(max_length=20,label='First Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    #last_name =forms.CharField(max_length=20,label='Last Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    email =forms.EmailField(label='Email',required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    
    
    class Meta:
        model = get_user_model()
        fields = ('email',)

class UserUpdateForm(UserChangeForm):
    first_name=forms.CharField(max_length=20,label='First Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name =forms.CharField(max_length=20,label='Last Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    email =forms.EmailField(label='Email',required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    username =forms.CharField(label='username',required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.ImageField(label='Image', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    password=None
    
    class Meta:
        model = get_user_model()
        fields = ('first_name','last_name','email','username','image')

class PasswordResetForm1(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm1, self).__init__(*args, **kwargs)

class SetPasswordForm1(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm1, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class UserUpdateSettingsForm(forms.ModelForm):
    name=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    email_address=forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class':'form-control'}))
    city=forms.CharField(max_length=50, required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    address=forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number=forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    #staff=forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    Facebook=forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    Instagram=forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    outlet_logo=forms.ImageField(label='Image', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    outlet_description=forms.CharField(max_length=20,  required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    
    
    
    
    class Meta:
        model = Outlets
        exclude = ('user',)


class OutletForm(forms.ModelForm):
    name=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    email_address=forms.EmailField(max_length=60, widget=forms.EmailInput(attrs={'class':'form-control'}))
    city=forms.CharField(max_length=50, required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    address=forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number=forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    #staff=forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    Facebook=forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    Instagram=forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    outlet_logo=forms.ImageField(label='Image', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    outlet_description=forms.CharField(max_length=20,  required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    
    
   
    
    
    class Meta:
        model = Outlets
        exclude = ('user',)

class OutletStaffForm(forms.ModelForm):


    #outlet=forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    name=forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class':'form-control'}))
    address=forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number=forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    #status=forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(label='Email',required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    Employee_id=forms.CharField(max_length=4,  required=True,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    description=forms.CharField(max_length=20,  required=False,widget=forms.TextInput(attrs={'class':'form-control'}))

    
    
    
    
    
    class Meta:
        model = OutletStaff
        exclude = ('user',)

        widgets = {


        'outlet': forms.Select( attrs={'class':'form-control'}),
        'status' : forms.Select( attrs={'class':'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OutletStaffForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['outlet'].queryset = Outlets.objects.filter(user=user)

class OutletStaffLoginForm(forms.ModelForm):

    
    
    class Meta:
        model = OutletStaffLogin
        exclude = ('user','date',)

        widgets = {


        'outlet_staff': forms.Select( attrs={'class':'form-control', 'placeholder':'Choose Employee'}),


        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OutletStaffLoginForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['outlet_staff'].queryset = OutletStaff.objects.filter(user=user)
        self.fields['outlet_staff'].label = ''
        #self.fields['outlet_staff'].choices = [('', 'Select Outlet Staff')] + list(self.fields['outlet_staff'].choices)

    def clean(self):
        cleaned_data = super().clean()
        outlet_staff = cleaned_data.get('outlet_staff')

        if not outlet_staff:
            raise ValidationError("Please select an outlet staff.")

        return cleaned_data

class StaffValidityForm(forms.Form):

    
    Unique_pin=forms.CharField(max_length=4,label='', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Pin to Log in'}))
    