from datetime import datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View, ListView,CreateView,DetailView,UpdateView,View,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ProductList,Measurement,Category,SalesReceipt,PaymentOptions,Payment,ProductListO
from django.contrib.auth.models import User
from .forms import ProductUpdateForm,ProductForm,MeasurementForm,CategoryForm,MeasureUpdateForm,CategoryUpdateForm,CreateReceiptForm,CreateReceiptFormUp,PayOptionsForm,PaymentFormUp,ProductFormO,ReceiptForm,ReceiptFormU,PaymentForm,OutletStaffSignInForm
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from accounts.decorators import email_verified_required
from accounts.models import Outlets,OutletStaff,OutletStaffLogin
from django.db.models import Sum
from django.http import QueryDict
from django.utils import timezone
from datetime import timedelta
import calendar
from django.http import FileResponse
import io
from collections import OrderedDict
from django.template.loader import get_template
from django.template import Context
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
@email_verified_required
def HomeView(request):
	producto_list=ProductListO.objects.filter(user=request.user, paid=False)
	product=ProductList.objects.filter(user=request.user)
	

	totalQ=0
	for producto in producto_list:
		productoQ={producto.Quantity}
		
		for x in productoQ:
			totalQ += int(x)

	current_date = timezone.now().date()
	months_in_year = list(calendar.month_name)[1:]
	
	monthly_sales_data = {month: 0 for month in months_in_year}

	Receipt_monthly = SalesReceipt.objects.filter(
    	user=request.user,
    	issued=True,
    	products__date__date__year=current_date.year).order_by('-date')		


	for receipt in Receipt_monthly:
		month_name = receipt.date.strftime('%B')

		if month_name in monthly_sales_data:
			monthly_sales_data[month_name] += receipt.get_total_amount_onR()

	data_for_months = [int(month) for month in monthly_sales_data.values()]
	print(data_for_months)

	
	start_of_week = current_date - timedelta(days=current_date.weekday())
	end_of_week = start_of_week + timedelta(days=6)
	days_of_week = [(start_of_week + timedelta(days=i)).strftime('%A') for i in range(7)]

	daily_sales_data = {day: 0 for day in days_of_week}

	Receipt_day = SalesReceipt.objects.filter(
            user=request.user,
            issued=True,
            products__date__date=current_date,
        ).order_by('-date')
	day_of_week=current_date.strftime('%A')
	Profit=0
	total_priceIna_forday = 0
	total_priceIna_fordayCost=0
	for receipt in Receipt_day:

		total_priceIna_forday += receipt.get_total_amount_onR()
	 
		total_priceIna_fordayCost += receipt.get_total_amount_onRCost()

		Profit= total_priceIna_forday - total_priceIna_fordayCost



	Receipt = SalesReceipt.objects.filter(
            user=request.user,
            issued=True,
            #products__date__date=current_date,
            products__date__date__gte=start_of_week,
            products__date__date__lte=end_of_week
        ).order_by('-date')
	day_of_week=current_date.strftime('%A')
	
	for receipt in Receipt:


		day_of_week = receipt.date.strftime('%A')

		daily_sales_data[day_of_week] += receipt.get_total_amount_onR()

	data_for_days = [int(d) for d in daily_sales_data.values()]

	product_sales=ProductListO.objects.filter(user=request.user).order_by('product')

	context={

		'labels_monthly':months_in_year,
		'data_monthly':data_for_months,
		'labels':days_of_week,
		'data':data_for_days,
		'totalQ':totalQ,
		'producto_list':producto_list,
	
		"total_priceIna_forday":total_priceIna_forday,
		"total_priceIna_fordayCost":total_priceIna_fordayCost,
		"Profit":Profit,
		"current_date":current_date,
		"product_sales":product_sales,
		"product":product
		
		}


	return render(request, 'index.html', context)



	
@method_decorator(login_required, name='dispatch')
@method_decorator(email_verified_required, name='dispatch')
class ProductListsView(LoginRequiredMixin,ListView):
	template_name= 'product_lists.html'
	model = ProductList

