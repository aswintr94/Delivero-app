from django.shortcuts import render,redirect
from my_app.models import Admin_Register,Driver_Register,Tasks,Delivered,Delivery_Documents,Returned,Return_Documents,Delivery_Docs_by_admin,Statistics
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
import random
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
import pandas as pd
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
import json
import datetime

# Create your views here.
def sign_in(request):
    return render(request,'sign_in.html')

def sign_in_check(request):
    data = dict()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Admin_Register.objects.filter(username=username,password=password).exists():
            admin_data = Admin_Register.objects.get(username=username,password=password)
            new_var = Admin_Register.objects.filter(username=username,password=password).values('image').first()
            request.session['name'] = admin_data.name
            request.session['email'] = admin_data.email
            request.session['username'] = admin_data.username
            request.session['password'] = admin_data.password
            request.session['status'] = admin_data.status
            request.session['id'] = admin_data.id
            request.session['image'] = new_var['image']
            data['message'] = "Login Successfully"
            data['error'] = 1
            return JsonResponse(data)
        else:
            data['message'] = "Check your username and password"
            data['error'] = 0
            return JsonResponse(data)

def home(request):
    if 'username' in request.session:
        pending_tasks = Tasks.objects.count()
        delivered_tasks = Delivered.objects.count()
        returned_tasks = Returned.objects.count()
        drivers = Driver_Register.objects.count()
        Statistics.objects.all().delete()
        admins = Admin_Register.objects.all()
        image = Admin_Register.objects.get(id=request.session.get('id')).image
        for admins in admins:
            admin_details = Admin_Register.objects.get(id=admins.id)
            no_of_pending_tasks = Tasks.objects.filter(admin_id_id__name = admins.name).count()
            no_of_delivered_tasks = Delivered.objects.filter(creator=admins.name).count()
            no_of_returned_tasks = Returned.objects.filter(creator=admins.name).count()
            new = Statistics(admin=admin_details,pending_tasks=no_of_pending_tasks,delivered_tasks=no_of_delivered_tasks,returned_tasks=no_of_returned_tasks)
            new.save()
        numbers = Statistics.objects.all()
        return render(request,'index.html',{'pending_tasks': pending_tasks,'delivered_tasks': delivered_tasks,'returned_tasks': returned_tasks,'drivers': drivers,'numbers':numbers,'image':image})
    else:
        return redirect(sign_in)

def admin_register(request):
    if 'username' in request.session:
        return render(request,'admin_register.html')
    else:
        return redirect(sign_in)

def admin_reg_submit(request):
    data = dict()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        status = request.POST.get('admin')
        if len(request.FILES) != 0:
            image = request.FILES.get('image')
        else:
            image = "default/default.png"

        if Admin_Register.objects.filter(email=email).exists():
            data['message'] = "Email ID already exists"
            data['error'] = 0
            return JsonResponse(data)

        if Admin_Register.objects.filter(username=username).exists():
            data['message'] = "Username not available"
            data['error'] = 0
            return JsonResponse(data)

        new = Admin_Register(name=name,email=email,username=username,password=password,status=status,image=image)
        new.save()
        data['message'] = "successfully registered"
        data['error'] = 1
        return JsonResponse(data)

def admin_list(request):
    if 'username' in request.session:
        db = Admin_Register.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(db, 3)
        try:
            datas = paginator.page(page)
        except PageNotAnInteger:
            datas = paginator.page(1)
        except EmptyPage:
            datas = paginator.page(paginator.num_pages)
        return render(request,'admin_list.html',{'datas':datas})
    else:
        return redirect(sign_in)

def update_user(request,u_id):
    if 'username' in request.session:
        user_data = Admin_Register.objects.get(id=u_id)
        return render(request,'update_user.html',{'user_data':user_data})
    else:
        return redirect(sign_in)
    

def user_update_submit(request):
    data = dict()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        status = request.POST.get('admin')
        user_id = request.POST.get('user_id')

        try: 
            image = request.FILES['image']
            fs = FileSystemStorage()
            path = "admin/%s" %image.name
            new_image = fs.save(path,image)
        except MultiValueDictKeyError:
            db = Admin_Register.objects.get(id=user_id)
            new_image = db.image
        
        Admin_Register.objects.filter(id=user_id).update(name=name,email=email,username=username,password=password,status=status,image=new_image)
        data['message'] = "Updated the details successfully!"
        data['error'] = 1
        return JsonResponse(data)

def delete_user(request):
    data = dict()
    if request.method == "POST": 
        admin_id = request.POST.get('admin_id')

        Admin_Register.objects.filter(id=admin_id).delete()
        # data['message'] = ""
        return redirect(admin_list)

def driver_registration(request):
    if 'username' in request.session:
        return render(request,'driver_registration.html')
    else:
        return redirect(sign_in)

