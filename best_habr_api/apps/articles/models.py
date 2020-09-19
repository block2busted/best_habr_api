from django.db import models


class Article(models.Model):
    """Habr-article model.
    """
    title = models.CharField(max_length=64, help_text='Title')
    content = models.TextField(help_text='Content')
    url = models.URLField(help_text='Url')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ('-pk', )

    def __str__(self):
        return 'Article {}'.format(self.title)