@email_verified_required
@login_required
def ProductCreatView(request, pk):
	form=ProductForm(request.POST, user=request.user)
	productList=ProductList.objects.filter(user__id=pk)
	if request.user.id==pk:
		current_user=request.user

		if request.method=='POST':
			form= ProductForm(request.POST or None, user=request.user)
			if form.is_valid():
				
				form_create=form.save(commit=False)
				form_create.user=request.user
				
				form_create.save()
				messages.success(request, ('Product added successfully...'))
				return redirect('product_lists')

		context={
				'form':form,
				
				'productList':productList,

			}
		return render (request, 'create_product.html',context)
@login_required
@email_verified_required
def ProductUpdateView(request, pk):
	productList = get_object_or_404(ProductList, pk=pk)
	if productList.user.id == request.user.id:

		form=ProductForm(request.POST or None, instance=productList, user=request.user)
		if request.method=="POST":
			form=ProductForm(request.POST or None, instance=productList, user=request.user)
			if form.is_valid():
				user_product=form.save(commit=False)
				user_product.user=request.user
				user_product.save()
				return redirect(request.META.get("HTTP_REFERER"))
		context={
				"form":form,
		}
		return render(request, 'detail_updateview.html', context)
	else:
		return render(request, '401.html')

@method_decorator(login_required, name='dispatch')
@method_decorator(email_verified_required, name='dispatch')
class DeleteProductView(DeleteView):
    model = ProductList
    template_name = 'delete_product.html'
    success_url = reverse_lazy('product_lists')

@login_required
@email_verified_required
def MeasurementUpdateView(request, pk):
	measurement = get_object_or_404(Measurement, pk=pk)
	if measurement.user.id == request.user.id:

		form=MeasureUpdateForm(request.POST or None, instance=measurement)
		if request.method=="POST":
			form=MeasureUpdateForm(request.POST or None, instance=measurement)
			if form.is_valid():
				user_measurement=form.save(commit=False)
				user_measurement.user=request.user
				user_measurement.save()
				return redirect(request.META.get("HTTP_REFERER"))
		context={
				"form":form,
				"measurement":measurement,
		}
		return render(request, 'mdetail_updateview.html', context)
	else:
		return render(request, '401.html')

@login_required
@email_verified_required
def MeasurementCreatView(request, pk):
	form=MeasurementForm(request.POST)
	measurement=Measurement.objects.filter(user__id=pk)
	if request.user.id==pk:

		if request.method=='POST':
			form= MeasurementForm(request.POST or None)
			if form.is_valid():
				form_create=form.save(commit=False)
				form_create.user=request.user
				form_create.save()
				messages.success(request, ('Measurement added successfully...'))
				return redirect(request.META.get("HTTP_REFERER"))


		context={
				'form':form,
				'measurement':measurement,

			}
		return render (request, 'create_measurement.html',context)
	else:
		return render (request, '404.html')
#class DeleteMeasurementView(DeleteView):
 #   model = Measurement
  #  template_name = 'delete_product.html'
   # success_url = reverse_lazy('index')
@login_required
@email_verified_required
def DeleteMeasurementView(request, pk):
    measurement = get_object_or_404(Measurement, pk=pk)
    user=request.user
    if measurement.user.id == user.id:
    	if request.method == 'POST':
    		measurement.delete()
    		messages.success(request, 'measurement deleted successfully.')
    		return redirect('create_measure', user.pk)  # Redirect to the post list or any other desired URL
    	return render(request, 'delete_measurement.html', {'measurement': measurement})
    else:
    	return render(request, '404.html')


@login_required
@email_verified_required
def CategoryCreatView(request, pk):

	form=CategoryForm(request.POST)
	category=Category.objects.filter(user__id=pk)
	if request.user.is_authenticated:
		if request.user.id==pk:

			if request.method=='POST':
				form= CategoryForm(request.POST or None)
				if form.is_valid():
					form_create=form.save(commit=False)
					form_create.user=request.user
					form_create.save()
					messages.success(request, ('Category added successfully...'))
					return redirect(request.META.get("HTTP_REFERER"))


			context={
							'form':form,
							'category':category,

					}
			return render (request, 'create_category.html',context)
		else:
			return render (request, '404.html')
	return render (request, '404.html')

