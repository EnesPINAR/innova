from django.db import models
from datetime import date
from django.core.validators import BaseValidator
from phonenumber_field.modelfields import PhoneNumberField

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

class User(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'), 
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('0+', '0+'),
        ('0-', '0-'),
    ]
    
    phone_number = PhoneNumberField(default='+900000000000', help_text='Kullanıcı telefon numarası', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, help_text='Kullanıcı adı')
    surname = models.CharField(max_length=100, null=True, help_text='Kullanıcı soyadı')
    password = models.CharField(max_length=128, help_text='Kullanıcı şifresi')
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text='Boy (cm)', null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text='Kilo (kg)', null=True, blank=True) 
    birth_date = models.DateField(null=True, blank=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES, null=True, blank=True)
    membership_start = models.DateField(help_text='Üyelik başlangıç tarihi', default=date.today, blank=False)
    membership_end = models.DateField(help_text='Üyelik bitiş tarihi', null=True, blank=False)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Program')
    diet = models.ForeignKey(Diet, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Diyet')
    
    def clean(self):
        import re
        if self.phone_number:
            if not re.match(r'^\+?1?\d{9,15}$', str(self.phone_number)):
                from django.core.exceptions import ValidationError
                raise ValidationError({
                    'phone_number': 'Telefon numarası "+999999999" formatında girilmelidir. En fazla 15 rakam kullanılabilir.'
                })

    def save(self, *args, **kwargs):
        # First validate required fields
        validation_errors = {}
        
        if not self.phone_number:
            validation_errors['phone_number'] = 'Telefon numarası zorunludur.'
        
        if not self.password:
            validation_errors['password'] = 'Şifre zorunludur.'
        
        if not self.name or not self.surname:
            validation_errors['name'] = 'Ad ve soyad zorunludur.'

        if not self.membership_start:
            validation_errors['membership_start'] = 'Üyelik başlangıç tarihi zorunludur.'
            
        if not self.membership_end:
            validation_errors['membership_end'] = 'Üyelik bitiş tarihi zorunludur.'
        
        if validation_errors:
            from django.core.exceptions import ValidationError
            raise ValidationError(validation_errors)
            
        self.clean()

        super().save(*args, **kwargs)

    @classmethod
    def authenticate(cls, phone_number, password):
        try:
            user = cls.objects.get(phone_number=phone_number)
            if user.password == password:  # TODO use hashing
                return user
        except cls.DoesNotExist:
            pass
        return None

    @property
    def active(self):
        from datetime import date
        today = date.today()
        return today <= self.membership_end if self.membership_end else False

    @property
    def age(self):
        if not self.birth_date:
            return None
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    @property
    def remaining_days(self):
        if not self.membership_end:
            return None
        from datetime import date
        today = date.today()
        remaining = self.membership_end - today
        return remaining.days

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'



