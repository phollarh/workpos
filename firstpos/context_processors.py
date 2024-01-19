from django.contrib.auth.decorators import login_required
from django.utils.functional import SimpleLazyObject
from .models import ProductListO,ProductList

def total_quantity(request):
    if request.user.is_authenticated:
        producto_list=ProductListO.objects.filter(user=request.user, paid=False)
        totalQ=0
        for producto in producto_list:
            productoQ={producto.Quantity}
        
            for x in productoQ:
                totalQ += int(x)
    else:
        totalQ = 0
    return {'totalQ': totalQ}

total_quantity_lazy = total_quantity

from datetime import datetime

def current_year(request):
    return {'current_year': datetime.now().year}