@method_decorator(login_required, name='dispatch')
@method_decorator(email_verified_required, name='dispatch')
class CategoryUpdateView(LoginRequiredMixin, UpdateView):

	template_name = 'cdetail_updateview.html'
	form_class = CategoryUpdateForm
	model = Category
	def form_valid(self, form):
		form.instance.user_id = self.request.user.id
		return super().form_valid(form)
@login_required
@email_verified_required
def CategoryDeleteView(request, pk):
    category = get_object_or_404(Category, pk=pk)
    user=request.user
    if category.user.id == user.id:
    	if request.method == 'POST':
    		category.delete()
    		messages.success(request, 'category deleted successfully.')
    		return redirect('create_category' ,user.pk)  
    	return render(request, 'delete_category.html', {'category': category})
    else:
    	return render(request, '404.html')






@login_required
@email_verified_required
def CreateReceipt(request, pk):
	try:

		staff_login = OutletStaffLogin.objects.get(user=request.user.pk) 
		active_staff=staff_login.outlet_staff
		
	except OutletStaffLogin.DoesNotExist:
		staff_login=None
		active_staff = None
	productList=ProductList.objects.filter(user_id=pk)
	
	if active_staff:
		
		context={
					'staff_login':staff_login,
					'active_staff':active_staff,
					'productList':productList,
				
				}
		
		return render(request, 'create_receipt.html', context)
	else:
		messages.success(request, ('Please log in the Employee section to continue ...'))
		return render(request, 'accounts/settings_page.html')


	
	
@login_required
@email_verified_required
def CreateReceiptV(request, pk):
	
	product=get_object_or_404(ProductList, pk=pk)
	totalQ = request.session.get('totalQ', 0)
	current_user=request.user
	
	if product.user.id == current_user.id:

		form = ProductFormO(request.POST or None)
	
		if request.method == 'POST':
			form=ProductFormO(request.POST)

			if form.is_valid():
				
				creator=form.save(commit=False)
				creator.user=request.user
				creator.product=product
				creator.save()
				messages.success(request, ('Receipt added successfully...'))
				#return redirect(request.META.get("HTTP_REFERER"))
				Receipt=SalesReceipt.objects.filter(user=current_user, issued=False)
				if Receipt.exists():
					Receipt_O=Receipt[0]
					Receipt_O.save()
					Receipt_O.products.add(creator)
				else:
					Receipt=SalesReceipt.objects.create(user=current_user)
					Receipt.products.add(creator)
				return redirect('salesrcd2', pk=request.user.id)
				#return redirect('create_receiptV_update', pk=creator.pk)
		context={
			'form':form,
			'product':product,
			'totalQ':totalQ ,
		

			}
		return render(request, 'create_receiptV.html', context)

	else:
		return render(request, '404.html')


@login_required
@email_verified_required
def RemoveProducto(request, pk):
	producto = get_object_or_404(ProductListO, pk=pk)
	user=request.user
	if producto.user.id == user.id:
		
		producto.delete()
		return redirect(request.META.get("HTTP_REFERER"))
    	
	else:
		return render(request, '404.html')



			
	
@login_required
@email_verified_required
def CreateReceiptVUpdate(request, pk):
	
	producto=get_object_or_404(ProductListO ,pk=pk)
	totalQ = request.session.get('totalQ', 0)
	
	current_user=request.user
	if producto.user.id == request.user.id :
		form=ProductFormO(request.POST or None, instance=producto)
		
		
		if request.method=='POST':
			form=ProductFormO(request.POST or None, instance=producto)
			if form.is_valid():
				creatorp=form.save(commit=False)
				creatorp.user=request.user
				creatorp.save()
				print('sucess')
				Receipt=SalesReceipt.objects.filter(user=current_user, issued=False)
				if Receipt.exists():
					Receipt_O=Receipt[0]
					Receipt_O.save()
					Receipt_O.products.add(creatorp)
				else:
					Receipt=SalesReceipt.objects.create(user=current_user)
					Receipt.products.add(creatorp)
				return redirect('salesrcd2', pk=request.user.id)
		
			

				
		context={
				
				'form':form,
				'producto':producto,
				'totalQ':totalQ
			


		}
		return render(request, 'create_receiptUpdateV.html', context )
	else:
		return render(request, '401.html')

