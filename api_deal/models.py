from django.db import models


class Deal(models.Model):
    """
    Сделка - покупка клиетом камней
    """
    client = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        verbose_name='Логин клиента',
        related_name='deals'
    )
    gem = models.ForeignKey(
        'Gem',
        on_delete=models.CASCADE,
        verbose_name='Камни',
        related_name='deals'
    )
    total = models.PositiveIntegerField(
        verbose_name='Сумма',
        default=0
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество камней',
        default=1
    )
    date = models.DateField(
        verbose_name='Дата сделки',
    )

    class Meta:
        verbose_name = 'Сделка клиента'
        verbose_name_plural = 'Сделки клиентов'

    def __str__(self):
        return f'{self.client} {self.gem} ${self.total}'

    def __repr__(self):
        return f'<{self.client} {self.gem} ${self.total}>'

    @classmethod
    def clear_db(cls):
        cls.objects.all().delete()


class Customer(models.Model):
    """
    Клиент
    """
    name = models.CharField(
        max_length=255,
        verbose_name='Логин клиента',
        unique=True,
        null=False
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'<{self.name}>'

    @classmethod
    def clear_db(cls):
        cls.objects.all().delete()


class Gem(models.Model):
    """
    Камень
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

    @classmethod
    def clear_db(cls):
        cls.objects.all().delete()


def clear_all_table_models():
    """
    Отчистка БД
    """
    Gem.clear_db()
    Deal.clear_db()
    Customer.clear_db()
