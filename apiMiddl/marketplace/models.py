# from django.db import models
# from django.contrib.auth import get_user_model
# from django.contrib import admin

# # from items.models import Item

# User = get_user_model()

# class Tag(models.Model):
#     name = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return self.name 

# class SubscriptionOption(models.Model):
#     price = models.DecimalField(decimal_places=2,max_digits=10)
#     period = models.IntegerField()
#     #offering = models.ForeignKey(Offering, on_delete = models.CASCADE, related_name = "subscription_prices")

#     def __str__(self):
#         return "%d moneys for %d days" % (self.price, self.period)

# class Offering(models.Model):
#     title = models.CharField(max_length=200, blank=True, null=True)
#     price = models.DecimalField(decimal_places=2,max_digits=10)
#     tags = models.ManyToManyField(Tag, related_name = '+')
#     owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "+")
#     # item  = models.ForeignKey(Item, on_delete = models.CASCADE, null=True)
#     subscriptionOptions = models.ManyToManyField(SubscriptionOption)
#     description = models.TextField()
#     briefDescription = models.TextField()

#     def __str__(self):
#         return ' name:' + self.title

#     # @property
#     # def type(self):
#     #     return self.item.get_item().display_type_name


# class Review(models.Model):
#     rate = models.IntegerField()
#     topic = models.TextField(blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     offering = models.ForeignKey(Offering, on_delete = models.CASCADE)
#     owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "+")

#     def __str__(self):
#         return self.topic