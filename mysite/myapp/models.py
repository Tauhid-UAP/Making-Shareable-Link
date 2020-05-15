from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.db import models

# Create your models here.

class MyAccountManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user=self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user





class MyUser(AbstractBaseUser):

    # required to include
    email = models.EmailField(verbose_name='email', unique=True, max_length=60)
    username = models.CharField(max_length=60, unique=True)
    date_joined = models.DateField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # new
    first_name = models.CharField(max_length=60, verbose_name='first name')
    last_name = models.CharField(max_length=60, verbose_name='last name')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class PageRandCode(models.Model):
    myuser = models.OneToOneField(to=MyUser, on_delete=models.CASCADE)
    # random_code = models.PositiveIntegerField()
    random_code = models.CharField(max_length=20)

class MyContent(models.Model):
    myuser = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=50, blank=True)