@login_required		
@email_verified_required
def SalesReceiptView(request, pk):
	
	products=ProductListO.objects.filter(user__id=pk, paid=False)
	Receipt=SalesReceipt.objects.get(user__id=pk, issued=False)
	
	

	if Receipt.user.id == request.user.id:

		if products.exists():

			initial_amount = Receipt.get_total_amount_onR()
			formpay = PaymentForm(initial={'Amount_tenderd': initial_amount})


			print(initial_amount)
	

			
			if request.method == 'POST':
				formpay=PaymentForm(request.POST or None)
			
				if formpay.is_valid():
					
					
					creatorpay=formpay.save(commit=False)
					creatorpay.user=request.user

					creatorpay.amount=Receipt.get_total_amount_onR()
				
				
					creatorpay.save()
					Receipt.payment=creatorpay
					Receipt.issued=True
					#products.paid=True
					for product in products:
						product.paid=True
						product.save()

					Receipt.save()
				
				print('sucess')
				return redirect('create_receiptS', pk=Receipt.pk)
				
					



			context={
				
			#'form':form,
			'Receipt':Receipt,
			'formpay':formpay

			}
			return render(request, 'salesrcd2.html', context )
		else:
			return redirect('create_receipt', pk=request.user.id)
		

	else:
		return render(request, '401.html')


@login_required
@email_verified_required
def SalesReceiptPdf(request, pk):
	Receipt=get_object_or_404(SalesReceipt ,pk=pk, issued=True)
	#template=get_template('receiptsuccesspdf.html')
	context={
		'Receipt':Receipt,

			}
	template = get_template('receiptsuccesspdf.html')
	rendered_html = template.render(context)
	response = WeasyTemplateResponse(request, template=template, context=context)
	response.content_disposition = 'inline; filename="receiptsuccesspdf.pdf"'

	return response
	


@login_required
@email_verified_required
def AmountTenderdView(request, pk):

	Receipt=get_object_or_404(SalesReceipt, pk=pk, issued=False)

	amount_tenderd=SalesReceipt(
					user=request.user,
					Amount_tenderd=Receipt.get_total_amount_onR(),
					
					)
	
	amount_tenderd.save()
	Receipt.Amount_tenderd=amount_tenderd

	Receipt.save()
	return redirect('salesrcd2', pk=Receipt.pk)
@login_required
@email_verified_required
def AddPayment(request, pk):

	Receipt=get_object_or_404(SalesReceipt, pk=pk, issued=False)

	payment=Payment(
					user=request.user,
					amount=Receipt.get_total_amount_onR(),
					
					)
	
	payment.save()
	Receipt.payment=payment
	Receipt.issued=True
	Receipt.save()
	return redirect('create_receiptS', pk=Receipt.pk)
	payment=PaymentForm(request.POST or None)
	if request.method=='POST':
		payment=PaymentForm(request.POST or None)

