from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    about = models.TextField(blank=False, null=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=False, null=True)
    otp_code = models.TextField(blank=False, null=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    # organization = models.ForeignKey(Organization, models.DO_NOTHING, blank=True, null=True)
    # roles = models.ManyToManyField(Role, related_name = '+')

    class Meta:
        db_table = "users"

    def __str__(self):
        return str(self.name)

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'about': self.about,
            'image': self.image,
            'otp_code': self.otp_code,
            'verified': self.verified,
        }

# class Permission(models.Model):
#     name = models.CharField(max_length=200)

# class Role(models.Model):
#     name = models.CharField(max_length=200)
#     permissions = models.ManyToManyField(Permission, related_name = '+')

# class Organization(models.Model):
#     name = models.CharField(unique=True, max_length=200, blank=True, null=True)
#     about = models.TextField(blank=True, null=True)
#     logo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
#     creation_ts = models.DateTimeField(default=datetime.now, blank=True, null=True)

#     def __str__(self):
#         return self.name
        