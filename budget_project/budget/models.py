from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=100
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSACTION_TYPES = [
        (INCOME, 'Доход'),
        (EXPENSE, 'Расход'),
    ]

    amount = models.DecimalField(
        'Сумма',
        max_digits=10,
        decimal_places=2
    )
    transaction_type = models.CharField(
        'Тип операции',
        max_length=10,
        choices=TRANSACTION_TYPES
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория'
    )
    date = models.DateField('Дата')
    description = models.TextField('Описание', blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'

    def __str__(self):
        return f'{self.transaction_type}: {self.amount} ₽'