def driver_reg_submit(request):
    data = dict()
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        first_part = fname[0:3]
        second_part = str(random.randint(100,200))
        code = first_part+second_part

        if Driver_Register.objects.filter(email=email).exists():
            data['message'] = 'Email ID already exists'
            data['error'] = 0
            return JsonResponse(data)

        if Driver_Register.objects.filter(username=username).exists():
            data['message'] = "Username cannot be taken"
            data['error'] = 0
            return JsonResponse(data)
            
        if Driver_Register.objects.filter(mobile=mobile).exists():
            data['message'] = 'Mobile number already taken'
            data['error'] = 0
            return JsonResponse(data)

        new = Driver_Register(first_name=fname,last_name=lname,email=email,mobile=mobile,username=username,password=password,driver_id=code)
        new.save()
        data['message'] = "Successfully registered"
        data['error'] = 1
        return JsonResponse(data)

def driver_list(request):
    if 'username' in request.session:
        all_drivers = Driver_Register.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(all_drivers, 2)
        try:
            datas = paginator.page(page)
        except PageNotAnInteger:
            datas = paginator.page(1)
        except EmptyPage:
            datas = paginator.page(paginator.num_pages)
        return render(request,'driver_list.html',{'datas':datas})
    else:
        return redirect(sign_in)

def search_driver(request):
    if 'username' in request.session:
        search_detail = request.POST.get('search')
        if (Driver_Register.objects.filter(Q(first_name__contains=search_detail) | Q(last_name__contains=search_detail) | Q(email__contains=search_detail) | Q(username__contains=search_detail)).exists()):
            data = Driver_Register.objects.filter(Q(first_name__contains=search_detail) | Q(last_name__contains=search_detail) | Q(email__contains=search_detail) | Q(username__contains=search_detail))
            return render(request,'driver_list.html',{'datas':data})
        else:
            message = "Driver not found"
            return render(request,'driver_list.html',{'message': message})
    else:
        return redirect(sign_in)

def update_driver(request,d_id):
    if 'username' in request.session:
        driver = Driver_Register.objects.get(id=d_id)
        return render(request,'update_driver.html',{'driver':driver})
    else:
        return redirect(sign_in)

def driver_data_update(request):
    data = dict()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        username = request.POST.get('username')
        password = request.POST.get('password')
        d_id = request.POST.get('driver_id')

        Driver_Register.objects.filter(id=d_id).update(first_name=first_name,last_name=last_name,email=email,mobile=mobile,username=username,password=password)
        data['message'] = "Details updated"
        data['error'] = 1
        return JsonResponse(data)
    else:
        data['message'] = "Updation failed"
        data['error'] = 0
        return JsonResponse(data)

def delete_driver(request,d_id):
    task = Tasks.objects.all()
    driver = Driver_Register.objects.get(id=d_id).driver_id
    if Tasks.objects.filter(driver_code=driver).exists():
        messages.error(request,"The driver is assigned with tasks. Can't delete")
    else:
        Driver_Register.objects.filter(id=d_id).delete()
    return redirect(driver_list)

def add_tasks(request):
    if 'username' in request.session:
        return render(request,'add_tasks.html')
    else:
        return redirect(sign_in)

def upload_tasks(request):
    data = dict()
    if request.method == "POST":
        admin = request.POST.get('admin')
        file = request.FILES.get('task_file')
        filename = file.name
        if filename.endswith('.xlsx'):
            data1 = pd.read_excel(file)
            df = pd.DataFrame(data1)
            for i in range(len(df)):
                new = Tasks(
                    admin_id=Admin_Register.objects.get(name=admin),
                    order_id=df.loc[i].order_id,
                    invoice_no=df.loc[i].invoice_no,
                    product=df.loc[i].product_code,
                    driver_code=df.loc[i].driver_code,
                    customer_name=df.loc[i].customer_name,
                    customer_mobile=df.loc[i].customer_mobile,
                    customer_address=df.loc[i].customer_address,
                    shipping_name=df.loc[i].shipping_name,
                    district=df.loc[i].district,
                    pin_code=df.loc[i].pincode,
                    alt_contact_no=df.loc[i].alternate_contact_no,
                    client = df.loc[i].client_name,
                    preference=df.loc[i].preference_no,
                    latitude=df.loc[i].latitude,
                    longitude=df.loc[i].longitude,
                    status="Pending",
                    )
                new.save()
            data['message'] = "Tasks upload success"
            data['error'] = 1
            return JsonResponse(data)
            
        else:
            data['message'] = "Check the type of the file"
            data['error'] = 0
            return JsonResponse(data)

def live_tasks_table(request):
    if 'username' in request.session:
        if request.session.get('status') == 'super admin':
            db = Tasks.objects.all()
            drivers = Driver_Register.objects.all()
            admin = Admin_Register.objects.all()
            return render(request,'live_tasks_table.html',{'task':db,'drivers':drivers,'admin':admin})
        else:
            db = Tasks.objects.filter(admin_id_id__name = request.session.get('name'))
            drivers = Driver_Register.objects.all()
            admin = Admin_Register.objects.all()
            return render(request,'live_tasks_table.html',{'task':db,'drivers':drivers,'admin':admin})

    else:
        return redirect(sign_in)

