from django.db import models

class Section(models.Model):
    title = models.CharField(max_length=100)
    article = models.ForeignKey(to='blog.Article', related_name='parts', on_delete=models.CASCADE)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title