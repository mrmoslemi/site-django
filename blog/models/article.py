from django.db import models


class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, db_index=True)
    categories = models.ManyToManyField(to='blog.Category')
    meta = models.ManyToManyField(to='blog.Meta')
    author = models.ForeignKey(to='blog.Author', on_delete=models.CASCADE)
    meta_description = models.CharField(max_length=255, blank=True)
    keywords = models.ManyToManyField(to='blog.Keyword',blank=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title