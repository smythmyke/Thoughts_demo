from django.db import models
from django.db.models.fields.related import ForeignKey, RelatedField
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class user_manager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['first_name']) <2:
            errors['first_name'] = "Please enter your first name."
        if len(postData['last_name']) <2:
            errors['last_name'] = "Please enter your last name."
        chkmail = self.filter(email = postData['email']) 
        if chkmail:
            errors['email'] = 'This email is in use.' 
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid Email Address'
        if len(postData['password'])<8:
            errors['password']='Your password is too short.'
        if postData['password']!=postData['conf_password']:
            errors['dup_pass']="Your passwords don't match!"
            
        return errors
    def login_validate(self, postData):
        errors = {}
        chkmail = self.filter(email = postData['email']) 
        if not chkmail:
            errors['email'] = 'invalid email or password' 
        # bcrypt again does not work for some reason on this computer, but here I would assign user to the first (and only) instance of a matched email and then pass it to bcrypt so that the check function would check the decoded salt versions. This value is passed back.
        # user = chkmail[0]
        # return bcrypt.checkpw(password.encode(), user.password.encode())
        return errors
    
class user(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=user_manager()
    
    
    

class thought_manager(models.Manager):
    def validate (self, postData):
        errors = {}
        if len(postData['thoughts']) <5:
            errors['thought'] = "Please enter a thought longer than 5 characters."
        return errors



class thought(models.Model):
    thoughts=models.CharField(max_length=255)
    posted_by=models.ForeignKey(user, related_name="posted_thoughts", on_delete=models.CASCADE)
    liked_by=models.ManyToManyField(user, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=thought_manager()
    
    