from rest_framework import serializers

from .models import Partner1C, ParentChild1C


class Partner1CSerializer(serializers.ModelSerializer):

    class Meta:
        model = Partner1C
        fields = '__all__'


class ParentChild1CSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParentChild1C
        fields = '__all__'
