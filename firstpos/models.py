from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from .fields import PositiveDecimalFromOneField
from django.urls import reverse_lazy,reverse
from accounts.models import Outlets, OutletStaff
#from accounts.models import CustomUser

# Create your models here.
class Category(models.Model):
	user=models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	name=models.CharField(max_length=100, blank=True, null=True)
	#category=models.CharField(choices= CATEGORY_LISTS, max_length=100, blank=True, null=True)

	def __str__(self):
		return f"{self.name}"
	def get_absolute_url(self) :
		return reverse('detail_updateview', args=(str(self.id)))
    
class ProductList(models.Model):
	user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
	#outlet=models.ForeignKey(Outlets, on_delete=models.SET_NULL, null=True)
	product_name=models.CharField(max_length=100)
	#sold_In=models.ForeignKey('Measurement',on_delete=models.SET_NULL, blank=True,null=True)
	#sold_In=models.CharField(max_length=60, blank=True,null=True)
	sold_In=models.ForeignKey('Measurement',on_delete=models.SET_NULL, blank=True,null=True)
	cost_price=models.DecimalField(default=0, decimal_places=2, max_digits=8)
	selling_price=models.DecimalField(default=0, decimal_places=2, max_digits=8)
	#images= models.ImageField(null=True,blank=True,upload_to=image_upload_to)
	#selling_price=models.DecimalField(default=0, decimal_places=2, max_digits=8)
	stock_inventory=models.DecimalField(default=0, decimal_places=1, max_digits=100, blank=True, null=True)
	category=models.ForeignKey(Category, on_delete=models.SET_NULL , blank=True, null=True)
	

	def __str__(self):

		return f"{self.product_name} | {self.cost_price}"
	def get_absolute_url(self) :
          return reverse('detail_updateview', args=(str(self.id)))
          #return reverse('index')

	
	#def get_total_quantity_sold(self):
	#	total_quantity_sold = 0

       
	#	for product_order in self.productlisto_set.all():
	#		total_quantity_sold += product_order.Quantity

	#	return total_quantity_sold
class ProductListO(models.Model):
	user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
	product=models.ForeignKey(ProductList,on_delete=models.CASCADE)
	
	#sold_In=models.CharField(max_length=60, blank=True,null=True)
	#cost_price=models.DecimalField(default=0, decimal_places=2, max_digits=8)
	
	Quantity=PositiveDecimalFromOneField(max_digits=3, decimal_places=1)
	#category=models.ForeignKey(Category, on_delete=models.SET_NULL , blank=True, null=True)
	description=models.CharField(max_length=300, null=True, blank=True)
	date=models.DateTimeField(default=timezone.now)
	paid=models.BooleanField(default=False)
	#stock_inventory=models.ForeignKey('StockInventory', on_delete=models.SET_NULL, blank=True, null=True)

	def save(self, *args, **kwargs):
		if self.Quantity > 0:
            # Subtract from stock_inventory only if Quantity is greater than 0
			self.product.stock_inventory -= self.Quantity / 2
			self.product.save()
		super(ProductListO, self).save(*args, **kwargs)


	
	def __str__(self):

		return f"{self.product} | {self.product.selling_price} per {self.product.sold_In}"
	def get_absolute_url(self) :
          return reverse('detail_updateview', args=(str(self.id)))
          #return reverse('index')
	def cost_price(self):
		return self.product.cost_price * self.Quantity
	def price(self):
		return self.product.selling_price * self.Quantity



	
class SalesReceipt(models.Model):

	user=models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

	products=models.ManyToManyField(ProductListO)
	#products=models.ForeignKey(ProductList, on_delete=models.CASCADE)
	#products = models.ManyToManyField(ProductList)
	#Quantity=PositiveDecimalFromOneField(max_digits=3, decimal_places=1)
	Remarks=models.TextField(max_length=200, null=True, blank=True)
	date=models.DateTimeField(default=timezone.now)
	payment_option=models.ForeignKey('PaymentOptions', on_delete=models.SET_NULL, blank=True, null=True)
	paymentT= models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
	Note=models.CharField(max_length=100, blank=False, null=False)
	
	issued=models.BooleanField(default=False)

	def __str__(self):
		return f"{self.user} | {self.products} - {self.date}"
	def get_total_amount_onRCost(self):
		total_cost_price=0

		for y in self.products.all():
			total_cost_price += y.cost_price()
			return total_cost_price
	def get_total_amount_onR(self):
		total=0
		for x in self.products.all():
			total +=x.price()
		return total
	
class Measurement(models.Model):
	user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
	name=models.CharField(max_length=30)
	value=models.DecimalField(default=1, decimal_places=4, max_digits=5, null=True, blank=True)
	SI_Units=models.CharField(max_length=5, null=True, blank=True)

	def __str__(self):
		return f" {self.name}"
	def get_absolute_url(self) :
 		return reverse('mdetail_updateview', args=(str(self.id)))
class Payment(models.Model):
     user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
     payment_option=models.ForeignKey('PaymentOptions',on_delete=models.SET_NULL, blank=True, null=True)
     Payemntfor_receipt=models.ForeignKey(SalesReceipt, on_delete=models.SET_NULL, blank=True, null=True)
     Amount_tenderd=models.DecimalField(default=0, decimal_places=3, max_digits=8, blank=True, null=True)
     
     time=models.DateTimeField(auto_now=True)
     amount=models.DecimalField(default=0, decimal_places=3, max_digits=8, blank=True, null=True)

     def __str__(self):
          return f"{self.user} {self.amount} |{self.payment_option}"
     def balance(self):
     	Total_bal=self.Amount_tenderd - self.amount
     	return Total_bal
class PaymentOptions(models.Model):
	user=models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	name=models.CharField(max_length=50, null=True, blank=True)

	def __str__(self):
		return f"{self.name}"
class StockInventory(models.Model):
	user=models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	stock_inventory=PositiveDecimalFromOneField(max_digits=10, decimal_places=2)
	products=models.ForeignKey(ProductList, on_delete=models.CASCADE)


	def __str__(self):

		return f"{self.user} {self.amount} |{self.stock_inventory}"


	def stockInventory(self):
		total_inventory=stock_inventory - products.Quantity

		return total_inventory