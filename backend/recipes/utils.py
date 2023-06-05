from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from recipes.models import IngredientRecipe, Ingredient


def create_ingredients(ingredients, recipe):
    ingredient_list = []
    for ingredient in ingredients:
        current_ingredient = get_object_or_404(Ingredient,
                                               id=ingredient.get('id'))
        amount = ingredient.get('amount')
        ingredient_list.append(
            IngredientRecipe(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=amount
            )
        )
    IngredientRecipe.objects.bulk_create(ingredient_list)


def create_model_instance(request, instance, serializer_name):
    serializer = serializer_name(
        data={'user': request.user.id, 'recipe': instance.id, },
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_model_instance(request, model_name, instance, error_message):
    if not model_name.objects.filter(user=request.user,
                                     recipe=instance).exists():
        return Response({'errors': error_message},
                        status=status.HTTP_400_BAD_REQUEST)
    model_name.objects.filter(user=request.user, recipe=instance).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
