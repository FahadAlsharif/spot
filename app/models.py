from email import message
from django.db import models
import bcrypt
import re
# Create your models here.


class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invali
        try  :
            if len(postData['email1']) == 0:
                errors['email_em'] = "Email cannot be empty"
                return errors
            user = User.objects.filter(email=postData['email1']) 
            if len(user) == 0:
                errors['email_e'] = "Email or Password is not correct"

            if (user[0].email != postData['email1']):
                errors['email_n'] = "Email or Password is not correct"

            if not bcrypt.checkpw(postData['password1'].encode(), user[0].password.encode()):
                errors['password'] = "Email or Password is not correct"
            return errors
        except :
            errors['email_exist'] = "Email does not exist!"
            return errors

    def register_validator(self, postData):
        email_re = re.compile(
            r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        errors = {}
        emails = User.objects.filter(email=postData['email'])
        if len(emails)>0:
            errors['emailExist']="This Email is already in use!"
            return errors
        if len(postData['fname']) < 2:
            if len(postData['fname']) == 0:
                errors['fname_empty'] = "First Name cannot be empty"
            else:
                errors['fname'] = "First Name should be at least 2 characters"

        if len(postData['lname']) < 2:
            if len(postData['lname']) == 0:
                errors['lname_empty'] = "Last Name cannot be empty"
            else:
                errors['lname'] = "Last Name should be at least 2 characters"

        if len(postData['email']) == 0:
            errors['email_empty'] = "Email cannot be empty"
        if not email_re.match(postData["email"]):
            errors["email"] = "Email address not valid."
        if len(postData['passward']) < 8:
            errors['passward'] = "Password should be more than 8  characters"

        if (postData['passward'] != postData['Cpassward']):
            errors["Cpassward"] = "Password and Confirm PW are not the same"

        return errors

class WishManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData["item"]) == 0:
            errors["item"] = "please enter a item."
        elif len(postData['item']) < 2:
            errors["item"] = "item must be longer than 2 characters"
        if len(postData["desc"]) == 0:
            errors["item"] = "please enter a Description."
        elif len(postData['desc']) < 5:
            errors["item"] = "Description must be longer than 5 characters"
        return errors  
    
class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wish(models.Model):
    item = models.CharField(max_length=255)
    desc = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name="wishs", on_delete = models.CASCADE)
    like = models.ManyToManyField(User, related_name="liked")
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
    objects = WishManager()

class Grantedd(models.Model):
    Gran = models.ForeignKey(Wish, related_name="wishd", on_delete = models.CASCADE)
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
