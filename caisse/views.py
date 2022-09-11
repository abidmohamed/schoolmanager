from django.db.models import Sum
from django.shortcuts import render
import os
from uuid import uuid4
import decimal
from datetime import date, datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
# Category
from caisse.filters import TransactionCategoryFilter, TransactionFilter
from caisse.forms import CategoryTransactionForm, TransactionForm
from caisse.models import TransactionCategory, Transaction
from payments.models import ParentPayment, StudentPayment, Payroll


@login_required
def cash_register(request):
    context = {}
    total_value = 0
    # get all client payments (cash)
    students_payments = StudentPayment.objects.all().aggregate(Sum('amount'))
    students_payments = students_payments['amount__sum']
    # get all supplier payments (cash)
    parent_payments = ParentPayment.objects.all().aggregate(Sum('amount'))
    parent_payments = parent_payments['amount__sum']

    payrolls_sum = Payroll.objects.filter(paid=True).aggregate(Sum('amount'))
    if payrolls_sum['amount__sum']:
        payrolls_sum = round(payrolls_sum['amount__sum'], 2)
    else:
        payrolls_sum = 0

    # get all transactions
    in_transaction = Transaction.objects.filter(Transaction_type='Income').aggregate(Sum('amount'))
    out_transaction = Transaction.objects.filter(Transaction_type='Expense').aggregate(Sum('amount'))
    # print(in_transaction['amount__sum'])
    total_transaction = 0
    if in_transaction['amount__sum']:
        total_transaction += in_transaction['amount__sum']
    if out_transaction['amount__sum']:
        total_transaction -= out_transaction['amount__sum']

    if students_payments is None:
        students_payments = 0
    if parent_payments is None:
        parent_payments = 0
    if total_transaction is None:
        total_transaction = 0

    total_value = (students_payments + parent_payments + total_transaction) - payrolls_sum

    context['students_payments'] = students_payments
    context['parent_payments'] = parent_payments
    context['total_transaction'] = total_transaction
    context['payrolls_sum'] = payrolls_sum
    context['total_value'] = total_value

    return render(request, "caisse/transaction_list.html", context)


@login_required
def transaction_category_list(request):
    context = {}
    categories_list = TransactionCategory.objects.all().order_by('name')

    myFilter = TransactionCategoryFilter(request.GET, queryset=categories_list)

    # paginate after filtering
    categories_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(categories_list, 5)
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter

    context['categories'] = categories
    # company = Settings.objects.all().filter()[:1].get()
    # context['company'] = company
    if request.method == 'GET':
        form = CategoryTransactionForm()
        context['form'] = form
        return render(request, 'category/list.html', context)

    if request.method == 'POST':
        form = CategoryTransactionForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "New Category Added")

            return redirect('caisse:transaction_category_list')
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('caisse:transaction_category_list')

    return render(request, 'category/list.html', context)


@login_required
def transaction_category_details(request, pk):
    context = {}
    try:
        category = TransactionCategory.objects.get(id=pk)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('caisse:transaction_category_list')

    transactions_list = category.items.all()

    myFilter = TransactionFilter(request.GET, queryset=transactions_list)

    # paginate after filtering
    transactions_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of transactions in the page
    paginator = Paginator(transactions_list, 5)
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter

    context['transactions'] = transactions
    context['category'] = category

    # company = Settings.objects.all().filter()[:1].get()
    # context['company'] = company
    if request.method == 'GET':
        form = TransactionForm()
        context['form'] = form
        return render(request, 'transaction/list.html', context)

    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "New Value Added")

            return redirect('caisse:transaction_list')
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('caisse:transaction_list')

    return render(request, 'category/details.html', context)


@login_required
def transaction_list(request):
    context = {}
    transactions_list = Transaction.objects.all().order_by('trans_date')

    myFilter = TransactionFilter(request.GET, queryset=transactions_list)

    # paginate after filtering
    transactions_list = myFilter.qs
    # Page
    page = request.GET.get('page', 1)
    # Number of customers in the page
    paginator = Paginator(transactions_list, 5)
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    context['myFilter'] = myFilter

    context['transactions'] = transactions

    total = 0
    incomes = 0
    expenses = 0
    for transaction in transactions_list:
        if transaction.Transaction_type == "Income":
            total += transaction.amount
            incomes += transaction.amount
        else:
            total -= transaction.amount
            expenses += transaction.amount

    context['incomes'] = incomes
    context['total'] = total
    context['expenses'] = expenses

    # company = Settings.objects.all().filter()[:1].get()
    # context['company'] = company
    if request.method == 'GET':
        form = TransactionForm()
        context['form'] = form
        return render(request, 'transaction/list.html', context)

    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "New Value Added")

            return redirect('caisse:transaction_list')
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('caisse:transaction_list')

    return render(request, 'transaction/list.html', context)


def transaction_details(request, slug):
    context = {}
    try:
        transaction = Transaction.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('caisse:transaction_list')

    context['transaction'] = transaction
    return render(request, 'transaction/details.html', context)


def transaction_update(request, slug):
    context = {}
    try:
        transaction = Transaction.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('caisse:transaction_list')

    form = TransactionForm(instance=transaction)
    context['form'] = form
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction_form = form.save(commit=False)
            transaction_form.save()

            return redirect('caisse:transaction_details', slug)

    return render(request, 'transaction/update.html', context)


def transaction_delete(request, slug):
    try:
        transaction = Transaction.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('caisse:transaction_list')

    transaction.delete()

    return redirect('caisse:transaction_list')
