from api.views import CodeSubmissionViewSet, MathSubmissionViewSet, sign_up, login
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path
router = DefaultRouter()
router.register("submit/code", CodeSubmissionViewSet)
router.register("submit/math", MathSubmissionViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('signup/', sign_up, name='signup'),
]
urlpatterns += router.urls
