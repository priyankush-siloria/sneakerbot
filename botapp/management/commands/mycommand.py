from django.core.management.base import BaseCommand, CommandError 

from .config import Config


from .ecombot import EcomBot


class Command(BaseCommand): 
	help = 'Does some magical work' 

	def handle(self, *args, **options): 
		""" Do your work here """

		bet = EcomBot(Config()) 