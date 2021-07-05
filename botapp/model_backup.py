from django.db import models
from django.contrib.auth.models import User




class UserProfile(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	first_name = models.CharField(max_length=140,null=True, blank=True)
	last_name = models.CharField(max_length=140,null=True, blank=True)



class Category(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False)

	def __str__(self):
		return self.name




class OrderedItem(models.Model):
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
	product_name  = models.CharField(max_length=120, null=True, blank=True)
	image = models.ImageField(null=False, blank=False)
	price = models.CharField(max_length=120, null=True, blank=True)
	total_price = models.CharField(max_length=120, null=True, blank=True)
	quantity = models.CharField(max_length=120, null=True, blank=True)
	color = models.CharField(max_length=120, null=True, blank=True)

	def __str__(self):
		return self.product_name





class SneakerItem(models.Model):
	sneaker_name  = models.CharField(max_length=120, null=True, blank=True)
	image = models.URLField(max_length = 200, null=True, blank=True)
	price = models.CharField(max_length=120, null=True, blank=True)
	color = models.CharField(max_length=120, null=True, blank=True)

	def __str__(self):
		return self.sneaker_name





class AvalSkuSize(models.Model):
	sku = models.CharField(max_length=120, null=True, blank=True)
	size = models.CharField(max_length=120, null=True, blank=True)
	sneaker_item = models.ForeignKey(OrderedItem, on_delete=models.CASCADE, null=True, blank=True)

	
	def __str__(self):
		return self.sku



class AllSkuSize(models.Model):
	sku = models.CharField(max_length=120, null=True, blank=True)
	size = models.CharField(max_length=120, null=True, blank=True)
	sneaker_item = models.ForeignKey(OrderedItem, on_delete=models.CASCADE, null=True, blank=True)

	
	def __str__(self):
		return self.sku
