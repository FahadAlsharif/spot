from multiprocessing import context
from django.shortcuts import render, redirect
from .models import*
from django.contrib import messages
import bcrypt

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['passward']
            pwHash = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt()).decode()
            newUser = User.objects.create(
            fname=fname, lname=lname, email=email, password=pwHash)
            newUser.save()
            request.session['loggedInId'] = newUser.id
        return redirect('/home')
    else:
        return redirect('/')




def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            request.session['loggedInId'] = User.objects.get(
                email=request.POST['email1']).id
            return redirect('/home')


def success(request):
    if not 'loggedInId' in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['loggedInId']),
        'wish' : Wish.objects.all().order_by("-createdAt"), #all of them in same day ! im sure the code is right !! i cound done it by (ID) to show you or you could try it xD
        'granted' :Grantedd.objects.all()
        }
    return render(request, 'welcome.html', context)

def logout(request):
    del request.session['loggedInId']
    return redirect('/')

def addwishform(request):
        context = {
        'user': User.objects.get(id=request.session['loggedInId']),
        }
        return render (request , "newwish.html" , context)

def stat(request):
    user = User.objects.get(id=request.session['loggedInId'])
    userd= Wish.objects.filter(done=True).filter(user=user)
    userf= Wish.objects.filter(done=False).filter(user=user)
    context = {
        'Granted': Grantedd.objects.all,
        'user': User.objects.get(id=request.session['loggedInId']),
        'userd':userd,
        'userf':userf,
        
        }
    return render (request , "stat.html" , context)

def addwish(request):
    if request.method == 'POST':
        errors = Wish.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/home/addwish')
        else:
            user = User.objects.get(id=request.session['loggedInId'])
            newwish = Wish.objects.create(
                item = request.POST['item'],
                desc = request.POST['desc'],
                user = user)
            newwish.save()
            newwish.like.add(user)
    return redirect('/home')
def editt(request,_id):
    editwish= Wish.objects.get(id=_id)
    context = {
        'wish' :editwish
    }
    return render(request,'editwish.html',context)

def editwish(request, _id):
    if request.method == 'POST':
        errors = Wish.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/home/edit/{_id}')
        else:
            editwish= Wish.objects.get(id=_id)
            editwish.item=request.POST['item']
            editwish.desc=request.POST['desc']
            editwish.save()
        return redirect('/home')

def dle(request, _id):
    Wish.objects.get(id=_id).delete()
    return redirect('/home')

def Granted(request,_id):
    wish = Wish.objects.get(id=_id)
    Grantedd.objects.create(
        Gran=wish
    )
    wish.done=True
    wish.save()
    return redirect('/home')

def like_wish(request, _id):
    wish = Wish.objects.get(id=_id)
    user = User.objects.get(id=request.session['loggedInId'])
    wish.like.add(user)
    return redirect('/home')