def task_sort_by_admin(request):
    if 'username' in request.session:
        admin_name = request.POST.get('admin')
        drivers = Driver_Register.objects.all()
        admin = Admin_Register.objects.all()
        if admin_name == 'all':
            db = Tasks.objects.all()
            return render(request,'live_tasks_table.html',{'task':db,'drivers':drivers,'admin':admin})
        else:
            db = Tasks.objects.filter(admin_id__name = admin_name)
            return render(request,'live_tasks_table.html',{'task':db,'drivers':drivers,'admin':admin})
    else:
        return redirect(sign_in)

def delete_task(request):
    id = request.POST.get('identifier')
    Tasks.objects.get(id=id).delete()
    return redirect(live_tasks_table)

def view_task(request,o_id):
    if 'username' in request.session:
        order_details = Tasks.objects.get(id=o_id)
        return render(request,'view_task.html',{'details':order_details})
    else:
        return redirect(sign_in)

def change_driver(request):
    new_driver = request.POST.get('driver')
    task_id = request.POST.get('task_id')
    Tasks.objects.filter(id=task_id).update(driver_code=new_driver)
    return redirect(live_tasks_table)

def change_preference(request):
    new_pref = request.POST.get('new_pref')
    task_id = request.POST.get('task_id')
    Tasks.objects.filter(id=task_id).update(preference=new_pref)
    return redirect(live_tasks_table)

def task_list_delete(request):
    if request.is_ajax():
        selected_tests = request.POST['task_list_ids']
        selected_tests = json.loads(selected_tests)
        for test in enumerate(selected_tests):
            if test != '':
                Tasks.objects.filter(id__in=selected_tests).delete()
        return None

def delivered_tasks(request):
    items = Delivered.objects.all()
    additional_docs = Delivery_Docs_by_admin.objects.all()
    return render(request,'delivered tasks.html',{'items':items,'doc':additional_docs})

def view_documents(request,t_id):
    doc = Delivery_Documents.objects.get(task_id=t_id)
    return render(request,'delivery_documents.html',{'doc':doc})

def delivery_docs_by_admin(request):
    data = dict()
    if request.method == "POST":
        task_id = request.POST.get('task_id')
        document = request.FILES.get('document')
        task_details = Delivered.objects.get(task_id=task_id)
        docs = Delivery_Docs_by_admin(task_details=task_details,document=document)
        docs.save()
        data['message'] = "Upload Success"
        data['error'] = 1
        return JsonResponse(data)
    else:
        data['message'] = "Upload Failed"
        data['error'] = 0
        return JsonResponse(data)

def delete_additional_delivery_doc(request,id):
    Delivery_Docs_by_admin.objects.filter(id=id).delete()
    return redirect(delivered_tasks)

def returned_tasks(request):
    data = Returned.objects.all()
    if Return_Documents.objects.all():
        doc = Return_Documents.objects.all()
        return render(request,'returned table.html',{'data':data,'doc':doc})
    else:
        return render(request,'returned table.html',{'data':data})

def upload_return_doc(request):
    data = dict()
    if request.method == "POST":
        t_id = request.POST.get('t_id')
        return_item_details = Returned.objects.get(task_id=t_id)
        document = request.FILES.get('return doc')
        doc = Return_Documents(return_item_details=return_item_details,document=document)
        doc.save()
        data['message'] = "Upload success"
        data['error'] = 1
        return JsonResponse(data)
    else:
        data['message'] =  "Upload_failed"
        data['error'] = 0
        return JsonResponse(data)

def delete_return_docs(request,id):
    Return_Documents.objects.filter(id=id).delete()
    return redirect(returned_tasks)

def return_to_pending(request,t_id):
    Tasks.objects.filter(id=t_id).update(admin_id=request.session.get('id'),date=datetime.date.today(),status="Pending")
    Return_Documents.objects.filter(return_item_details__task_id=t_id).delete()
    Returned.objects.filter(task_id=t_id).delete()
    return redirect(returned_tasks)

def delete_returned_item(request,t_id):
    Returned.objects.filter(task_id=t_id).delete()
    Tasks.objects.filter(id=t_id).delete()
    Return_Documents.objects.filter(return_item_details=t_id).delete()
    return redirect(returned_tasks)


def change_password_submit(request):
    data = dict()
    if request.method == "POST":
        
        current_password = request.POST.get('current_password')
        new_password_1 = request.POST.get('new_password_1')
        new_password_2 = request.POST.get('new_password_2')
        if current_password == request.session['password']:
            if new_password_1 == new_password_2:
                Admin_Register.objects.filter(id=request.session.get('id')).update(password=new_password_2)
                request.session['password'] = new_password_2
                data['message'] = "Password changed successfully"
                data['error'] = 1
                return JsonResponse(data)
            else:
                data['message'] = "New passwords doesn't match"
                data['error'] = 0
                return JsonResponse(data)
        else:
            data['message'] = "Check your current password"
            data['error'] = 0
            return JsonResponse(data)


        

def sign_out(request):
    del request.session['name']
    del request.session['email']
    del request.session['username']
    del request.session['password']
    del request.session['status']
    del request.session['id']
    return redirect(sign_in)