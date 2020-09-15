from django.db import models


class Article(models.Model):
    """Habr-article model."""
    title = models.CharField(max_length=64, help_text='Article title')
    content = models.TextField()
    url = models.URLField()

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return 'Article {}'.format({self.title})