@login_required
@email_verified_required
def CreateReceiptUpdate(request, pk):
	paymentoption=PaymentOptions.objects.all()
	Receipt=get_object_or_404(SalesReceipt ,pk=pk)
	#payment=get_object_or_404(ProductList, pk=pk)
	#formP = PaymentFormUp(request.POST or None, user=request.user)
	if Receipt.user.id == request.user.id:
		form=CreateReceiptFormUp(request.POST or None, instance=Receipt, user=request.user)
		formP = PaymentFormUp(request.POST or None, instance=Receipt, user=request.user)
		if request.method=='POST':
			form=CreateReceiptFormUp(request.POST or None, instance=Receipt, user=request.user)
			formP = PaymentFormUp(request.POST or None,instance=Receipt, user=request.user)
			if form.is_valid():
				print(form.cleaned_data)
				

				creatorp=form.save(commit=False)
				creatorp.user=request.user
				creatorp.save()
				print('sucess')
				return redirect(request.META.get("HTTP_REFERER"))

			if formP.is_valid():
				print(form.cleaned_data)
				pform=formP.save(commit=False)
				pform.user=request.user
				#pform.save()
				payment=Payment(
					user=request.user,
					amount=Receipt.total_price(),
					payment_option=pform.payment_option,
					)
				#payment_option=PaymentOptions(
				#	user=request.user,
				#	name=pform.payment_option,
				#	)
				
				payment.save()
				#payment_option.save()
				Receipt.payment=payment
				#Receipt.payment_option=payment_option
				Receipt.save()
				
				print('payment success')
				return redirect(request.META.get("HTTP_REFERER"))
			 
				
		context={
				'formP':formP,
				'form':form,
				'Receipt':Receipt,
				'paymentoption':paymentoption,

		}
		return render(request, 'create_receiptUpdate.html', context )
	else:
		return render(request, '401.html')
@login_required
@email_verified_required
def CreateReceiptSucess(request, pk):
	Receipt=get_object_or_404(SalesReceipt ,pk=pk, issued=True)
	if Receipt.user.id == request.user.id :


		context={
			"Receipt":Receipt,

		}
        
		return render(request, 'create_receiptS2.html', context)
	else:

		return render(request, '404.html')
@login_required
@email_verified_required
def PastReceiptSucess(request, pk):
	Receipt=get_object_or_404(SalesReceipt ,pk=pk, issued=True)
	if Receipt.user.id == request.user.id :


		context={
			"Receipt":Receipt,

		}
        
		return render(request, 'receiptsuccesspdf.html', context)
	else:

		return render(request, '404.html')


		
@login_required
@email_verified_required
def SalesRcListsDel(request, pk):
    Receipt = get_object_or_404(SalesReceipt, pk=pk, issued=True)
    if Receipt.user.id==request.user.id:
    	if request.method == 'POST':
    		Receipt.delete()
    		messages.success(request, 'Receipt deleted successfully.')
    		return redirect('salesrc')
    	return render(request, 'SalesRcListsDel.html', {'Receipt': Receipt})
    else:
    	return render(request, '404.html')

@method_decorator(login_required, name='dispatch')
@method_decorator(email_verified_required, name='dispatch')
class SalesRcDtailView(LoginRequiredMixin,DetailView):
	template_name= 'salesrcd.html'
	model = SalesReceipt



@method_decorator(login_required, name='dispatch')
@method_decorator(email_verified_required, name='dispatch')
class PayOptionsView(LoginRequiredMixin,ListView):
	template_name= 'payoptions.html'
	model = PaymentOptions
@login_required
@email_verified_required
def PayOptionsViewC(request, pk):
	form=PayOptionsForm(request.POST)
	payoptions=PaymentOptions.objects.filter(user__id=pk)
	if request.user.id==pk:
		current_user=request.user

		if request.method=='POST':
			form= PayOptionsForm(request.POST or None)
			if form.is_valid():				
				form_create=form.save(commit=False)
				form_create.user=request.user
				
				form_create.save()
				messages.success(request, ('Payment added successfully...'))
				#return redirect(request.META.get("HTTP_REFERER"))
				return redirect('payoptions')
		context={
				'form':form,
				
				'payoptions':payoptions,

			}
		return render (request, 'create_paymentP.html',context)

