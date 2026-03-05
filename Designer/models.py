from django.db import models

# Create your models here.
class userDB(models.Model):
    username = models.CharField(null = True, blank = True, max_length= 30)
    email = models.CharField(null = True, blank = True, max_length = 40)
    password = models.CharField(null = True, blank = True, max_length = 128)
    designation = models.CharField(null=True, blank=True, max_length = 128)
    profileimage = models.ImageField(upload_to="images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class projectDB(models.Model):
    email = models.CharField(null=True, blank=True, max_length=30)
    projectname = models.CharField(null=True, blank=True, max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    cssstyle = models.TextField(null=True, blank=True)
    htmlcode = models.TextField(null=True, blank=True)


class inheritanceDB(models.Model):
    email = models.CharField(null=True, blank=True, max_length=30)
    projectname = models.CharField(null=True, blank=True, max_length=40)

    child = models.CharField(null=True, blank=True, max_length=30)
    parent = models.CharField(null=True, blank=True, max_length=30)

class styleDB(models.Model):
    email = models.CharField(null=True, blank=True, max_length=30)
    projectname = models.CharField(null=True, blank=True, max_length=40)
    classname = models.CharField(null=True, blank=True, max_length=30)
    LHS = models.CharField(null=True, blank=True, max_length=30)
    RHS = models.CharField(null=True, blank=True, max_length=30)
    Animation = models.CharField(null = True, blank = True, max_length = 30)

class divisionDB(models.Model):
    divname = models.CharField(null=True, blank=True, max_length=30)
    email = models.CharField(null=True, blank=True, max_length=30)
    projectname = models.CharField(null=True, blank=True, max_length=40)



class imageDB(models.Model):
    email = models.CharField(null=True, blank=True, max_length=30)
    projectname = models.CharField(null=True, blank=True, max_length=40)
    imagename = models.CharField(null=True, blank=True, max_length=40)

    image = models.ImageField(upload_to="images", null=True, blank=True)


class inputDB(models.Model):
    email = models.CharField(null=True, blank=True, max_length=30)
    projectname = models.CharField(null=True, blank=True, max_length=40)
    inputname = models.CharField(null=True, blank=True, max_length=30)
    placeholder = models.CharField(null=True, blank=True, max_length=30)
    inputtype = models.CharField(null=True, blank=True, max_length=30)




class textDB(models.Model):
    email = models.CharField(null=True, blank=True, max_length=30)
    projectname = models.CharField(null=True, blank=True, max_length=40)
    textcontent = models.CharField(null=True, blank=True, max_length=256)
    textname = models.CharField(null=True, blank=True, max_length=30)








