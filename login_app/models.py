from django.db import models
import bcrypt
import re
from datetime import datetime 
from django.core.exceptions import ObjectDoesNotExist

class UserManager(models.Manager):
    def basic_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['firstname']) < 2:
            errors["firstname"] = "First name should be at least 2 characters"
        if len(postData['lastname']) < 2:
            errors["lastname"] = "Last name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if  Registration.objects.filter(email=postData['email']).exists():
            errors['email'] = "Email already exists"
        if postData['password'] != postData['copassword']:
            errors['password_match'] = "Passwords do not match"
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = "Invalid email address!"
            # validated dob to required in database and age grater than 13
        if not postData['birthday']:
            errors["birthday"] = "Date of Birth is required"
        else:
                biryhday = datetime.strptime(postData['birthday'], "%Y-%m-%d").date()
                today = datetime.now().date()
                age = today.year - biryhday.year
                if biryhday >= today:
                    errors["birthday_past"] = "Date of Birth must be in the past"
                elif age < 13:
                    errors["birthday"] = "Age must be at least 13 years"
        return errors
    def basic_validatorlogin(self,postData):
            errors = {}
            try:
                user = Registration.objects.get(email=postData['email'])
            except ObjectDoesNotExist:
                errors['email'] = "Email not found."
                return errors
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = "Invalid password."
            return errors




class Registration(models.Model):
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    password=models.CharField(max_length=255)
    copassword=models.CharField(max_length=255)
    birthday = models.DateField(default=datetime.today)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()



    def __str__(self):
        return f"{self.firstname}"


def all_registrations():
    return Registration.objects.all()


def add_newreg(POST):
    password = bcrypt.hashpw(POST['password'].encode(), bcrypt.gensalt()).decode()
    copassword=bcrypt.hashpw(POST['copassword'].encode(), bcrypt.gensalt()).decode()
    registration = Registration.objects.create(
        firstname=POST['firstname'],
        birthday=POST['birthday'],
        lastname=POST['lastname'],
        email=POST['email'],
        password=password,
        copassword=copassword
    )
    return registration
            

def get_reid(session):
    return Registration.objects.get(id=session['reg_id'])



