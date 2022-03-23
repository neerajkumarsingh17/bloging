from curses.ascii import US
from gettext import install
from django.shortcuts import  render, redirect, reverse
from .forms import UserForm, ProfileForm, CompanyForm, ClientForm
from django.contrib.auth import login, authenticate, logout #add this
from django.contrib import messages
import pdb
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.db.models import Q
import datetime
from django.views.decorators.csrf import csrf_exempt




# Create your views here.
def user_login(request):
    user = request.user
    users = Profile.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        at_index = username.find('@')+1
        domain = username[at_index:]
        if domain != 'adamasuniversity.ac.in' or domain != 'riceindia.org':
            return render(request,'index.html',{'error':'Invalid email address. Please use adamasuniversity or riceindia email id to login'})
        password = request.POST.get('password')
        #pdb.set_trace()
        print(username,password)
        user = authenticate(request,username = username,password = password)
        if user is not None:
            if user.is_active:
                login(request,user)
                role = user.profile.all()[0].role
                if user.profile.all()[0].role == 'SuperAdmin':
                    num_companies = Company.objects.all().count()
                    approved_count = Company.objects.filter(is_approved=True).count()
                    num_clients = Client.objects.all().count()
                    approved_count_client = Client.objects.filter(is_approved=True).count()

                else:
                    num_companies = Company.objects.filter(spoc__user=user).count()
                    approved_count = Company.objects.filter(spoc__user=user).filter(is_approved=True).count()
                    num_clients = Client.objects.filter(spoc__user=user).count()
                    approved_count_client = Client.objects.filter(spoc__user=user).filter(is_approved=True).count()

                return render(request,'homepage.html',{'role':role,
                            'users':users,
                            'num_companies':num_companies,
                            'approved_count':approved_count,
                            'num_clients':num_clients,
                            'approved_count_client':approved_count_client})
        else:
            return render(request,'index.html',{'error':'Sorry we could not find an account with that username. Please Try Again.'})
    else:
        if str(str(request.user))=='AnonymousUser':
            return render(request,'index.html',)
        else:
            role = request.user.profile.all()[0].role
            if user.profile.all()[0].role == 'SuperAdmin':
                num_companies = Company.objects.all().count()
                approved_count = Company.objects.filter(is_approved=True).count()
                num_clients = Client.objects.all().count()
                approved_count_client = Client.objects.filter(is_approved=True).count()

            else:
                num_companies = Company.objects.filter(spoc__user=user).count()
                approved_count = Company.objects.filter(spoc__user=user).filter(is_approved=True).count()
                num_companies = Company.objects.filter(spoc__user=user).count()
                approved_count = Company.objects.filter(spoc__user=user).filter(is_approved=True).count()
                num_clients = Client.objects.filter(spoc__user=user).count()
                approved_count_client = Client.objects.filter(spoc__user=user).filter(is_approved=True).count()

            return render(request,'homepage.html',{'role':role,
                                'users':users,
                                'num_companies':num_companies,
                                'approved_count':approved_count,
                                'num_clients':num_clients,
                                'approved_count_client':approved_count_client})
        
        

@login_required
def user_logout(request):
    logout(request)
    return redirect('loginpage')

def home(request):
    user = request.user
    users = Profile.objects.all()
    if str(user)=='AnonymousUser':
        return redirect('loginpage')
    elif user.profile.all()[0].role == 'SuperAdmin':
        num_companies = Company.objects.all().count()
        approved_count = Company.objects.filter(is_approved=True).count()
        num_clients = Client.objects.all().count()
        approved_count_client = Client.objects.filter(is_approved=True).count()
        #pdb.set_trace()
    else:
        num_companies = Company.objects.filter(spoc__user=user).count()
        approved_count = Company.objects.filter(spoc__user=user).filter(is_approved=True).count()
        num_clients = Client.objects.filter(spoc__user=user).count()
        approved_count_client = Client.objects.filter(spoc__user=user).filter(is_approved=True).count()


    if user is not None:
            if user.is_active:
                role = user.profile.all()[0].role
                return render(request,'homepage.html',{'role':role,
                            'users':users,
                            'num_companies':num_companies,
                            'approved_count':approved_count,
                            'num_clients':num_clients,
                            'approved_count_client':approved_count_client})

    if str(user)=='AnonymousUser':
        return redirect('loginpage')

    # idx = 
    # url = "https://bootdey.com/img/Content/avatar/avatar"+idx+".png"
    return render(request,'homepage.html',{'users':users,
                    'num_companies':num_companies,
                    'approved_count':approved_count,
                    'num_clients':num_clients,
                    'approved_count_client':approved_count_client})

