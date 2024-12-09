from rest_framework import serializers
from .models import CustomUser, Participant, Scores, Criterios

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('username', 'fullname', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Удаляем вторую проверку пароля
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            fullname=validated_data['fullname'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class SetScoreSerializer(serializers.Serializer):
    participant_id = serializers.IntegerField()
    juri_id = serializers.IntegerField()
    criterion_id = serializers.IntegerField()
    stage = serializers.IntegerField()
    score = serializers.CharField(max_length=512)

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'full_name', 'place_of_study', 'teacher_full_name', 'teacher_phone']

class CriteriosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criterios
        fields = ['id', 'criterion', 'stage', 'created_at']