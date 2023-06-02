from django.urls import include, path
from rest_framework.routers import DefaultRouter
from recipes.views import TagViewSet, IngredientViewSet

app_name = 'recipes'

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [path('', include(router.urls))]
