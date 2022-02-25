"""bloging URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views, settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from cdc_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.user_login,name='loginpage'),
    path('home',views.home,name='homepage'),
    path('logout',views.user_logout,name='logout'),
    path('add_people',views.add_user,name='add_people'),
    path('get_user_details',views.get_user_details,name='get_user_details'),

    path('company',views.company_details,name='client_db'),
    path('get_company_details',views.get_company_details,name='get_company_details'),
    path('delete_company_details_row',views.delete_company_details_row,name='delete_company_details_row'),
    path('edit_company_details/<data>',views.edit_company_details,name='edit_company_details'),
    # path('edit_company_details_row',views.edit_company_details_row,name='edit_company_details_row'),
    path('approve_company_details_row',views.approve_company_details_row,name='approve_company_details_row'),
    
    path('clients',views.client_details,name='client_database'),
    path('get_client_details',views.get_client_details,name='get_client_details'),
    path('delete_client_details_row',views.delete_client_details_row,name='delete_client_details_row'),
    path('delete_people_row',views.delete_people_row,name='delete_people_row'),
    path('edit_client_details/<data>',views.edit_client_details,name='edit_client_details'),
    path('edit_people/<data>',views.edit_people,name='edit_people'),
    path('approve_client_details_row',views.approve_client_details_row,name='approve_client_details_row'),
    
    path('final_report',views.final_report,name='final_report'),
    path('get_final_report',views.get_final_report,name='get_final_report'),
    path('delete_final_report_row',views.delete_final_report_row,name='delete_final_report_row'),
    path('delete_people_row',views.delete_people_row,name='delete_people_row'),
    path('edit_final_report/<data>',views.edit_final_report,name='edit_final_report'),
    path('password-reset',views.password_reset,name='password-reset')

    
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
