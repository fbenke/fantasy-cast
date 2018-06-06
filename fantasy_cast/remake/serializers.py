from rest_framework import serializers
from remake.models import Remake


class RemakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Remake
        exclude = ('user',)


class RemakeNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Remake
        fields = '__all__'
        depth = 1
