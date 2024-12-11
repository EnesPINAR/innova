from django.contrib import admin

# Register your models here.
from .models import Movement, Meal, Program, Diet, User

admin.site.register(Movement)
admin.site.register(Meal)
admin.site.register(Program)
admin.site.register(Diet)
admin.site.register(User)
