from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
Email_Regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
Name_Regex = re.compile(r'^[A-Za-z]+$')

# Create your models here.
class userManager(models.Manager):
    def validate (self, postData):
        errors = []
        if not Email_Regex.match(postData['email']):
            errors.append("Invalid email")
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors.append("Email already exists in our database")
        if postData['password'] != postData['confirm_password']:
            errors.append("Your passwords don't match")
        if len(postData['first_name']) < 2:
            errors.append("Is that really your first name?")
        if len(postData['last_name']) < 2:
            errors.append("Is that really your last name?")
        if not Name_Regex.match(postData['first_name']):
            errors.append("Is that number really in your first name?")
        if not Name_Regex.match(postData['last_name']):
            errors.append("Is that number really in your last name?")
        if len(postData['password']) < 8:
            errors.append("Password too short")
        if len(errors) == 0:
            #create the user
            newuser = User.objects.create(first_name= postData['first_name'], last_name= postData['last_name'], email= postData['email'], password= bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
            return (True, newuser)
        else:
            return (False, errors)

    def login(self, postData):
        errors1 = []
        if 'email' in postData and 'password' in postData:
            try:
                print 50*('8')
                user = User.objects.get(email = postData['email'])#userManage acceses the database using .get (finds that one user's object)
            except User.DoesNotExist: #if the user doesnt exist from the .get(.get returns nothin, this 'except' prevents an error message)
                print 50*('4')
                errors1.append("Sorry please try again")
                return (False, errors1)

        #password field/check
        pw_match = bcrypt.hashpw(postData['password'].encode(), user.password.encode())
        print 10*"3", user.password
        if pw_match == user.password:
            return (True, user)
        else:
            errors1.append("Sorry please try again!!!!")
            return (False, errors1)

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()

class secretManager(models.Manager):
    def validate (self, postData, userid):
        if len(postData)<3:
            return(False, "Secrets must be at least 3 characters long")
        print postData, userid
        try:
            currentuser = User.objects.get(id=userid)
            self.create(message=postData, author=currentuser)
            return(True, "Secret's safe with us")
        except:
            return(False, "We couldn't create this secret")

    def newlike(self, secretid, userid):
        try:
            secret = self.get(id=secretid)
        except:
            return(False, "Secret not found")
        user = User.objects.get(id=userid)
        if secret.author == user:
            return (False, "No self-love")
        secret.likers.add(user)
        return(True, "You liked this secret")

    def deleteLike(self,secretid,userid):
        try:
            secret = self.get(id=secretid)
        except:
            return(False, "Secret not found")
        user = User.objects.get(id=userid)
        if secret.author != user:
            return (False, "Don't delete others secrets")
        secret.delete()
        return (True, "Secret Deleted")

class Secret(models.Model):
    message = models.TextField(max_length=1000)
    likers= models.ManyToManyField(User, related_name="all_likes")
    author= models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = secretManager()