@method_decorator(login_required, name='dispatch')
@method_decorator(email_verified_required, name='dispatch')	
class SalesRcListsView(LoginRequiredMixin,View):



	
	def get(self, *args, **kwargs):




		start_date_str = self.request.GET.get('start_date')
		end_date_str = self.request.GET.get('end_date')

		
		 
		start_date = timezone.now().date() if not start_date_str else timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
		end_date = timezone.now().date() if not end_date_str else timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()

		




		Receipts = SalesReceipt.objects.filter(
            	user=self.request.user,
            	issued=True,
            	date__date__gte=start_date,
            	date__date__lte=end_date
			).order_by('-date')

		p=Paginator(Receipts, 20)

	

		page = self.request.GET.get('page')


		

		
		Receipt= p.get_page(page)

		
		number_of_pages = p.get_elided_page_range()

		if Receipt.number <= 10:
			number_of_pages = list(range(1, min(11, p.num_pages + 1)))
		elif Receipt.number > p.num_pages - 8 :
			number_of_pages = list(range(Receipt.paginator.num_pages - 10, p.num_pages + 1))
		else:
			number_of_pages = list(range(Receipt.number - 5, Receipt.number + 5))


		#number_of_pages = [str(page) for page in number_of_pages]

		if number_of_pages[0] != 1:
			number_of_pages = [1, '...'] + number_of_pages
		if number_of_pages[-1] != p.num_pages:
			number_of_pages = number_of_pages + ['...', p.num_pages]

		




		#filter_params = self.request.GET.urlencode()
		context={

					"start_date": start_date,
            		"end_date": end_date,
					"Receipt":Receipt,
					"Receipts":Receipts,
					"number_of_pages":number_of_pages,
					#"filter_params":filter_params,


				}
		#filter_params = QueryDict(self.request.GET.urlencode())
		#context.update(filter_params)
		return render(self.request, 'salesrc.html', context)
@login_required
@email_verified_required
def SalesView(request):

	start_date_str = request.GET.get('start_date')
	end_date_str = request.GET.get('end_date')

		
		 
	start_date = timezone.now().date() if not start_date_str else timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
	end_date = timezone.now().date() if not end_date_str else timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()



	pro = ProductList.objects.filter(
		productlisto__user=request.user,
		
			).distinct()
	totalQ_per_product = []
	#total_sold_n_product={}
	total_sold_n_product = []
		

	for product in pro:

		
		
		totalQ = 0

		item = ProductListO.objects.filter(
            user=request.user,
            product=product.id,
            date__date__gte=start_date,
            date__date__lte=end_date
        )
		h = item.count()
	
		total_sold_n_product.append((product.id, h))
		print(total_sold_n_product)

		for producto in item:
			productQ = {producto.Quantity}

			for x in productQ:
				totalQ += int(x)

		#totalQ_per_product[product.id] = totalQ
		totalQ_per_product.append((product.id, totalQ))
	totalQ_per_product = sorted(totalQ_per_product, key=lambda x: x[1], reverse=True)
		


	

	context={

		'pro':pro,
		'item': item,
		'start_date':start_date,
		'end_date':end_date,
		'totalQ':totalQ,
		'totalQ_per_product':totalQ_per_product,
		'total_sold_n_product':total_sold_n_product,
		'h':h,
		
	
		

		

		}

	return render(request, 'product_sales.html', context)
@login_required
@email_verified_required
def SalesView_byProduct(request, pk):

	start_date_str = request.GET.get('start_date')
	end_date_str = request.GET.get('end_date')

		
		 
	start_date = timezone.now().date() if not start_date_str else timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
	end_date = timezone.now().date() if not end_date_str else timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()

	pro=get_object_or_404(ProductList, pk=pk)

	item=ProductListO.objects.filter(
		user=request.user, 
		product=pro,
		date__date__gte=start_date,
		date__date__lte=end_date,
		)

	h = item.count()

	


	totalQ=0
	Profit=0
	total_price = 0
	total_priceCost=0
	for producto in item:
		productoQ={producto.Quantity}
			
		for x in productoQ:
			totalQ += int(x)

		total_price += producto.price()
		 
		total_priceCost += producto.cost_price()

		Profit= total_price - total_priceCost


			

	current_date = timezone.now().date()

		

	day_of_week=current_date.strftime('%A')
	
	
	#



		#total_product_sales= sales_product.get_total_amount_onR()


	context={

				'item':item,
				'pro':pro,
				'h':h,
				'total_price':total_price,
				'Profit':Profit,
				'total_priceCost':total_priceCost,
				'start_date': start_date,
				'end_date': end_date,
				'totalQ':totalQ,
			

		}
	return render(request, 'product_sale.html', context)
		#return SalesView(request, 'product_sale.html',  totalQ=totalQ, h=h, context=context)




