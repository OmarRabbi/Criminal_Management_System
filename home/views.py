from django.shortcuts import render, redirect
from home.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def addrecords(request):
    if request.method == "POST":
        data = request.POST
        criminal_name = data.get('criminal_name')
        height = data.get('height')
        age = data.get('age')
        unique_identity = data.get('unique_identity')
        criminal_image = request.FILES.get('criminal_image')
        crime_type = data.get('crime_type')
        crime_desc = data.get('crime_desc')
        CriminalRecords.objects.create(
            criminal_name = criminal_name,
            height = height,
            age = age,
            unique_identity = unique_identity,
            criminal_image = criminal_image,
            crime_type = crime_type,
            crime_desc = crime_desc,
        )
        return redirect('/add-records/')
    return render(request, 'addrecords.html', context={'page' : 'add-records'})
@login_required(login_url="/login/")
def view(request):
    records = CriminalRecords.objects.all()
    if request.GET.get('search'):
        records = records.filter(criminal_name__icontains = request.GET.get('search'))
    return render(request, 'index.html', context={'records' : records, 'page' : 'homepage'})
def delete_record(request, id):
    record = CriminalRecords.objects.get(id = id)
    record.delete()
    return redirect('/')
@login_required(login_url="/login/")
def update_record(request, id):
    records = CriminalRecords.objects.get(id = id)
    if request.method == "POST":
        data = request.POST
        criminal_name = data.get('criminal_name')
        height = data.get('height')
        age = data.get('age')
        unique_identity = data.get('unique_identity')
        criminal_image = request.FILES.get('criminal_image')
        crime_type = data.get('crime_type')
        crime_desc = data.get('crime_desc')
        records.criminal_name = criminal_name
        records.height = height
        records.age = age 
        records.unique_identity = unique_identity
        records.crime_desc = crime_desc
        if crime_type:
            records.crime_type = crime_type
        if criminal_image:
            records.criminal_image = criminal_image
        records.save()
        return redirect('/')
    return render(request, 'updaterecords.html', context={'records' : records, 'page' : 'update-records'})
def login_page(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        if not User.objects.filter(username = username).exists():
            messages.info(request, 'Invalid username')
            return redirect('/login/')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid password')
            return redirect('/login/')
    return render(request, 'login.html', context={'page' : 'login'})
def logout_page(request):
    logout(request)
    return redirect('/login/')
def register_page(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get('first_name')
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, 'Username already taken')
            return redirect('/register/')
        user = User.objects.create(
            first_name = first_name,
            email = email,
            username = username,
        )
        user.set_password(password)
        user.save()
        messages.info(request, 'Account created Successfully')
    return render(request, 'register.html', context={'page' : 'login'})