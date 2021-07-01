from django.urls import path, include
from rest_framework.routers import DefaultRouter
from planner import views
from planner.views import PersonViewSet, TaskViewSet, UserViewSet, MeetingViewSet

router = DefaultRouter()
router.register(r'people', views.PersonViewSet)
#router.register(r'users', views.UserViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'meetings', views.MeetingViewSet)

# Ordering of paths is important
# The more generic should be last, path('', include(router.urls))
urlpatterns = [
    path(
        'users',
        UserViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
    ),
    path(
        'people/',
        PersonViewSet.as_view({
        'get': 'list',
        'post': 'create',
        })
    ),
    path(
        'tasks/people/<pk>/',
        TaskViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
    ),
    path(
        'meetings/people/<pk>/',
        MeetingViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
    ),
    path('', include(router.urls)),
]
