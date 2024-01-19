from django.contrib import admin
from .models import Category,ProductList,Measurement,SalesReceipt,Payment,PaymentOptions,ProductListO,StockInventory
# Register your models here.
admin.site.register(ProductList)
admin.site.register(Category)
#admin.site.register(SalesReceipt)
admin.site.register(Measurement)
admin.site.register(SalesReceipt)
admin.site.register(Payment)
admin.site.register(PaymentOptions)
admin.site.register(ProductListO)
admin.site.register(StockInventory)