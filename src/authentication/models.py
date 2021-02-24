from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
# User = get_user_model()


from django.conf import settings
from django.utils import timezone


from django.contrib.auth.hashers import make_password
# Create your models here.

class AccountManager(BaseUserManager):
	def create_user(self, email, username,first_name, last_name, date_of_birth, password=None, password2=None):
		if not email:
			raise ValueError('Users must have an email address')

		if not username:
			raise ValueError('Users must have a username')
        # if not password:
		# 	raise ValueError('Users must have a password')

		user = self.model(email=self.normalize_email(email),username=username,first_name=first_name,last_name=last_name,date_of_birth=date_of_birth)
		user.set_password(password)#validated_data['password'])
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password=None):

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

#user a token vermek: python manage.py drf_create_token username 

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique= True,db_index=True)
    first_name = models.CharField(max_length=30,null=True) # Databasedeki userlar silinmesin diye null true dedim. Duzeltilecek
    last_name = models.CharField(max_length=30,null=True) # Databasedeki userlar silinmesin diye null true dedim. Duzeltilecek
    email = models.EmailField(max_length = 60, unique=True)
    date_of_birth = models.DateField(null=True)
    #passwordHash = models.CharField(max_length=100)
    emailConf = models.BooleanField(default=False)
    #phoneNum = models.CharField(max_length=10) #UserContactTableında kullanıyorum, bir user birden fazla adres ve numara ekleyebilir satın alırken
    # lastOnline = models.DateTimeField(auto_now=True)
    # dateCreated = models.DateTimeField(auto_now_add=True)
    dateDeleted = models.DateTimeField(auto_now=True, null=True)
    averageRate = models.DecimalField(null = True, max_digits=3, decimal_places=2)

    ###ABSTRACT BASE USER Required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' #Login with email
    REQUIRED_FIELDS = ['username'] #Require username while logging in

    objects = AccountManager()


    SALES_MANAGER = 'SM'
    PRODUCT_MANAGER = 'PM'
    CUSTOMER = 'CU'
    POSSIBLE_ROLES = [
        (SALES_MANAGER, 'Sales Manager'),
        (PRODUCT_MANAGER, 'Product Manager'),
        (CUSTOMER, 'Customer'),
        ]

    userRole = models.CharField(
        max_length=2,
        choices=POSSIBLE_ROLES,
        default=CUSTOMER,
        )


    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    # Why did we allow to have blank in dateDeleted field? I think we should make it NULL
    #isDeleted = models.BooleanField(default=False) # Do we need is deleted part?

    # def __str__(self):
    #     if self.first_name != None and self.last_name != None:
    #         return "%s %s" % (self.first_name, self.last_name)
    #     else:
    #         return self.username

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

