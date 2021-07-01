from django.contrib.auth.models import User
from rest_framework import serializers, mixins
from rest_framework.viewsets import GenericViewSet
from planner.models import Person, Bio, Email, Task, Meeting
from datetime import date, timedelta
from django.utils import timezone
from datetime import date, timedelta, datetime
#from django.db.models.fields import TimeField

class BioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bio
        fields = [
           'id',
           'bio', 
           'image',
        ]

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = [
            'id',
            'address'
        ]

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(
        'get_owner'
    )

    person = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all(),
        write_only = True)

    def get_owner(self, obj):
        return obj.person.name

    # This method is called when posting a new Task
    def validate(self, data):
        errors = {}
        request = self.context['request']
        person = data['person']
        print(f'{request.user} == {person.user}')
        if person.user != request.user:
            print(f'{person.user} <> {request.user}')
            errors['error'] = f'Task owner has to be {request.user}'
            raise serializers.ValidationError(errors)
        #assert False
        return data

    class Meta:
        model = Task
        fields = '__all__'
        #write_only = [ 'person' ]


class MeetingSerializer(serializers.ModelSerializer):
    duration = serializers.IntegerField(initial=30)
    time = serializers.TimeField(initial='00:00')
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all(),
        write_only = True,
    )
    participants = serializers.PrimaryKeyRelatedField(
        write_only = True,
        many=True,
        queryset=Person.objects.all())

    participant_names = serializers.SerializerMethodField(
        'get_participants'
    )

    creator = serializers.SerializerMethodField(
        'get_creator'
    )

    # return meeting creator name instead of id
    def get_creator(self, obj):
        return { 'name': obj.created_by.name, 'id': obj.created_by.id }

    # return list participant names instead of ids
    def get_participants(self, obj):
        names = []
        for participant in obj.participants.all():
            names.append(participant.name)
        return names

    # This method is called when posting a new Meeting
    def validate(self, data):
        errors = {}
        request = self.context['request']
        created_by = data['created_by']
        if created_by.user != request.user:
            errors['error'] = f'Meeting has to be created by {request.user}'
            raise serializers.ValidationError(errors)
        #assert False
        return data

    class Meta:
        model = Meeting
        #fields = '__all__'
        fields = [
            'id',
            'title',
            'purpose',
            'date',
            'time',
            'duration',
            'created_by',
            'creator',
            'participants',
            'participant_names',
        ]


class PersonSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    bio  = BioSerializer()
    email  = EmailSerializer()
    tasks = TaskSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        return obj.my_status()

    class Meta:
        model = Person
        fields = [
            'id',
            'name',
            'age',
            'status',
            'user',
            'bio',
            'email',
            'tasks',
            'user',
        ]
        #read_only_fields = ['user']


    # instance is the Person object
    def update(self, instance, validated_data):
        user = instance.user

        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        bio = instance.bio
        bio_data = validated_data.pop('bio')
        bio.bio = bio_data.get('bio', bio.bio)
        bio.image = bio_data.get('image', bio.image)
        bio.save()

        email = instance.email
        email_data = validated_data.pop('email')
        email.address = email_data.get('address', email.address)
        email.save()

        return instance


    def create(self, validated_data):
        person_name = validated_data.pop('name')
        person_age = validated_data.pop('age')
        person_status = validated_data.pop('status')
        person = Person.objects.create(name=person_name, age=person_age, status=person_status)
        bio_data = validated_data.pop('bio')
        bio = Bio.objects.create(person=person, **bio_data)
        email_data = validated_data.pop('email')
        email = Email.objects.create(person=person, **email_data)
        user_name = validated_data.pop('user')
        user = User.objects.get(username = user_name)
        person.user = user
        person.save()

        return person
    


class UserSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'person',
            'email',
            'password',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email = validated_data['email'],
            username = validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
