from rest_framework import serializers
from core.models import Comment, Person


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = Comment.get_fields()


class AllPersonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'patronymic', 'surname']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = Person.get_fields()
