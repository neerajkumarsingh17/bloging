from django.contrib import admin
from .models import *




class CompanyAdmin(admin.ModelAdmin):
    """Admin for Company"""
    search_fields = ('name', 'contact')
    list_display = ('id', 'name', 'contact')

class LocationAdmin(admin.ModelAdmin):
    """Admin for Location"""
    search_fields = ('city', 'state')
    list_display = ('id', 'address', 'city', 'state', 'zipcode')

class CourseAdmin(admin.ModelAdmin):
    """Admin for Course"""
    search_fields = ('name',)
    list_display = ('id', 'name')

class ClientAdmin(admin.ModelAdmin):
    """Admin for Client"""
    search_fields = ('company', 'spoc', 'school', 'course', )
    list_display = ('id', 'company')


# Register your models here.
admin.site.register(School)
admin.site.register(Profile)
admin.site.register(ProfileSchool)
admin.site.register(Company, CompanyAdmin)
# admin.site.register(Location, LocationAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Client, ClientAdmin)

