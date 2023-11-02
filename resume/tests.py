from django.test import TestCase
import unittest
from blog.models import ArticleCategory, Author, Article, ArticlePart, ContentBlock, ParagraphBlock, TableBlock, PictureBlock

class ModelsTestCase(TestCase):

    def test_article_category_model(self):
        category = ArticleCategory.objects.create(
            name='Test Category',
            description='Test description'
        )
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.slug, 'test-category')

    def test_author_model(self):
        author = Author.objects.create(
            full_name='Test Author',
            bio='Test bio'
        )
        self.assertEqual(author.full_name, 'Test Author')
        self.assertEqual(str(author), 'Test Author')

    def test_article_model(self):
        category = ArticleCategory.objects.create(name='Cat1')
        author = Author.objects.create(full_name='Author1')
        article = Article.objects.create(
            title='Test Article',
            category=category,
            author=author
        )
        self.assertEqual(article.title, 'Test Article')
        self.assertEqual(str(article), 'Test Article')

    # TODO: Add tests for other models
