from rest_framework import serializers
from .models import *



class Profileserializer (serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model=profile
        fields=['age','school','image','first_name','last_name']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = post
        fields = ['text','image']        