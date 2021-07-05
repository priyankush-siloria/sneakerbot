from django.db import models
from django.contrib.auth.models import User




class UserProfile(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	first_name = models.CharField(max_length=140,null=True, blank=True,verbose_name='First Name')
	last_name = models.CharField(max_length=140,null=True, blank=True,verbose_name='Last Name')



class Category(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False)

	def __str__(self):
		return self.name

class Address(models.Model):
	fname = models.CharField(max_length=140,null=True, blank=True,verbose_name='First Name')
	lname = models.CharField(max_length=140,null=True, blank=True,verbose_name='Last Name')
	created = models.DateTimeField(auto_now_add=True)
	address_line1 = models.CharField(max_length=140,null=True, blank=True,verbose_name='Address Line 1')
	address_line2 = models.CharField(max_length=140,null=True, blank=True,verbose_name='Address Line 2')
	address_line3 = models.CharField(max_length=140,null=True, blank=True,verbose_name='Address Line 3')
	postal_code = models.CharField(max_length=6,null=True, blank=True,verbose_name='Postal Code')
	state = models.CharField(max_length=60,null=True, blank=True,verbose_name='State')
	email = models.CharField(max_length=140,null=True, blank=True,verbose_name='Email')
	full_address = models.CharField(max_length=200,null=True, blank=True,verbose_name='Full Address')


class OrderedItem(models.Model):
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
	product_name  = models.CharField(max_length=120, null=True, blank=True)
	product_img_url = models.URLField(max_length = 200, null=True, blank=True)
	status = models.CharField(max_length=120, null=True, blank=True)
	price = models.CharField(max_length=120, null=True, blank=True)
	sku = models.CharField(max_length=120, null=True, blank=True)
	size = models.CharField(max_length=120, null=True, blank=True)
	total_price = models.CharField(max_length=120, null=True, blank=True)
	quantity = models.CharField(max_length=120, null=True, blank=True)
	color = models.CharField(max_length=120, null=True, blank=True)
	country = models.CharField(max_length=120, null=True, blank=True)
	address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.product_name
