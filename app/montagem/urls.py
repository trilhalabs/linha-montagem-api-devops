from django.urls import path, include
from rest_framework.routers import DefaultRouter

from montagem import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('atributos', views.AtributoViewSet)
router.register('montagens', views.MontagemViewSet)

app_name = 'montagem'

urlpatterns = [
    path('', include(router.urls))
]
