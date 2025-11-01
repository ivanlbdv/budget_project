import csv
from collections import defaultdict
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import formats

from .forms import CategoryForm, LoginForm, TransactionForm
from .models import Category, Transaction


@login_required
def dashboard(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category')

    transactions = Transaction.objects.filter(user=request.user)

    if start_date and end_date:
        transactions = transactions.filter(
            date__gte=start_date,
            date__lte=end_date
        )

    if search_query:
        transactions = transactions.filter(description__icontains=search_query)

    if category_id:
        transactions = transactions.filter(category_id=category_id)

    # Расчёт сумм через БД
    total_income = transactions.filter(transaction_type='income').aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_expense = transactions.filter(transaction_type='expense').aggregate(
        total=Sum('amount')
    )['total'] or 0

    # График расходов и доходов по месяцам
    monthly_data = defaultdict(lambda: {'income': 0, 'expense': 0})

    for trans in transactions:
        month_key = trans.date.strftime('%Y-%m')
        if trans.transaction_type == 'income':
            monthly_data[month_key]['income'] += trans.amount
        else:
            monthly_data[month_key]['expense'] += trans.amount

    labels_expense = sorted(monthly_data.keys())
    data_expense = [float(monthly_data[month]['expense']) for month in labels_expense]
    labels_income = labels_expense
    data_income = [float(monthly_data[month]['income']) for month in labels_income]

    labels_expense_formatted = [
        formats.date_format(
            datetime.strptime(month, '%Y-%m'),
            'M Y'
        )
        for month in labels_expense
    ]
    labels_income_formatted = labels_expense_formatted

    categories = Category.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'start_date': start_date,
        'end_date': end_date,
        'search_query': search_query,
        'selected_category': category_id,
        'categories': categories,
        'labels_expense': labels_expense_formatted,
        'data_expense': data_expense,
        'labels_income': labels_income_formatted,
        'data_income': data_income
    })


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()

            messages.success(request, 'Категория добавлена!')
            return redirect('dashboard')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Операция добавлена!')
            return redirect('dashboard')
    else:
        form = TransactionForm()
        # Заполняем список категорий для текущего пользователя
        form.fields['category'].queryset = Category.objects.filter(
            user=request.user
        )
    return render(request, 'transaction_form.html', {'form': form})


@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk, user=request.user)
    form = TransactionForm(instance=transaction)
    print(f"Transaction ID: {transaction.id}")  # должен вывести ID из URL
    print(f"Form data: {form.initial}")  # покажет начальные данные формы
    return render(request, 'edit_transaction.html', {
        'form': form,
        'transaction': transaction
    })


@login_required
def update_transaction(request, pk):
    if request.method == 'POST':
        transaction = get_object_or_404(Transaction, id=pk, user=request.user)
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Операция обновлена!')
            return redirect('dashboard')
        else:
            return render(request, 'edit_transaction.html', {
                'form': form,
                'transaction': transaction
            })
    else:
        return redirect('edit_transaction', pk=pk)


@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk, user=request.user)

    transaction.delete()

    messages.success(request, 'Операция удалена!')

    return redirect('dashboard')


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Дата', 'Тип', 'Сумма (₽)', 'Категория', 'Описание'])

    transactions = Transaction.objects.filter(user=request.user)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_query = request.GET.get('q')
    category_id = request.GET.get('category')

    if start_date and end_date:
        transactions = transactions.filter(
            date__gte=start_date,
            date__lte=end_date
        )
    if search_query:
        transactions = transactions.filter(description__icontains=search_query)
    if category_id:
        transactions = transactions.filter(category_id=category_id)

    for transaction in transactions:
        writer.writerow([
            transaction.date,
            transaction.get_transaction_type_display(),
            transaction.amount,
            transaction.category.name if transaction.category else '',
            transaction.description
        ])

    return response


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Неверный логин или пароль.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('login')
