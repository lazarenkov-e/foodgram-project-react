import json

from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт ингредиентов из json в бд'

    def handle(self, *args, **kwargs):
        with open(
            'recipes/data/ingredients.json',
            'r',
            encoding='utf8',
        ) as file:
            data = json.load(file)

        for row in data:
            account = Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit'],
            )
            account.save()
