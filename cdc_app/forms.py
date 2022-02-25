from cProfile import label
from multiprocessing.connection import Client
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ValidationError


# Create your forms here.

class DateInput(forms.DateInput):
    input_type = 'date'
	
class UserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	class Meta:
		model = User
		fields = ('email','password')

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		del self.fields['password2']
		del self.fields['password1']
		self.fields['email'].widget = forms.TextInput(attrs={'placeholder':'Email-Id'})
		self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder':'Password'})

	def clean_email(self):
		data = self.cleaned_data['email']
		if data.isdigit():
			raise ValidationError("You have entered a Number! Please enter Name.")
		else:
			return data

	

class ProfileForm(forms.ModelForm):
    email_id = forms.EmailField(max_length = 200,required=True)

    def __init__(self,*args,**kwargs):
    #     pdb.set_trace()
    #     try:
    #         is_edit = kwargs['is_edit']
    #         kwargs = {}
    #         pdb.set_trace()
    #         super (ProfileForm,self ).__init__(*args,**kwargs) # populates the post
           
    #     except:
    #         super (ProfileForm,self ).__init__(*args,**kwargs) # populates the post
        super(ProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['email_id'].widget.attrs['readonly'] = True

    def clean_email_field(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.email_id
        else:
            return self.cleaned_data['email_id']

    class Meta:
        model = Profile
        fields = ('email_id','emp_id','first_name','middle_name','last_name', 'gender', 'role','designation')
        labels = {'email_id':'EMAIL ID','emp_id':'Employee id'}
# class CompanyForm(forms.ModelForm):
#     def __init__(self,*args,**kwargs):
#         from django.db.models import Q
#         profile_filter = Q()
#         try:
#             action = kwargs['action']
#             name = kwargs['name']
#             spoc = kwargs['spoc']
#             website =  kwargs['website']
#             contact =  kwargs['contact']
#             email =  kwargs['email']
#             phone =  kwargs['phone']
#             position =  kwargs['position'] 
#             location = kwargs['location']
#             sector = kwargs['sector']
#             company_turnover =  'company_turnover',
#             approximate_manpower =  'approximate_manpower'
#             kwargs = {}
#             super (CompanyForm,self ).__init__(*args,**kwargs) # populates the post
#             self.fields['name'].queryset = name
#             self.fields['spoc'].queryset = Profile.objects.filter(id = spoc.id)
#             self.fields['website'].queryset = website
#             self.fields['contact'].queryset = contact
#             self.fields['email'].queryset = email
#             self.fields['phone'].queryset = phone
#             self.fields['position'].queryset = position
#             self.fields['location'].queryset = Location.objects.filter(id = location.id)
#             self.fields['sector'].queryset = sector
#             self.fields['company_turnover'].queryset = company_turnover
#             self.fields['approximate_manpower'].queryset = approximate_manpower
#         except:
#             try:
#                 print("Profile sent")
#                 profile = kwargs['profile'][0]
#                 if profile.role == 'Observer':
#                     profile_filter = Q(id = profile.id)
#                 if profile.role == 'SuperAdmin':
#                     profile_filter = Q()
#                 if profile.role == 'Staff':
#                     profile_filter = Q(id = profile.id)
#                 kwargs.pop('profile')
#                 # filter which profiles to send. if profile.role == superadmin: then return full list, else just profile.id = profile.od
#             except:
#                 print('Error in CompanyForm')
#             # pdb.set_trace()

#             super (CompanyForm,self ).__init__(*args,**kwargs) # populates the post
#             self.fields['spoc'].queryset = Profile.objects.filter(profile_filter)
#         # print(Profile.objects.filter(profile_filter).values_list('id'))
#         # print(Profile.objects.filter(profile_filter).values_list('user'))
#         # pdb.set_trace()
        
#     class Meta:
#         model=Company
#         fields = ['name','spoc','website','contact','email','phone','position','location','sector','company_turnover','approximate_manpower']



class CompanyForm(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		try:
			from django.db.models import Q
			profile_filter = Q()
			profile = kwargs['profile'][0]
			print("Profile sent")
			if profile.role == 'Observer':
				profile_filter = Q(id = profile.id)
			if profile.role == 'SuperAdmin':
				profile_filter = Q()
			if profile.role == 'Staff':
				profile_filter = Q(id = profile.id)
			kwargs.pop('profile')
			super (CompanyForm,self ).__init__(*args,**kwargs) # populates the post
			for visible in self.visible_fields():
				visible.field.widget.attrs['class'] = 'form-control'
			self.fields['spoc'].queryset = Profile.objects.filter(profile_filter)
		
			# filter which profiles to send. if profile.role == superadmin: then return full list, else just profile.id = profile.od
		except:
			super (CompanyForm,self ).__init__(*args,**kwargs) # populates the post
			# pdb.set_trace()
			for visible in self.visible_fields():
				visible.field.widget.attrs['class'] = 'form-control'
		# pdb.set_trace()

		# print(Profile.objects.filter(profile_filter).values_list('id'))
		# print(Profile.objects.filter(profile_filter).values_list('user'))
		# pdb.set_trace()
		
	def clean_contact(self):
		data = self.cleaned_data['contact']
		
		if data.isdigit():
			raise ValidationError("You have entered a Number! Please enter Name.")
		else:
			return data

	def clean_phone(self):
		data = self.cleaned_data['phone']
		print(data, str(data))
		if data < 0 :
			raise ValidationError("Entered number is invalid!")
		if len(str(data)) < 10:
			raise ValidationError("Entered number has less than 10 digits!")
		if len(str(data)) > 10:
			raise ValidationError("Entered number has more than 10 digits!")
		
		
		return data
	class Meta:
		model=Company
		# fields = '__all__'
		exclude = ('is_approved', 'created_datetime', 'modified_datetime')
		labels = {'name':'Company Name','spoc':'CDC Employee','contact':'Contact Person','company_turnover':'Approx Turnover(cr)','approximate_manpower':'Manpower'}
		widgets = {'date_of_entry': DateInput(),
					'date_of_first_contact': DateInput(),
					'date_of_last_contact': DateInput()
					}

class ClientForm(forms.ModelForm):
	
	def __init__(self,*args,**kwargs):
		try:
			from django.db.models import Q
			profile_filter = Q()
			profile = kwargs['profile'][0]
			print("Profile sent")
			if profile.role == 'Observer':
				profile_filter = Q(id = profile.id)
			if profile.role == 'SuperAdmin':
				profile_filter = Q()
			if profile.role == 'Staff':
				profile_filter = Q(id = profile.id)
			kwargs.pop('profile')
			super (ClientForm,self ).__init__(*args,**kwargs) # populates the post
			for visible in self.visible_fields():
				visible.field.widget.attrs['class'] = 'form-control'
			self.fields['spoc'].queryset = Profile.objects.filter(profile_filter)
			self.fields['company'].queryset = Company.objects.filter(spoc__in = Profile.objects.filter(profile_filter))
		
			# filter which profiles to send. if profile.role == superadmin: then return full list, else just profile.id = profile.od
		except:
			super (ClientForm,self ).__init__(*args,**kwargs) # populates the post
			for visible in self.visible_fields():
				visible.field.widget.attrs['class'] = 'form-control'
			# pdb.set_trace()
			print('Error in CompanyForm')
		
	class Meta:
		model=Client
		exclude = ('is_approved', 'created_datetime', 'modified_datetime','consideration_status')
		labels = {'spoc':'CDC Employee','company':'Company Name',}
		widgets = {'date_of_entry': DateInput(),
					'date_of_first_contact': DateInput(),
					'date_of_last_contact': DateInput()
					}

 
    
