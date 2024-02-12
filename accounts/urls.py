from django.urls import path
from . import views
from .views import OutletStaffListsView

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.Register, name='register'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('email_confirmation/', views.EmailConfirmPage, name='email_confirmation'),
    path('view_profile/<int:pk>', views.Update_ViewProfile, name='view_profile'),
    path('change_password/', views.password_change, name='change_password'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('password_reset_confirm/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    path('settings_page/', views.Settings_Page, name='settings_page'),
    path('settings_paged/', views.Settings_PageD, name='settings_paged'),
    path('settings_pagedup/<int:pk>', views.Settings_PageD_Update, name='settings_pagedup'),
    path('create_outlet/', views.OutletCreatView, name='create_outlet'),
    path('delete_outlet/<int:pk>', views.DeleteOutlettView, name='delete_outlet'),
    path('add_staff/', views.AddOutletStaff, name='add_staff'),
    path('outlet_staffs', views.OutletStaffListsView, name='outlet_staffs'),
    path('outlet_staffs/outlet_staffsup/<int:pk>', views.OutletStaffUpdateView, name='outlet_staffsup'),
    path('outlet_staffs/delete/<int:pk>', views.DeleteOutletStaffView, name='delete_employee'),
    path('employee_login/', views.OutletStaffLoginView, name='employee_login'),
    path('employee_logout/<int:pk>', views.OutletStaffLogout, name='employee_logout'),
    path('outlet_staffs/<int:pk>/staff_Details/', views.OutletStaffDView, name='staff_Details')
]   