@login_required
def add_user(request):
    profile_form = ProfileForm()
    if request.method=='POST':
        email_id = request.POST.get('email_id')
        emp_id = request.POST.get('emp_id')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')

        role = request.POST.get('role')
        designation = request.POST.get('designation')

        user = User.objects.create_user(
            username = email_id,
            password = first_name.lower() + '' + last_name.lower()
        )

        user.save()

        profile = Profile(emp_id = emp_id,first_name=first_name,middle_name=middle_name,last_name=last_name,gender = gender, role=role,designation=designation)
        profile.user = user
        profile.save()
        return redirect('add_people')
        
        
    return render(request,'add_people.html',{'profile_form':profile_form})

@login_required
@csrf_exempt
def company_details(request):
    import json
    action = request.POST.get('action')
    role = request.user.profile.all()[0].role
    flag = False
    if action != None:
        if request.POST.get('action') == 'edit':
            # data =  json.loads(request.POST.get('data'))
            company = Company.objects.get(id = request.POST.get('company_id'))
            
            edit_company_form = CompanyForm(instance = company)
            # pdb.set_trace()

            return render(request,'company_details.html',{'edit_company_form':edit_company_form, 'role':role})
        else:
            pass
    else:
        company_form = CompanyForm(profile = request.user.profile.all())
        if request.method=='POST':
            # name = request.POST.get('name')
            # spoc = Profile.objects.filter(id=request.POST.get('spoc'))[0]
            # pdb.set_trace()
            # website = request.POST.get('website')
            # contact = request.POST.get('contact')
            # email = request.POST.get('email')
            # phone = request.POST.get('phone')
            # position = request.POST.get('position')
            # location = Location.objects.filter(id=request.POST.get('location'))[0]
            # sector = request.POST.get('sector')
            # company_turnover = request.POST.get('company_turnover')
            # approximate_manpower = request.POST.get('approximate_manpower')
            
            # company = Company.objects.create(name=name,spoc=spoc,website=website,
            #                 contact=contact,email=email,phone=phone,
            #                 position=position,location=location,sector=sector,
            #                 company_turnover=company_turnover,approximate_manpower=approximate_manpower)

            # company.save()
            # pdb.set_trace()
            company_form = CompanyForm(request.POST)
            if company_form.is_valid():
                company_form.save()
            else:
                flag = True

        return render(request,'company_details.html',{'company_form':company_form, 'role':role, 'form_make_visible':flag})

@csrf_exempt
@login_required
def delete_company_details_row(request):
    data = request.POST['data'].split('_')
    action, pk = data[0], data[1]
    # pdb.set_trace()
    company = Company.objects.get(id = pk)
    if action == 'delete':
        company.delete()
    elif  action == 'edit':
        company.name = company.name+"updated"
        company.save()
    else:
        action = "Invalid action"
    # pdb.set_trace()
    return JsonResponse({"action": action})


@csrf_exempt
def edit_company_details(request, data):
    if True:
        if request.method == 'POST':
            print("edit company called",data)
            # pdb.set_trace()
            prev_data = Company.objects.get(id = data)
            prev_data.is_approved = False
            edit_company_form = CompanyForm(request.POST, instance = prev_data)
            if edit_company_form.is_valid():
                edit_company_form.save()
                return redirect('client_db')

        else:
            try:
                edit_company_form = CompanyForm(instance = Company.objects.get(id = data))
            except:
                edit_company_form = CompanyForm()
    else:
        edit_company_form = CompanyForm()
    return render(request,'edit_company_form.html',{'edit_company_form':edit_company_form})

