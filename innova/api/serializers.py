from rest_framework import serializers
from .models import Movement, Meal, Program, Diet, User
from django.contrib.auth.hashers import make_password, check_password

class MovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        fields = ['id', 'name', 'video', 'sets', 'reps']

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'name', 'amount', 'unit', 'protein', 'carbs', 'oil', 'calories']

class ProgramSerializer(serializers.ModelSerializer):
    movements = MovementSerializer(many=True, read_only=True)

    class Meta:
        model = Program
        fields = ['id', 'name', 'movements']

class DietSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True, read_only=True)
    total_calories = serializers.ReadOnlyField()
    total_protein = serializers.ReadOnlyField()
    total_carbs = serializers.ReadOnlyField()
    total_oil = serializers.ReadOnlyField()

    class Meta:
        model = Diet
        fields = ['id', 'name', 'meals', 'total_calories', 'total_protein', 'total_carbs', 'total_oil']

class UserSerializer(serializers.ModelSerializer):
    program = ProgramSerializer(read_only=True)
    diet = DietSerializer(read_only=True)
    age = serializers.ReadOnlyField()
    active = serializers.ReadOnlyField()
    remaining_days = serializers.ReadOnlyField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'phone_number', 'first_name', 'last_name', 'height', 'weight',
            'birth_date', 'blood_type', 'membership_start', 'membership_end',
            'program', 'diet', 'age', 'active', 'remaining_days', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        # Ensure password is hashed before saving
        if self._state.adding or self._password_changed:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    @classmethod
    def authenticate(cls, phone_number, password):
        try:
            user = cls.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except cls.DoesNotExist:
            pass
        return None 