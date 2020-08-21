import decimal

from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .cache import clear_top_cache


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
    total = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        verbose_name='Сумма',
        default=decimal.Decimal(0.00)
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
        return f'{self.client} {self.gem} ${decimal.Decimal(self.total)}'

    def __repr__(self):
        return f'<{self.client} {self.gem} ${decimal.Decimal(self.total)}>'

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
        verbose_name = 'Камень'
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


@receiver(post_delete, sender=Deal)
def deal_delete_handler(sender, **kwargs):
    """
    Чистим кеш, если были внесены изменения в БД
    """
    clear_top_cache()


@receiver(post_save, sender=Deal)
def deal_save_handler(sender, **kwargs):
    """
    Чистим кеш, если были внесены изменения в БД
    """
    if kwargs['created']:
        clear_top_cache()


@receiver(post_delete, sender=Customer)
def customer_delete_handler(sender, **kwargs):
    """
    Чистим кеш, если были внесены изменения в БД
    """
    clear_top_cache()


@receiver(post_save, sender=Customer)
def customer_save_handler(sender, **kwargs):
    """
    Чистим кеш, если были внесены изменения в БД
    """
    if kwargs['created']:
        clear_top_cache()


@receiver(post_delete, sender=Gem)
def gem_delete_handler(sender, **kwargs):
    """
    Чистим кеш, если были внесены изменения в БД
    """
    clear_top_cache()


@receiver(post_save, sender=Gem)
def gem_save_handler(sender, **kwargs):
    """
    Чистим кеш, если были внесены изменения в БД
    """
    if kwargs['created']:
        clear_top_cache()
