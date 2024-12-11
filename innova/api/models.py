from django.db import models
from datetime import date
from django.core.validators import BaseValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, UserManager

class MinValueValidator(BaseValidator):
    message = "Bu değer %(limit_value)s değerinden büyük veya eşit olmalıdır."
    code = "min_value"

    def compare(self, a, b):
        return a < b

# Create your models here.
class Movement(models.Model):
    name = models.CharField(max_length=200)
    video = models.URLField(max_length=200, help_text='YouTube video linki')
    sets = models.IntegerField(default=3, help_text='Set sayısı', validators=[MinValueValidator(1)])
    reps = models.IntegerField(default=12, help_text='Tekrar sayısı', validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Hareket'
        verbose_name_plural = 'Hareketler'

class Meal(models.Model):
    name = models.CharField(max_length=200)
    amount = models.IntegerField()
    unit = models.CharField(
        max_length=10,
        choices=[
            ('piece', 'Adet'),
            ('gram', 'Gram'), 
            ('liter', 'Litre')
        ],
        default='piece'
    )
    protein = models.IntegerField(default=0, help_text='Protein miktarı (gram)')
    carbs = models.IntegerField(default=0, help_text='Karbonhidrat miktarı (gram)')
    oil = models.IntegerField(default=0, help_text='Yağ miktarı (gram)')
    calories = models.IntegerField(default=0, help_text='Kalori miktarı (kcal)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Yemek'
        verbose_name_plural = 'Yemekler'

class Program(models.Model):
    name = models.CharField(max_length=200)
    movements = models.ManyToManyField(Movement, help_text='Birden fazla seçmek için CTRL tuşuna basılı tutun.')
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Program'
        verbose_name_plural = 'Programlar'

class Diet(models.Model):
    
    meals = models.ManyToManyField(Meal, help_text='Birden fazla seçmek için CTRL tuşuna basılı tutun.')
    @property
    def name(self):
        total_calories = sum(meal.calories for meal in self.meals.all())
        return f"{total_calories} Kcal Diyet"
    @property
    def total_calories(self):
        return sum(meal.calories for meal in self.meals.all())
    @property
    def total_protein(self):
        return sum(meal.protein for meal in self.meals.all())
        
    @property
    def total_carbs(self):
        return sum(meal.carbs for meal in self.meals.all())
        
    @property
    def total_oil(self):
        return sum(meal.oil for meal in self.meals.all())
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Diyet'
        verbose_name_plural = 'Diyetler'

class CustomUserManager(UserManager):
    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be set')
        if not extra_fields.get('first_name'):
            raise ValueError('First name must be set')
        if not extra_fields.get('last_name'):
            raise ValueError('Last name must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
    BLOOD_TYPES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'), 
        ('B-', 'B-'),
        ('AB+', 'AB-'),
        ('AB-', 'AB-'),
        ('0+', '0+'),
        ('0-', '0-'),
    ]
    
    username = None
    phone_number = PhoneNumberField(
        unique=True,
        default='+900000000000', 
        help_text='Kullanıcı telefon numarası'
    )
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    height = models.DecimalField(max_digits=5, decimal_places=2, help_text='Boy (cm)', null=True, blank=True, editable=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text='Kilo (kg)', null=True, blank=True, editable=True) 
    birth_date = models.DateField(null=True, blank=True, editable=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES, null=True, blank=True, editable=True)
    membership_start = models.DateField(help_text='Üyelik başlangıç tarihi', default=date.today, blank=False, editable=True)
    membership_end = models.DateField(help_text='Üyelik bitiş tarihi', null=True, blank=False, editable=True)
    program = models.ForeignKey('Program', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Program')
    diet = models.ForeignKey('Diet', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Diyet')
    
    def clean(self):
        import re
        if self.phone_number:
            if not re.match(r'^\+?1?\d{9,15}$', str(self.phone_number)):
                from django.core.exceptions import ValidationError
                raise ValidationError({
                    'phone_number': 'Telefon numarası "+999999999" formatında girilmelidir. En fazla 15 rakam kullanılabilir.'
                })
        if not self.first_name:
            from django.core.exceptions import ValidationError
            raise ValidationError({
                'first_name': 'First name is required.'
            })
        if not self.last_name:
            from django.core.exceptions import ValidationError
            raise ValidationError({
                'last_name': 'Last name is required.'
            })

    @property
    def active(self):
        today = date.today()
        return today <= self.membership_end if self.membership_end else False

    @property
    def age(self):
        if not self.birth_date:
            return None
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    @property
    def remaining_days(self):
        if not self.membership_end:
            return None
        today = date.today()
        remaining = self.membership_end - today
        return remaining.days

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'

    objects = CustomUserManager()