@csrf_exempt
def get_company_details(request):
    now = datetime.datetime.now()
    profile = request.user.profile.all()[0]
    print(request.user.profile.all()[0].role)
    try:
        if profile.role == 'SuperAdmin' or profile.role == 'Observer':
            companies1 = Company.objects.filter(is_approved=True).order_by('-created_datetime')
            companies2 = Company.objects.filter(is_approved=False).order_by('-created_datetime')
            from itertools import chain 
            companies = list(chain(companies2,companies1))

        elif profile.role == 'Staff' or profile.role == 'Observer':
            companies = Company.objects.filter(spoc = profile).order_by('-created_datetime')
    except:
        companies = Company.objects.none()
        print("Profile not found")
    
    comps = {}
    sl = 0
    for cc in companies:
        spoc = str(cc.spoc)
        name = cc.name
        website = cc.website
        contact = cc.contact
        email = cc.email
        phone = cc.phone
        position = cc.position
        address = cc.address
        city = cc.city
        zip = cc.zipcode
        state = cc.state
        country = cc.country
        sector = cc.sector
        turnover = cc.company_turnover
        approx_turnover = cc.approximate_manpower
        year = cc.created_datetime.year
        is_approved = cc.is_approved
        sl+=1
        comps[cc.id] = [sl, year, spoc,name,website,contact,email,phone,position,address,city,zip,state,country,sector,turnover,approx_turnover,is_approved]
    return JsonResponse({'companies':comps,'role':profile.role})

@csrf_exempt
def get_user_details(request):
    try:
        profile = request.user.profile.all()[0]
        if profile.role == 'SuperAdmin':
            profiles = Profile.objects.all()
        elif profile.role == 'Staff' or profile.role == 'Observer':
            profiles = Profile.objects.none()
        else:
            profiles = Profile.objects.none()
    except:
        profiles = Profile.objects.none()
        print("Profile not found")


    profs = {}
    sl = 0
    for pp in profiles:
        emp_id = pp.emp_id
        first_name = pp.first_name
        middle_name = pp.middle_name
        last_name = pp.last_name
        email_id = pp.user.username
        role = pp.role
        designation = pp.designation
        
        sl+=1
        profs[pp.id] = [sl,emp_id,first_name,middle_name,last_name,email_id,role,designation]
    return JsonResponse({'profiles':profs})

@login_required
@csrf_exempt
def approve_company_details_row(request):
    data = request.POST['data'].split('_')
    action, pk = data[0], data[1]
    company = Company.objects.get(id = pk)
    company.is_approved = True
    company.save()
    return JsonResponse({'status':'true'})

@login_required
@csrf_exempt
def client_details(request):
    import json
    action = request.POST.get('action')
    role = request.user.profile.all()[0].role
    now = datetime.datetime.now()
    profile = request.user.profile.all()[0]
    if action != None:
        if request.POST.get('action') == 'edit':
            client = Client.objects.get(id = request.POST.get('client_id'))
            
            edit_client_form = ClientForm(instance = client)
            # pdb.set_trace()

            return render(request,'client_details.html',{'edit_client_form':edit_client_form, 'role':role})
        else:
            pass
    else:
        client_form = ClientForm(profile = request.user.profile.all())
        if request.method=='POST':
            client_form = ClientForm(request.POST)
            # pdb.set_trace()
            if client_form.is_valid():
                client_form.save()
                redirect('client_database')
    
    return render(request,'client_details.html',{'client_form':client_form, 'role':role})
   

