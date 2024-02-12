from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .models import CustomUser,Outlets,OutletStaff,OutletStaffLogin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
#from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from .tokens import account_activation_token
from .forms import UserUpadetEmailForm,EmailAuthenticationForm,UserUpdateForm,UserRegisterForm,PasswordResetForm1,SetPasswordForm1,UserUpdateSettingsForm,OutletForm,OutletStaffForm,OutletStaffLoginForm,StaffValidityForm
from .decorators import email_verified_required
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from .decorators import email_verified_required
from django.views.generic import View, ListView,CreateView,DetailView,UpdateView,View,DeleteView





from django.contrib.auth.forms import AuthenticationForm


def login_user(request):
	form = EmailAuthenticationForm()
	if request.method == 'POST':
		form = EmailAuthenticationForm(request, request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(request, email=email, password=password)
			if user is not None:
				if user.email_verified:
					login(request, user)
					print('login success')
					#messages.success(request, ("Logged in successful..."))
					return redirect('index')
				else:
			
					login(request, user)
					print('Account is not active. Check your email for activation instructions')
					messages.error(request, "Account is not active. Check your email for activation instructions.")
					return redirect('email_confirmation')
			else:
				#user is None
				print('please check and email address and password')
				messages.error(request, ("please check email address and password..."))
				return redirect('login')
               
	return render(request, 'accounts/login2.html', {'form': form})

#def login_user(request):
#	user=get_user_model()
#	if request.method=="POST":
		
#		username=request.POST['username']
#		password=request.POST['password']
#		user=authenticate(request, username=username, password=password )
#		if user is not None: 
#			if user.email_verified:
#				login(request, user)
#				print('login success')
				#messages.success(request, ("Logged in successful..."))
#				return redirect('index')
#			else:
			
#				login(request, user)
#				print('Account is not active. Check your email for activation instructions')
#				messages.error(request, "Account is not active. Check your email for activation instructions.")
#				return redirect('email_confirmation')
#		else:
#			#user is None
#			print('please check and email address and password')
#			messages.error(request, ("user does not exist..."))
#			return redirect('login')
		 
		
				
#	return render(request, 'login.html' )
def activate(request, uidb64, token):
	User=get_user_model()

	try:
		uid=force_str(urlsafe_base64_decode(uidb64))
		user= User.objects.get(pk=uid)
	except:
		user= None
	if user is not None and account_activation_token.check_token(user, token):
		user.email_verified=True
		user.save()
		messages.success(request, 'Thank you for your email comfirmation, Please log in')
		return redirect('login')
	else:
		messages.error(request, 'Activation link is invalid')

	return redirect('index')

def activateEmail(request, user, to_email):
	mail_subject = 'Activate your user account.'
	message= render_to_string("accounts/template_activate_account.html",
		{
			'user': user.username,
			'domain': get_current_site(request).domain,
			'uid': urlsafe_base64_encode(force_bytes(user.pk)),
			'token': account_activation_token.make_token(user),
			'protocol': 'https' if request.is_secure() else 'http',

		}

		)
	email= EmailMessage(mail_subject, message, to=[to_email])
	if email.send():
		return redirect('email_confirmation')
		#messages.success(request, f'Please check your email to complete your resgistration. N.B check your spam folder')

	else:
		messages.error(request, f'Problem sending email to {to_email}, check if you type it correctly')


def Register(request):
	form=UserRegisterForm
	user=get_user_model()
	if request.method=='POST':
		form=UserRegisterForm(request.POST)
		if form.is_valid():
			
			user=form.save(commit=False)
			user.is_active=True
			user.email_verified=False
			user.save()
			email=form.cleaned_data['email']
			username= form.cleaned_data['email']
			password= form.cleaned_data['password1']
			
			user=authenticate(username=username, password=password)
			login(request,user)
			activateEmail(request, user, form.cleaned_data.get('email'))
				#messages.success(request, ('You have been registered...'))
			return redirect('email_confirmation')


	return render(request, 'accounts/register.html', {"form":form})

def EmailConfirmPage(request):
	
	user=get_user_model()
	
	if request.user.is_authenticated:
		user = request.user
		if user.email_verified:
			print('You have already been verified...')
			messages.success(request, ('You have already been verified...'))
			return redirect('index')

		else:
			form=UserUpadetEmailForm(request.POST or None, instance=user )
			if request.method =='POST':
				form=UserUpadetEmailForm(request.POST or None, instance=user )
				if form.is_valid():
					user_email=form.save(commit=False)
					user_email.user=request.user
					user_email.save()
					#email=form.cleaned_data['email']
					print('email email confirmation sent...')
					activateEmail(request, user, form.cleaned_data.get('email'))
					return redirect(request.META.get("HTTP_REFERER"))

	else:
		return redirect('login')
		



	return render(request, 'accounts/email_comfirmation.html', {'form':form })


def logout_user(request):
	logout(request)
	messages.success(request, ('logged out successful...'))
	return redirect('login')






@login_required
@email_verified_required
def Update_ViewProfile(request, pk):


	user=get_object_or_404(CustomUser, pk=pk)
	form=UserUpdateForm(request.POST or None, instance=user)
	if user.id == request.user.id:

		form=UserUpdateForm(request.POST or None, instance=user)
		if request.method=="POST":
			form=UserUpdateForm(request.POST or None,request.FILES, instance=user)
			if form.is_valid():
				user_p=form.save(commit=False)
				user_p.user=request.user
				user_p.save()
				return redirect(request.META.get("HTTP_REFERER"))
		context={
				"form":form,
				'user':user,
		}
		return render(request, 'accounts/My_Profile.html', context)
	else:
		return render(request, '401.html')

#class Settings_Page(ListView):
#	template_name= 'settings_page.html'
#	model = Outlets
@login_required
@email_verified_required
def Settings_Page(request):
	try:

		staff_login = OutletStaffLogin.objects.get(user=request.user) 
		active_staff=staff_login.outlet_staff
		

	
	except OutletStaffLogin.DoesNotExist:
		staff_login=None
		

	outlet_staff = OutletStaff.objects.filter(user=request.user)
	#if staff_login and staff_login.user.id == request.user.id:

	if staff_login:
		context={
				'active_staff':active_staff,
				'staff_login':staff_login,
				'outlet_staff':outlet_staff,
				}

		return render(request, 'accounts/settings_page.html', context)

	else:

		return render(request, 'accounts/settings_page.html')
	#else:

	#	return render(request, 'accounts/settings_page.html')


@login_required
@email_verified_required
def Settings_PageD(request):
	outlet=Outlets.objects.filter(user=request.user)

	


	context={

				'outlet':outlet,

		}

	return render(request, 'accounts/settings_paged.html', context)
	

def OutletStaffListsView(request):
	outlet = OutletStaff.objects.filter(user=request.user)
	#user=CustomUser.objects.get(pk=request.user)
	

	context={

		'outlet':outlet,
		


	}

	return render(request,'outlets/outlet_staffs.html', context)
	
@login_required
@email_verified_required
def OutletStaffUpdateView(request, pk):
	outlet = get_object_or_404(OutletStaff, pk=pk)
	if outlet.user.id == request.user.id:

		form=OutletStaffForm(request.POST or None, instance=outlet, user=request.user)
		if request.method=="POST":
			form=OutletStaffForm(request.POST or None, instance=outlet, user=request.user)
			if form.is_valid():
				user_outlet=form.save(commit=False)
				user_outlet.user=request.user
				user_outlet.save()
				return redirect(request.META.get("HTTP_REFERER"))
		context={
				"form":form,
		}
		return render(request, 'outlets/outlet_staffsUp.html', context)
	else:
		return render(request, '401.html')

@email_verified_required
@login_required
def AddOutletStaff(request):
	
	outlet=OutletStaff.objects.filter(user=request.user)


	form=OutletStaffForm(request.POST, user=request.user)

	
	if request.method=='POST':
		form= OutletStaffForm(request.POST or None, user=request.user)
		if form.is_valid():
			form_staff=form.save(commit=False)
			form_staff.user=request.user

				
			form_staff.save()
			messages.success(request, ('staff added successfully...'))
			return redirect('outlet_staffs')


	context={
				'form':form,
				
				'outlet':outlet,

				}
	return render (request, 'outlets/add_outletStaff.html',context)
	

@login_required
@email_verified_required
def DeleteOutletStaffView(request, pk):
	outlet_staff = get_object_or_404(OutletStaff, pk=pk)
	outlet_staff1=get_object_or_404(OutletStaffLogin, user=request.user)
	print(outlet_staff1.outlet_staff.id)
	print(outlet_staff.id)
	
	user=request.user
	if outlet_staff.user.id == request.user.id:
		if outlet_staff1.outlet_staff.id == outlet_staff.id :
    	

			outlet_staff1.outlet_staff=None
			outlet_staff1.save()
		outlet_staff_de=outlet_staff.delete()

		messages.success(request, 'Employee deleted successfully.')
		return redirect('outlet_staffs')
    	#return redirect(request.META.get("HTTP_REFERER"))
    #return render(request, 'delete_measurement.html', {'measurement': measurement})
	else:
		return render(request, '404.html')

@login_required
@email_verified_required
def OutletStaffLogout(request, pk):
	outlet_staff= OutletStaff.objects.filter(user=request.user)
	outlet_staff1 = OutletStaffLogin.objects.get(pk=pk)
	user=request.user
	if outlet_staff1.user.id == user.id:
		
		outlet_staff1.outlet_staff=None
		outlet_staff1.save()
		messages.success(request, 'signed out successful.')
		return redirect('settings_page')
    	#return redirect(request.META.get("HTTP_REFERER"))
    #return render(request, 'delete_measurement.html', {'measurement': measurement})
	else:
		return render(request, '404.html')


@login_required
@email_verified_required
def Settings_PageD_Update(request, pk):
	outlet=get_object_or_404(Outlets, pk=pk)
	form=UserUpdateSettingsForm(request.POST or None, instance=outlet)
	if outlet.user.id == request.user.id:

		if request.method=="POST":
			form=UserUpdateSettingsForm(request.POST or None, instance=outlet)
			if form.is_valid():
				outletP=form.save(commit=False)
				outletP.user=request.user
				outletP.save()
				return redirect(request.META.get("HTTP_REFERER"))

	else:
		return render(request, '404.html')

	context={
				"form":form,
				'outlet':outlet,
		}

	return render(request, 'accounts/settings_pagedup.html',context)
@login_required
@email_verified_required
def OutletCreatView(request):
	
	outlet=Outlets.objects.filter(user=request.user)
	
	form=OutletForm(request.POST)
	if outlet:

		messages.success(request, ('You can only add one Outlet...'))
		return redirect('settings_paged')

	else:

		if request.method=='POST':
			form= OutletForm(request.POST or None)
			if form.is_valid():
				form_create=form.save(commit=False)
				form_create.user=request.user
				
				form_create.save()
				messages.success(request, ('Outlet added successfully...'))
				return redirect('settings_paged')

		context={
					'form':form,
				
					'outlet':outlet,

				}
	return render (request, 'outlets/create_outlet.html',context)
	

@login_required
@email_verified_required
def DeleteOutlettView(request, pk):
    outlet = get_object_or_404(Outlets, pk=pk)
    user=request.user
    if outlet.user.id == user.id:
    
    	outlet_de=outlet.delete()

    	messages.success(request, 'Outlet deleted successfully.')
    	return redirect('settings_paged')
    	#return redirect(request.META.get("HTTP_REFERER"))
    #return render(request, 'delete_measurement.html', {'measurement': measurement})
    else:
    	return render(request, '404.html')


@login_required
@email_verified_required
def password_change(request):
	user=get_user_model()
	user = request.user
	if request.method == 'POST':
		form = SetPasswordForm1(user, request.POST)
		if form.is_valid():
			form.save()
			logout(request)
			messages.success(request, "Your password has been changed, Please log in again....")
			return redirect('login')
			
        

	form = SetPasswordForm1(user)
	return render(request, 'accounts/password_reset_confirm.html', {'form': form})
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm1(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                  
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly. Check your spam folder.
                        
                        """
                    )
                else:

                    messages.error(request, "Problem sending email, SERVER PROBLEM")
                    return redirect('login')
            else:
            	messages.error(request, "Email does not exists in our database")

            return redirect('accounts/login')



    form = PasswordResetForm1()
    return render(
        request=request, 
        template_name="accounts/password_reset.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm1(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and log in  now.")
                return redirect('login')
            

        form = SetPasswordForm1(user)
        return render(request, 'accounts/password_reset_confirm2.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("login")


@login_required
@email_verified_required
def OutletStaffLoginView(request):
	#outlet_staff1=get_object_or_404(OutletStaff, user=request.user)
	outlet_staff = get_object_or_404(OutletStaffLogin, user=request.user)
	if outlet_staff.user.id == request.user.id:
		form_l=StaffValidityForm(request.POST or None)
		form=OutletStaffLoginForm(request.POST or None, instance=outlet_staff, user=request.user)
		if request.method=="POST":
			form=OutletStaffLoginForm(request.POST or None, instance=outlet_staff, user=request.user)
			form_l=StaffValidityForm(request.POST or None)
			if form.is_valid() and form_l.is_valid():
				employee_id_entered = form_l.cleaned_data.get('Unique_pin')

				if OutletStaff.objects.filter(Employee_id=employee_id_entered).exists():
				 	user_outlet = form.save(commit=False)

				 	user_outlet.user = request.user
				 	user_outlet.save()
				 	messages.success(request, 'sign in successful')
				 	return redirect('staff_Details', pk=outlet_staff.pk)
				else:
				 	messages.error(request, 'Invalid Employee ID Details')

				
				

		context={
				"form":form,
				"form_l":form_l,
		}
		return render(request, 'outlets/outlet_staffsLogin.html', context)
	else:
		return render(request, '401.html')


def OutletStaffDView(request, pk):
	outlet_staff1 = OutletStaffLogin.objects.get(pk=pk)
	#user=CustomUser.objects.get(pk=request.user)
	if outlet_staff1.user.id==request.user.id:

		context={

			'outlet_staff1':outlet_staff1,
		


		}

		return render(request,'outlets/outlet_staffdetails.html', context)
	else:
		return render(request, '404.html')


