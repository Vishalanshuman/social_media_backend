from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email','role', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        if not attrs.get('username') and not attrs.get('email'):
            raise serializers.ValidationError({"username": "Username or email is required."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password before saving
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')

        # Authenticate user using either username or email
        user = authenticate(username=username_or_email, password=password)

        if user is None:
            try:
                # Try to find the user by email if authentication fails
                user = User.objects.get(email=username_or_email)
                if not user.check_password(password):
                    user = None
            except User.DoesNotExist:
                user = None

        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        attrs['user'] = user
        return attrs
    

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email','role']