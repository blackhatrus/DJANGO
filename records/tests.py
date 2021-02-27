"""

This module is for testing
Author:
Date: 11/02/2021


"""

from django.test import TestCase

# Create your tests here.
from .models import Record, Category, Comment


class GodnotaTests(TestCase):

    def setUp(self) -> None:
        self.category = Category.objects.create(title="тестовая категория",
                                                description="очень крутая категория")
        self.record = Record.objects.create(
            title="Cool shop",
            category=self.category,
            record_status='published',
            body="Очень крутой лабаз в даркнете",
            url="http://duytqwtduuq.onion",
            online_status="online",
            stars=3,
            added_to_cat='год назад',
            meta_desc='чумовой магаз',
        )
        self.comment = Comment.objects.create(
            record=self.record,
            body="Крутой коммент",
            author="Незнакомец",
        )

    def test_self_record_slug(self):
        self.assertEquals(self.record.slug, 'cool-shop')


    def test_self_category(self):
        self.assertEquals(self.category.title, 'тестовая категория')    