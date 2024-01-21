from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_the_test(self):
        self.recipe.title = 'A' * 70
        # aqui a validação ocorre, sem isso ele salvaria o título com mais de 65 caracteres
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
