from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from recipes.permissions import IsAuthorOrAdminPermission
from recipes.serializers import (FavoriteSerializer, IngredientSerializer,
                                 RecipeAddSerializer, RecipeSerializer,
                                 ShoppingCartSerializer, TagSerializer)
from recipes.utils import create_entity, delete_entity
from rest_framework import decorators, permissions, viewsets


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrAdminPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return RecipeAddSerializer
        return RecipeSerializer

    @decorators.action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[
            permissions.IsAuthenticated,
        ],
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return create_entity(request, recipe, FavoriteSerializer)

        if request.method == 'DELETE':
            error_message = 'У вас нет этого рецепта в избранном!'
            return delete_entity(request, Favorite, recipe, error_message)

    @decorators.action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[
            permissions.IsAuthenticated,
        ],
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return create_entity(request, recipe, ShoppingCartSerializer)

        if request.method == 'DELETE':
            error_message = 'У вас нет этого рецепта в списке покупок!'
            return delete_entity(request, ShoppingCart, recipe, error_message)

    @decorators.action(
        detail=False,
        methods=['GET'],
        permission_classes=[
            permissions.IsAuthenticated,
        ],
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = (
            IngredientRecipe.objects.filter(recipe__carts__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(ingredient_amount=Sum('amount'))
        )
        shopping_list = [f'Список покупок для {user.get_full_name()}:\n']
        number = 1
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            amount = ingredient['ingredient_amount']
            unit = ingredient['ingredient__measurement_unit']
            shopping_list.append(f'\n{number}. {name} - {amount}, {unit}')
            number += 1
        response = HttpResponse(shopping_list, content_type='text/plain')
        response[
            'Content-Disposition'
        ] = 'attachment; filename="shopping_list.txt"'
        return response
