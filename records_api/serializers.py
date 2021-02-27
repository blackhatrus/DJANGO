from rest_framework import serializers
from records.models import Record, RecordHistory
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username')


class RecordHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = RecordHistory
        fields = ('created', 'response')


class RecordListSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )
    recordhistory = RecordHistorySerializer(many=True)
    
    class Meta:
        model = Record
        fields = ('title', 'url', 'category', 'recordhistory')
    