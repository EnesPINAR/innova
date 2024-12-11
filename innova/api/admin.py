from django.contrib import admin
from django import forms
from phonenumber_field.formfields import SplitPhoneNumberField
# Register your models here.
from .models import Movement, Meal, Program, Diet, User

admin.site.register(Movement)
admin.site.register(Meal)
admin.site.register(Program)
admin.site.register(Diet)


class UserForm(forms.ModelForm):
    phone_number = SplitPhoneNumberField(region="TR", help_text="Kullanıcı telefon numarası")
    
    class Meta:
        model = User
        fields = '__all__'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm