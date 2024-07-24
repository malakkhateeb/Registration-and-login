from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


#render the main page of log in and registration 
def logIn(request):
    context={
        'regestrations':all_registrations(),
        # 'delet' :Registration.objects.all().delete()
    }
    return render(request, 'index.html', context)

# -------------------------------------------------------------------------
#this method to add new user to database
def addRegistrations(request):
    errors = Registration.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/')
    if request.method == 'POST':
            user=add_newreg(request.POST)
            request.session['reg_id'] = user.id 
            messages.success(request, "Successfully registered")
            
    return redirect('/success')

# -------------------------------------------------------------------------
#this method to add the email and passswored and hash the password and returns the error when logi with email and password invalid
def addLogin(request):
    errors = Registration.objects.basic_validatorlogin(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/')
    
    if request.method == 'POST':
        user = Registration.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['reg_id'] = logged_user.id
                return redirect('/success')
        messages.error(request, 'Invalid login credentials')
        return redirect('/')
    return redirect('/')

# -------------------------------------------------------------------------
#this method show the page when the user log in 
def showLogin(request):
    if 'reg_id' not in request.session:
        return redirect('/')
    else:
        context = {
            're_id': get_reid(request.session),
        }
        return render(request, 'show.html', context)

# -------------------------------------------------------------------------
#this method clean the sessions when log out 
def logOut(request):
    request.session.clear()
    return redirect('/')
