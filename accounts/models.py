from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .tests import rand_x_digit_num as random_card

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	card_number 			= models.CharField(default=random_card(10), max_length=10)
	money                   = models.FloatField(default=10)


	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

class Card(models.Model):
	owner = models.ForeignKey(Account, on_delete=models.CASCADE)
	number = models.CharField(default=random_card(10), max_length=10)
	money = models.FloatField(default=10)
	objects = models.Manager()


class Transaction(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	sender = models.ForeignKey(Card, on_delete = models.CASCADE, related_name='sender')
	receiver = models.ForeignKey(Card, on_delete = models.CASCADE, related_name='receiver')
	sent_money = models.CharField(max_length=30)
	time_sent = models.DateTimeField(auto_now_add=True)
	objects = models.Manager()

	def __str__(self):
		return str(self.id)
	def __repr__(self):
		return 'Sender: ' + self.sender + ' Receiver: ' + self.receiver + ' Money: ' + self.sent_money