from rest_framework.serializers import ModelSerializer, ValidationError
from remake import models


class RemakeNestedSerializer(ModelSerializer):

    class Meta:
        model = models.Remake
        fields = '__all__'
        depth = 1


class CharacterSerializer(ModelSerializer):

    class Meta:
        model = models.Character
        exclude = ('remake',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not ret['id']:
            ret['id'] = instance.tmdb_id if instance.tmdb_id else instance.imdb_principal.id
        return ret


class RemakeSerializer(ModelSerializer):

    characters = CharacterSerializer(many=True)

    class Meta:
        model = models.Remake
        fields = '__all__'
        read_only_fields = ('user',)
        extra_kwargs = {'characters': {'write_only': True}}

    def create(self, validated_data):
        characters_data = validated_data.pop('characters')
        remake = models.Remake.objects.create(**validated_data)
        for character_data in characters_data:
            models.Character.objects.create(remake=remake, **character_data)
        return remake

    def validate(self, data):
        if len(data.get('characters')) < 1:
            raise ValidationError('must specify at least one character')
        return data
