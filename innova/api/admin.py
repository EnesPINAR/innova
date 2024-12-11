from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from phonenumber_field.formfields import SplitPhoneNumberField
from .models import Movement, Meal, Program, Diet, User

admin.site.register(Movement)
admin.site.register(Meal)
admin.site.register(Program)
admin.site.register(Diet)

class CustomUserCreationForm(UserCreationForm):
    phone_number = SplitPhoneNumberField(region="TR", help_text="Kullanıcı telefon numarası")
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('phone_number', 'first_name', 'last_name')

class CustomUserChangeForm(UserChangeForm):
    phone_number = SplitPhoneNumberField(region="TR", help_text="Kullanıcı telefon numarası")
    
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('phone_number', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {
            'fields': (
                'first_name', 
                'last_name', 
                'height', 
                'weight', 
                'birth_date', 
                'blood_type'
            )
        }),
        ('Membership', {
            'fields': (
                'membership_start', 
                'membership_end', 
                'program', 
                'diet'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser', 
                'groups', 
                'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': (
                'last_login', 
                'date_joined'
            )
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone_number', 
                'first_name', 
                'last_name',
                'height',
                'weight',
                'birth_date',
                'blood_type',
                'membership_start',
                'membership_end',
                'program',
                'diet',
                'password1', 
                'password2'
            ),
        }),
    )
    
    search_fields = ('phone_number', 'first_name', 'last_name')
    ordering = ('phone_number',)