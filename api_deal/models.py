from django.db import models


class Client(models.Model):
    """
    """
    username = models.CharField(
        max_length=255,
        verbose_name='Логин клиента',
        unique=True,
        null=False
    )
    spent_money = models.PositiveIntegerField(
        verbose_name='Сумма',
        default=0
    )
    gems = models.ManyToManyField(
        'Gem',
        verbose_name='Камни',
        related_name='owners'
    )

    class Meta:
        verbose_name = 'Результат сделок клиента'
        verbose_name_plural = 'результаты сделок клиентов'

    def __str__(self):
        return f'{self.username}'

    def __repr__(self):
        return f'<{self.username}>'


class Gem(models.Model):
    """
    """
    title = models.CharField(
        max_length=255,
        verbose_name='Название',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Кмень'
        verbose_name_plural = 'Камни'

    def __str__(self):
        return f'{self.title}'

    def __repr__(self):
        return f'<{self.title}>'
