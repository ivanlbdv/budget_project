from django.contrib import admin

from .models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'transaction_type', 'category', 'date', 'user')
    list_filter = ('transaction_type', 'category', 'date', 'user')
    search_fields = ('description',)
