from rest_framework import serializers
from .models import Parent, Kids, Student


class ParentProfileSerializer(serializers.ModelSerializer):
    # Custom serializer method field to include the username
    username = serializers.SerializerMethodField()

    class Meta:
        model = Parent
        fields = [
            'id',
            'name',
            'address',
            'province',
            'phone',
            'email',
            'debt',
            'date_joined',
            'uniqueId',
            'slug',
            'date_created',
            'last_updated',
            'user',
            'profile',
            'username',  # Include the custom 'username' field in the response
        ]

    # Custom method to get the username of the associated user
    def get_username(self, parent):
        # Access the username of the associated user through the 'profile' field
        return parent.profile.username


class ParentProfileUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        # Update username if provided
        if 'username' in validated_data:
            instance.profile.username = validated_data['username']
        # Update password if provided
        if 'password' in validated_data:
            instance.profile.set_password(validated_data['password'])

        # Save the changes to the parent's profile
        instance.profile.save()
        return instance


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'


class KidsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kids
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