@csrf_exempt
def get_client_details(request):
    now = datetime.datetime.now()
    profile = request.user.profile.all()[0]
    print(request.user.profile.all()[0].role)
    try:
        if profile.role == 'SuperAdmin' or profile.role == 'Observer':

            clients1 = Client.objects.filter(is_approved=True).order_by('-created_datetime')
            clients2 = Client.objects.filter(is_approved=False).order_by('-created_datetime')
            from itertools import chain 
            clients = list(chain(clients2,clients1))

        elif profile.role == 'Staff' or profile.role == 'Observer':
            clients = Client.objects.filter(spoc = profile).order_by('-created_datetime')
    except:
        clients = Client.objects.none()
        print("Profile not found")
    
    clns = {}
    sl = 0
    for cc in clients:
        school = ""
        course = ""
        company_obj = cc.company
        company_name = company_obj.name
        contact_name = company_obj.contact
        position = company_obj.position
        location = cc.company.city + '-' + cc.company.state
        outreach_spoc = str(cc.spoc)
        projected_students = cc.projected_no_of_students
        school_obj = cc.school.all().values_list('school_name')
        for (i,) in school_obj:
            school += i + ', ' 
        course_obj = cc.course.all().values_list('name')
        for (i,) in course_obj:
            course += i + ', ' 
        school = school[:-2]
        course = course[:-2]
        # pdb.set_trace()
            
        lead_source = cc.lead_source
        remarks = cc.remarks
        date_first_contact = cc.date_of_first_contact
        #date_last_contact = cc.date_of_last_contact
        lead_status = cc.lead_status
        next_action = cc.next_action
        outocome = cc.outcome
        placement_conducted = cc.placement_drive_conducted
        internship_conducted = cc.internship_drive_conducted
        #pdb.set_trace()
        year = cc.created_datetime.year
        month = cc.created_datetime.strftime("%B")
        is_approved = cc.is_approved

        # is_approved = cc.is_approved
        sl+=1
        #clns[cc.id] = [sl, year, spoc,name,website,contact,email,phone,position,address,city,zip,state,country,sector,turnover,approx_turnover,is_approved]
        clns[cc.id] = [sl, year, month, company_name, contact_name,position,location,outreach_spoc,projected_students,school,
                    course,lead_source,remarks,date_first_contact,lead_status,next_action,outocome,placement_conducted, internship_conducted,is_approved]

    return JsonResponse({'clients':clns,'role':profile.role})

@login_required
@csrf_exempt
def approve_client_details_row(request):
    data = request.POST['data'].split('_')
    action, pk = data[0], data[1]
    client = Client.objects.get(id = pk)
    client.is_approved = True
    client.save()
    return JsonResponse({'status':'true'})

@csrf_exempt
@login_required
def delete_client_details_row(request):
    data = request.POST['data'].split('_')
    action, pk = data[0], data[1]
    # pdb.set_trace()
    client = Client.objects.get(id = pk)
    if action == 'delete':
        client.delete()
    else:
        action = "Invalid action"
    # pdb.set_trace()
    return JsonResponse({"action": action})

@csrf_exempt
def edit_client_details(request, data):
    # pdb.set_trace()
    if request.method == 'POST':
        prev_data = Client.objects.get(id = data)
        prev_data.is_approved = False
        edit_client_form = ClientForm(request.POST, instance = prev_data)

        if edit_client_form.is_valid():            
            edit_client_form.save()
            return redirect('client_database')

    else:
        try:
            edit_client_form = ClientForm(instance = Client.objects.get(id = data))
        except:
            edit_client_form = ClientForm()
            
    return render(request,'edit_client_form.html',{'edit_client_form':edit_client_form})

@csrf_exempt
def edit_people(request, data):
    # pdb.set_trace()
    if request.method == 'POST':
        prev_data = Profile.objects.get(id = data)
        
        edit_profile_form = ProfileForm(request.POST, instance = prev_data)

        if edit_profile_form.is_valid():            
            edit_profile_form.save()
            return redirect('add_people')

    else:
        try:
            instance = Profile.objects.get(id = data)
            email = instance.user.username
            edit_profile_form = ProfileForm(initial = {'email_id' : email}, instance = instance)
        except:
            edit_profile_form = ProfileForm()
            
    return render(request,'edit_profile_form.html',{'edit_profile_form':edit_profile_form})

@csrf_exempt
@login_required
def delete_people_row(request):
    data = request.POST['data'].split('_')
    action, pk = data[0], data[1]
    profile = Profile.objects.get(id = pk)
    user = User.objects.get(profile = profile)
    if action == 'delete':
        profile.delete()
        user.delete()
    else:
        action = "Invalid action"
    # pdb.set_trace()
    return JsonResponse({"action": action})


@login_required
@csrf_exempt
def final_report(request):

    return render(request,'final_report.html')


