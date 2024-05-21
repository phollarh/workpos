from django.urls import path
from . import views
from .views import HomeView,ProductListsView,ProductCreatView,ProductUpdateView,MeasurementCreatView,CategoryCreatView,MeasurementUpdateView,CategoryUpdateView,CreateReceipt,CreateReceiptUpdate,SalesRcListsView,SalesRcDtailView,CreateReceiptSucess,PayOptionsView,PayOptionsViewC,PayOptionsViewU,DeleteProductView,DeleteMeasurementView,CategoryDeleteView,PayOptionsViewD,CreateReceiptV,CreateReceiptVUpdate,SalesReceiptView,AddPayment,SalesRcListsDel,AmountTenderdView,RemoveProducto,PastReceiptSucess,SalesReceiptPdf,generate_sales_receipt_pdf

urlpatterns = [
    path('',HomeView, name='index'),
    path('product_lists/', ProductListsView.as_view(), name='product_lists'),
    path('product_lists/<int:pk>/delete_product', DeleteProductView.as_view(), name='delete_product'),
    path('payoptions/', PayOptionsView.as_view(), name='payoptions'),
    path('payoptionsC/<int:pk>', PayOptionsViewC, name='payoptionsC'),
    path('payoptions/<int:pk>/update_paymentU', PayOptionsViewU, name='update_paymentU'),
    path('payoptions/<int:pk>/remove', PayOptionsViewD, name='payoption_delete'),
    path('create_product/<int:pk>', ProductCreatView, name='create_product'),
    path('create_measure/<int:pk>', MeasurementCreatView, name='create_measure'),
    path('create_measure/<int:pk>/delete_measurement', DeleteMeasurementView, name='delete_measurement'),
    
    path('create_category/<int:pk>',CategoryCreatView, name='create_category'),
    path('create_category/<int:pk>/remove',CategoryDeleteView, name='delete_category'),
    path('product_lists/<int:pk>/detail_updateview', ProductUpdateView, name='detail_updateview'),
    path('mdetail_updateview/<int:pk>', MeasurementUpdateView, name='mdetail_updateview'),
    path('cdetail_updateview/<int:pk>', CategoryUpdateView.as_view(), name='cdetail_updateview'),
    path('create_receipt/<int:pk>', CreateReceipt, name='create_receipt'),
    path('create_receiptV/<int:pk>', CreateReceiptV, name='create_receiptV'),
    path('create_receiptV/<int:pk>/update', CreateReceiptVUpdate, name='create_receiptV_update'),
    path('create_receiptup/<int:pk>', CreateReceiptUpdate, name='create_receiptup'),
    path('create_receiptup/<int:pk>/sucess', CreateReceiptSucess, name='create_receiptS'),
    path('create_receiptup/<int:pk>/past_receiptS', PastReceiptSucess, name='past_receiptS'),
    path('create_receiptup/Delete', SalesRcListsDel, name='Delete_receiptS'),
    path('add_product', views.add_product, name='add_product'),
    path('salesrc/', SalesRcListsView.as_view(), name='salesrc'),
    path('salesrc/<int:pk>/salesrcd', SalesRcDtailView.as_view(), name='salesrcd'),
    path('salesrc/<int:pk>/salesrcd2', SalesReceiptView, name='salesrcd2'),
    path('change_quantity/', views.Change_Qreceipt, name='change_quantity'),
    path('salesrc/product_sales/<int:pk>/', views.SalesView_byProduct, name='product_sales'),
    path('salesrc/product_sales/', views.SalesView, name='product_sale'),
    path('AddPayment/<int:pk>', AddPayment, name='Add_payment'),
    path('amount_tenderd_view/<int:pk>', AmountTenderdView, name='amount_view'),
    path('remove_producto/<int:pk>', RemoveProducto, name='remove_producto'),
    path('receipt_pdf/<int:pk>', SalesReceiptPdf, name='receipt_pdf'),
    path('generate_sales_receipt/<int:pk>/', generate_sales_receipt_pdf, name='generate_sales_receipt'),
    path('generate_sales_receipt_txt/<int:pk>/', views.generate_sales_receipt_text, name='generate_sales_receipt_txt'),
    path('sales_chart/', views.sales_chart, name='sales_chart'),

    

]
