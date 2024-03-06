from unittest import TestCase
from recipes.tests.test_recipe_base import RecipeTestBase
from utils.pagination import make_pagination_range
from django.urls import reverse
from unittest.mock import patch


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa: E501
        # Current page = 1 - Qty Page = 2 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 2 - Qty Page = 2 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 3 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

        # Current page = 4 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4,
        )['pagination']
        self.assertEqual([3, 4, 5, 6], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        # Current page = 10 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)

        # Current page = 14 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=12,
        )['pagination']
        self.assertEqual([11, 12, 13, 14], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        # Current page = 18 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        # Current page = 19 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        # Current page = 20 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        # Current page = 21 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=21,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)


class IntegrationPaginationTest(RecipeTestBase):
    def test_make_pagination_current_page_is_one_if_not_page_attr_in_request(self):
        for i in range(1, 6):
            kwargs = {
                'slug': f's-{i}', 'author_data': {'username': f'user{i}'}, 'title': f'title {i}'}
            self.make_recipe(**kwargs)
        url = reverse('recipes:home')

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(f'{url}?page=1a').context['recipes']
            self.assertEqual(1, response.number)


# TODO: DA FORMA ABAIXO ERA COMO EU TINHA FEITO. ESTÁ FUNCIONANDO DE MANEIRA MAIS DINÂMICA, CONTUDO, TA MAIS DEMORADO
# from unittest import TestCase
# from django.urls import reverse
# from django.http import request
# from utils.pagination import make_pagination_range
# from recipes.tests.test_recipe_base import RecipeTestBase
# import math


# class PaginationTest(RecipeTestBase):
#     def test_make_pagination_range_returns_a_pagination_range(self):
#         pagination = make_pagination_range(
#             page_range=list(range(1, 21)),
#             qty_pages=4,
#             current_page=1,
#         )['pagination']
#         self.assertEqual([1, 2, 3, 4], pagination)

#     def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa: E501
#         # Current page = 1 - Qty Page = 4 - Middle Page = 2
#         pagination = make_pagination_range(
#             page_range=list(range(1, 21)),
#             qty_pages=4,
#             current_page=1,
#         )['pagination']
#         self.assertEqual([1, 2, 3, 4], pagination)

#         # Current page = 2 - Qty Page = 4 - Middle Page = 2
#         pagination = make_pagination_range(
#             page_range=list(range(1, 21)),
#             qty_pages=4,
#             current_page=2,
#         )['pagination']
#         self.assertEqual([1, 2, 3, 4], pagination)

#         # Current page = 3 - Qty Page = 4 - Middle Page = 2
#         # HERE RANGE SHOULD CHANGE
#         pagination = make_pagination_range(
#             page_range=list(range(1, 21)),
#             qty_pages=4,
#             current_page=3,
#         )['pagination']
#         self.assertEqual([2, 3, 4, 5], pagination)

#         # Current page = 4 - Qty Page = 4 - Middle Page = 2
#         # HERE RANGE SHOULD CHANGE
#         pagination = make_pagination_range(
#             page_range=list(range(1, 21)),
#             qty_pages=4,
#             current_page=4,
#         )['pagination']
#         self.assertEqual([3, 4, 5, 6], pagination)

#     def test_make_sure_middle_range_is_correct(self):  # noqa: E501
#         # Current page = 10 - Qty Page = 4 - Middle Page = 2
#         # HERE RANGE SHOULD CHANGE
#         pagination = make_pagination_range(
#             page_range=list(range(1, 21)),
#             qty_pages=4,
#             current_page=10,
#         )['pagination']
#         self.assertEqual([9, 10, 11, 12], pagination)

#         # Current page = 14 - Qty Page = 4 - Middle Page = 2
#         # HERE RANGE SHOULD CHANGE
#         pagination = make_pagination_range(
#             page_range=list(range(1, 21)),
#             qty_pages=4,
#             current_page=12,
#         )['pagination']
#         self.assertEqual([11, 12, 13, 14], pagination)

#     def test_make_pagination_range_is_static_when_last_page_is_next(self):
#         # Current page = 18 - Qty Page = 4 - Middle Page = 2
#         # HERE RANGE SHOULD CHANGE
#         pagination = make_pagination_range(
#             page_range=list(range(1, 21)),
#             qty_pages=4,
#             current_page=18,
#         )['pagination']
#         self.assertEqual([17, 18, 19, 20], pagination)

#         # Current page = 19 - Qty Page = 4 - Middle Page = 2
#         # HERE RANGE SHOULD CHANGE
#         pagination = make_pagination_range(
#             page_range=list(range(1, 21)),
#             qty_pages=4,
#             current_page=19,
#         )['pagination']
#         self.assertEqual([17, 18, 19, 20], pagination)

#         # Current page = 20 - Qty Page = 4 - Middle Page = 2
#         # HERE RANGE SHOULD CHANGE
#         pagination = make_pagination_range(
#             page_range=list(range(1, 21)),
#             qty_pages=4,
#             current_page=20,
#         )['pagination']
#         self.assertEqual([17, 18, 19, 20], pagination)

#     def test_make_pagination_returns_the_correct_num_of_recipes(self):
#         recipes = [
#             self.make_recipe(
#                 slug=f'slug-{i}', title=f'title {i}', author_data={'username': f'user{i}'}
#             )
#             for i in range(1, 31)
#         ]

#         response = self.client.get(reverse('recipes:home'))
#         context = response.context['recipes']
#         paginator = context.paginator

#         self.assertEqual(len(recipes), paginator.count)

#     def test_make_pagination_returns_the_correct_num_of_recipes_per_page(self):
#         recipes = [
#             self.make_recipe(
#                 slug=f'slug-{i}', title=f'title {i}', author_data={'username': f'user{i}'}
#             )
#             for i in range(1, 31)
#         ]

#         response = self.client.get(reverse('recipes:home'))
#         context = response.context['recipes']
#         paginator = context.paginator
#         self.assertEqual(9, paginator.per_page)

#     def test_make_pagination_returns_the_correctnum_of_pages(self):
#         recipes = [
#             self.make_recipe(
#                 slug=f'slug-{i}', title=f'title {i}', author_data={'username': f'user{i}'}
#             )
#             for i in range(1, 31)
#         ]

#         response = self.client.get(reverse('recipes:home'))
#         context = response.context['recipes']
#         paginator = context.paginator

#         self.assertEqual(math.ceil(len(recipes)/9),
#                          math.ceil(paginator.count/paginator.per_page))

#     def test_make_pagination_returns_current_page_equal_one_if_not_page_attr_on_url(self):
#         range_recipes = range(1, 18)
#         recipes = [
#             self.make_recipe(
#                 slug=f'slug-{i}', title=f'title {i}', author_data={'username': f'user{i}'}
#             )
#             for i in range_recipes
#         ]

#         search_url = reverse('recipes:home')
#         response = self.client.get(f'{search_url}')
#         context = response.context['recipes']
#         # request = response.request
#         # has_page_attr = 'page=' in request['QUERY_STRING']
#         # self.assertFalse(has_page_attr)
#         current_page = response.context['pagination_range']['current_page']
#         self.assertEqual(current_page, 1)