@login_required
@email_verified_required
def PayOptionsViewU(request, pk):
	payoptions = get_object_or_404(PaymentOptions, pk=pk)
	if payoptions.user.id == request.user.id:

		form=PayOptionsForm(request.POST or None, instance=payoptions)
		if request.method=="POST":
			form=PayOptionsForm(request.POST or None, instance=payoptions)
			if form.is_valid():
				user_payment=form.save(commit=False)
				user_payment.user=request.user
				user_payment.save()
				return redirect(request.META.get("HTTP_REFERER"))
		context={
				"form":form,
		}
		return render(request, 'update_paymentU.html', context)
	else:
		return render(request, '401.html')
@login_required
@email_verified_required
def PayOptionsViewD(request, pk):
    payoption = get_object_or_404(PaymentOptions, pk=pk)
    if payoption.user.id==request.user.id:
    	if request.method == 'POST':
    		payoption.delete()
    		messages.success(request, 'payment option deleted successfully.')
    		return redirect('payoptions')  # Redirect to the post list or any other desired URL
    	return render(request, 'delete_paymento.html', {'payoption': payoption})
    else:
    	return render(request, '404.html')

from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors, pdfencrypt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,KeepTogether
from reportlab.platypus.flowables import Image
from reportlab.lib.styles import getSampleStyleSheet
from .models import SalesReceipt
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import HRFlowable



