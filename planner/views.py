from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from planner.models import Person, Task, Meeting
from planner.serializers import PersonSerializer, UserSerializer, BioSerializer, EmailSerializer, TaskSerializer, MeetingSerializer
from planner.permissions import IsOwnerOrReadOnly, IsUserOrReadOnly, IsPersonOrReadOnly, IsCreatedByOrReadOnly
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Create your views here.
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsPersonOrReadOnly
    ]

#class UserViewSet(viewsets.ReadOnlyModelViewSet):
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # only allows GET and POST, all else as logged-in user
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        #IsUserOrReadOnly
    ]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    # return only the tasks for a person if pk is supplied
    def list(self, request, pk=None):
        if pk:
            #queryset = Task.objects.filter(person=pk)
            queryset = None
            try:
                person = get_object_or_404(Person, pk=pk)
                queryset = person.task_set.all()
            except:
                content = {'detail': f'Person {pk} Not found' }
                return Response(content, status=status.HTTP_404_NOT_FOUND)

        else:
            queryset = Task.objects.all()

        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsCreatedByOrReadOnly
    ]

    # return only the meetings for a person if pk is supplied
    def list(self, request, pk=None):
        if pk:
            #queryset = Meeting.objects.filter(created_by=pk)
            queryset = None
            try:
                person = get_object_or_404(Person, pk=pk)
                queryset = person.meeting_set.all()
            except:
                content = {'detail': f'Person {pk} Not found' }
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            #assert False
        else:
            queryset = Meeting.objects.all()

        serializer = MeetingSerializer(queryset, many=True, context = {'request': request})
        return Response(serializer.data)

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
        }
        return Response(content)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'meetings': reverse('meeting-list', request=request, format=format),
        'tasks': reverse('task-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'people': reverse('person-list', request=request, format=format),
    })
