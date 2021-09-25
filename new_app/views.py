from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
# import bcrypt


def index(request):
    return render(request, 'index.html')  # Create your views here.


def welcome(request):
    return render(request, 'welcome.html')


def register(request):
    if request.method == "GET":
        return redirect('/')

    errors = user.objects.validate(request.POST)
    if errors:
        for a in errors.values():
            messages.error(request, a)
        return redirect('/')
    else:
        new_user = user.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],                             email=request.POST['email'],                                       password=request.POST['password'])
        # bcrypt not working on computer for some reason. Here I would:
        # passwrd = request.POST['password']
        # hashpwrd = bcrypt.hashpw(passwrd.encode(), bcrypt.gensalt()).decode()
        # user.objects.create(password = hashpwrd)
        messages.success(request, "Registration Successful!")
        request.session['user_id'] = new_user.id
        request.session['name'] = new_user.first_name
        return redirect('/user_page')
    
def login (request):
    request.session.flush()
    return redirect('/')

def user_page(request):
    many_thoughts = thought.objects.all()
    context = {
        'all_thoughts':many_thoughts
        }
    
    return render (request, 'user_page.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def login (request):
    if request.method == "GET":
        return redirect('/')

    errors = user.objects.login_validate(request.POST)
    if errors:
        for a in errors.values():
            messages.error(request, a)
        return redirect('/')
    else:
        this_user = user.objects.get(email=request.POST['email'])
    context = {
        'current_user':this_user}
    request.session['user_id'] = this_user.id
    request.session['name']=this_user.first_name
    messages.success(request, "You are logged in!")
    return redirect('/user_page', context)

def add_thought (request):
    if request.method == "GET":
        return redirect('/')
    errors = thought.objects.validate(request.POST)
    if errors:
        for a in errors.values():
            messages.error(request, a)
        return redirect('quotes.html')
    else:
        current_user = user.objects.get(id=request.session['user_id'])
        new_thought = thought.objects.create(thoughts = request.POST['thoughts'], posted_by = current_user)                                             
    return redirect ('/user_page')

def details(request, thought_id):
    this_thought = thought.objects.get(id=thought_id)
    likes=this_thought.liked_by.all()
    context = {
        'one_thought':this_thought,
        'all_likes':likes
        }
    return render(request, 'thoughts_page.html', context)



def unlike(request, thought_id):
    this_thought=thought.objects.get(id=thought_id)
    this_user=user.objects.get(id=request.session['user_id'])
    this_user.likes.remove(this_thought)
    return redirect(f'/details/{thought_id}')

def like(request, thought_id):
    this_thought=thought.objects.get(id=thought_id)
    this_user=user.objects.get(id=request.session['user_id'])
    if this_user.id == this_thought.id:
        this_thought.liked_by.append(this_user) 
    this_user.likes.add(this_thought)
    return redirect(f'/details/{thought_id}')


def delete(request, thought_id):
    this_thought=thought.objects.get(id=thought_id)
    # this_user=user.objects.get(id=request.session['user_id'])
    this_thought.delete()
    # this_thought.save()
    return redirect('/user_page')