@login_required
@email_verified_required
def generate_sales_receipt_pdf(request, pk):
	Receipt = SalesReceipt.objects.get(pk=pk, issued=True)
	outlet=get_object_or_404(Outlets, user=request.user)
	attending_staff=get_object_or_404(OutletStaffLogin, user=request.user)

	
	custom_page_size = (2.1 * inch, 6 * inch)
	left_margin = 0 * inch
	right_margin =0 * inch
	top_margin = -0.3 * inch
	bottom_margin=0 * inch
	buffer = BytesIO()
	doc = SimpleDocTemplate(buffer, pagesize=custom_page_size,leftMargin=left_margin, rightMargin=right_margin, topMargin=top_margin, bottomMargin=bottom_margin )
	elements = []

	
	


   
	
    # Create a title for the PDF
	
	styles = getSampleStyleSheet()
	title = f"{outlet.name.upper()}"
	title_style = getSampleStyleSheet()['Title']
	title_style.fontSize=10
	title_style.fontName="Times-Bold"
	
	address_style = getSampleStyleSheet()['Normal']
	contact=f"{outlet.phone_number}"
	contact_style=  getSampleStyleSheet()['Normal']
	contact_style.alignment=TA_CENTER
	contact_style.fontSize=8

	Address=f"{outlet.address}"
	address_style.alignment = TA_CENTER
	address_style.fontSize = 8
	address_style.fontName="Times-Bold"

	issued_by =f"&nbsp;&nbsp;&nbsp;ISSUED BY : {attending_staff.outlet_staff.name}"
	issued_by_style=getSampleStyleSheet()['Normal']
	issued_by_style.fontSize = 8
	issued_by_style.fontName="Times-Bold"

	Receipt_id =f"&nbsp;&nbsp;&nbsp;RECEIPT ID : # - 0{Receipt.id}"
	Receipt_id_style=getSampleStyleSheet()['Normal']
	Receipt_id_style.fontSize=8
	Receipt_id_style.fontName="Times-Bold"
	
	time=f"&nbsp;&nbsp;&nbsp;DATE: {Receipt.date.strftime('%Y-%m-%d %H:%M:%S')}"
	time_style=getSampleStyleSheet()['Normal']
	time_style.fontSize=8
	time_style.fontName="Times-Bold"

	Amount_tenderd=" {0}".format( Receipt.payment.Amount_tenderd)  
	Amount_tenderd_style = getSampleStyleSheet()['Normal']
	Amount_tenderd_style.fontSize=9
	Amount_tenderd_style.alignment = 1
	Amount_tenderd_style.fontName='Times-Bold'
	Amount_tenderd_paragraph = Paragraph(Amount_tenderd, Amount_tenderd_style)

	Remarks=f"Thank you for your patronage"
	Remarks_style = getSampleStyleSheet()['Normal']
	Remarks_style.fontSize=8
	Remarks_style.fontName='Times-Bold'
	Remarks_style.alignment= TA_CENTER

	items_details=f" items &nbsp;&nbsp;&nbsp; Qty &nbsp;&nbsp;&nbsp; price  &nbsp;"
	items_details_style=getSampleStyleSheet()['Normal']
	items_details_style.fontSize=9
	items_details_style.fontName = 'Times-Roman'
	for product in Receipt.products.all():
		items=f"{product.product.product_name} &nbsp;&nbsp;&nbsp;{product.Quantity}&nbsp;&nbsp;&nbsp;{product.product.selling_price}  "	
		items_style=getSampleStyleSheet()['Normal']
		items_style.fontSize=9
		items_style.fontName = 'Times-Roman'
    # Create a table to display the receipt data
	receipt_data = [["Product", "Qty", "Price"]]

	for product in Receipt.products.all():
		receipt_data.append([f"{product.product.product_name}", f"{product.Quantity}" , f" {product.price()}"])
	
	#receipt_data.append([])
	#receipt_data.append([])
	
	receipt_table = Table(receipt_data, colWidths=[1.3*inch, 0.3*inch, 0.6*inch])
	receipt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
         ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 15),
        
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('WORDWRAP', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 15), 
	]))

	
	receipt_data_summary = [["","Mode",""]]
	receipt_data_summary.append([f"Total Amount ",f"",Receipt.get_total_amount_onR()])
	receipt_data_summary.append([f" Amount Tendered",f"{Receipt.payment.payment_option}",(Amount_tenderd_paragraph)])
	receipt_data_summary.append([f" Change Due",f"",Receipt.payment.balance()])
	receipt_table_summary = Table(receipt_data_summary, colWidths=[1.3*inch, 0.3*inch, 0.6*inch])
	receipt_table_summary.setStyle(TableStyle([
		('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        #('BOTTOMPADDING', (0, 0), (-1, 0), 15),
         
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('WORDWRAP', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 15), 
        


		]))
	
	
	elements.append(Paragraph(title, title_style))
	elements.append(Paragraph(Address, address_style) )
	elements.append(Spacer(1, 4))
	elements.append(Paragraph(contact, contact_style))
	elements.append(Spacer(1, 7))
	elements.append(HRFlowable(width="100%", thickness=1.5, color="black"))
	elements.append(Spacer(1, 4))
	elements.append(Paragraph(Receipt_id, Receipt_id_style))
	elements.append(Paragraph(time, time_style))
	elements.append(Paragraph(issued_by, issued_by_style))
	
	elements.append(Spacer(1, 7))
	#elements.append(Paragraph(items_details, items_details_style, encoding='utf-8'))
	elements.append(receipt_table)
	elements.append(HRFlowable(width="100%", thickness=1.5, color="black"))
	elements.append(receipt_table_summary)
	
	elements.append(HRFlowable(width="100%", thickness=1.5, color="black"))
	#elements.append(Paragraph(items, items_style))
	elements.append(Spacer(1, 4))
	elements.append(Paragraph(Remarks, Remarks_style))
	elements.append(Spacer(1, 10))
	elements.append(HRFlowable(width="100%", thickness=1.5, color="black"))
	elements.append(Spacer(1, 10))
	doc.build(elements)
	
	

	
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = f'inline; filename="sales_receipt_{pk}.pdf'

	buffer.seek(0)
	response.write(buffer.read())
	buffer.close()
	return response




def sales_chart(request):
    # Sample data
    labels = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
    data = [10, 20, 15, 25, 30]

    context = {
        'labels': labels,
        'data': data,
    }

    return render(request, 'sales/sales_chart.html', context)


		
		

	



	