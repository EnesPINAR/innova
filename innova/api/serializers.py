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
    password = serializers.CharField(write_only=True, required=False)
    height = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'phone_number', 'first_name', 'last_name', 'height', 'weight',
            'birth_date', 'blood_type', 'membership_start', 'membership_end',
            'program', 'diet', 'age', 'active', 'remaining_days', 'password'
        ]
        read_only_fields = [
            'id', 'phone_number', 'first_name', 'last_name',
            'birth_date', 'blood_type', 'membership_start', 'membership_end',
            'program', 'diet'
        ]

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # Handle password separately if it's included
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        
        # Update height and weight
        if 'height' in validated_data:
            instance.height = validated_data.get('height')
        if 'weight' in validated_data:
            instance.weight = validated_data.get('weight')
        
        instance.save()
        return instance