@csrf_exempt
def get_final_report(request):
    now = datetime.datetime.now()
    profile = request.user.profile.all()[0]
    print(request.user.profile.all()[0].role)
    try:
        if profile.role == 'SuperAdmin' or profile.role == 'Observer':

            clients1 = Client.objects.filter(is_approved=True).order_by('-created_datetime')
            clients2 = Client.objects.filter(is_approved=False).order_by('-created_datetime')
            from itertools import chain 
            clients = list(chain(clients2,clients1))

        elif profile.role == 'Staff' or profile.role == 'Observer':
            clients = Client.objects.filter(spoc = profile).order_by('-created_datetime')
    except:
        clients = Client.objects.none()
        print("Profile not found")
    clns = {}
    sl = 0
    for cc in clients:
        company_obj = cc.company

        if not (cc.is_approved and company_obj.is_approved):
            continue
        company_name = company_obj.name
        contact_name = company_obj.contact
        position = company_obj.position
        outreach_spoc = str(cc.spoc)
        projected_students = cc.projected_no_of_students
        number_of_hired_students = cc.no_of_students_hired
        school = ""
        course = ""
        school_obj = cc.school.all().values_list('school_name')
        for (i,) in school_obj:
            school += i + ', ' 
        course_obj = cc.course.all().values_list('name')
        for (i,) in course_obj:
            course += i + ', ' 
        school = school[:-2]
        course = course[:-2]
        # pdb.set_trace()
            
        lead_source = cc.lead_source
        remarks = cc.remarks
        date_first_contact = cc.date_of_first_contact
        date_last_contact = cc.date_of_last_contact

        lead_status = cc.lead_status
        next_action = cc.next_action
        outcome = cc.outcome
        placement_conducted = cc.placement_drive_conducted
        internship_conducted = cc.internship_drive_conducted
        #pdb.set_trace()
        year = cc.created_datetime.year
        month = cc.created_datetime.strftime("%B")
        is_approved = cc.is_approved
        email=  company_obj.email
        phone= company_obj.phone
        website= company_obj.website
        address= company_obj.address
        
        sector = company_obj.sector
        turnover = company_obj.company_turnover
        approx_manpower = company_obj.approximate_manpower
        city= company_obj.city
        state= company_obj.state
        zipcode= company_obj.zipcode
        country =  company_obj.country

        # is_approved = cc.is_approved
        sl+=1
        #clns[cc.id] = [sl, year, spoc,name,website,contact,email,phone,position,address,city,zip,state,country,sector,turnover,approx_turnover,is_approved]
        clns[cc.id] = [sl, company_name, contact_name, position, year, month, outreach_spoc, projected_students, number_of_hired_students, school,
                    course,lead_source,remarks,date_first_contact,date_last_contact, lead_status,next_action,outcome,placement_conducted, internship_conducted,
                    email, phone, website, address, sector,turnover,approx_manpower, city, state, zipcode, country]

    return JsonResponse({'clients':clns,'role':profile.role})

@login_required
@csrf_exempt
def approve_final_report_row(request):
    data = request.POST['data'].split('_')
    action, pk = data[0], data[1]
    client = Client.objects.get(id = pk)
    client.is_approved = True
    client.save()
    return JsonResponse({'status':'true'})

@csrf_exempt
@login_required
def delete_final_report_row(request):
    data = request.POST['data'].split('_')
    action, pk = data[0], data[1]
    # pdb.set_trace()
    client = Client.objects.get(id = pk)
    if action == 'delete':
        client.delete()
    else:
        action = "Invalid action"
    # pdb.set_trace()
    return JsonResponse({"action": action})

@csrf_exempt
def edit_final_report(request, data):
    # pdb.set_trace()
    if request.method == 'POST':
        prev_data = Client.objects.get(id = data)
        prev_data.is_approved = False
        edit_client_form = ClientForm(request.POST, instance = prev_data)

        if edit_client_form.is_valid():            
            edit_client_form.save()
            return redirect('client_database')

    else:
        try:
            edit_client_form = ClientForm(instance = Client.objects.get(id = data))
        except:
            edit_client_form = ClientForm()
            
    return render(request,'edit_client_form.html',{'edit_client_form':edit_client_form})


def password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        current_password = request.POST.get('password')
        user = authenticate(username=username,password=current_password)
        if user is not None:
            u = User.objects.get(username=username)
            new_password = request.POST.get('new-password')
            if(current_password==new_password):
                msg = 'Your New Password is same as Current Password. Please use a different password '
                return render(request,'password-reset.html',{'error':msg})
                
            u.set_password(new_password)
            u.save()
            return render(request,'index.html',{'msg':'Password Reset Successfully. Please login!'})
        else:
            msg = 'Invalid username or password. Please use adamasuniversity or riceindia email id to reset'
            return render(request,'password-reset.html',{'error':msg})

    return render(request,'password-reset.html')
