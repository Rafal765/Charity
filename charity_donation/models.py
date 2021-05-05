from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


TYPES = (
        ('f', 'fundacja'),
        ('o', 'organizacja rządowa'),
        ('z', 'zbiórka lokalna'),
        )


class Category(models.Model):
    """
    name: name of the category
    """
    name = models.CharField(max_length=64)


class Institution(models.Model):
    """
    name: name of an institution
    description: description of the institution
    type: type of institution (availible: 'fundacja', 'organizacja rządowa', 'zbiórka lokalna')
    categories: applicable categories from Category model
    """
    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.CharField(max_length=1, choices=TYPES, default='f')
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    """
    quantity: amount of bags
    categories: applicable categories from Category model
    institution: related institution from Institution model
    address, city, zip_code: where bags await
    phone_number: your contact number
    pick_up_time, pick_up_date: when bags are supposed to be taken
    pick_up_comment: additional comment
    user: website user who donates
    is_taken: user confirms whether donation was taken
    """
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    phone_number = PhoneNumberField()
    city = models.CharField(max_length=64)
    zip_code = models.IntegerField()
    pick_up_date = models.DateField(auto_now=False, auto_now_add=False)
    pick_up_time = models.TimeField(auto_now=False, auto_now_add=False)
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
    is_taken = models.BooleanField(default=False)

