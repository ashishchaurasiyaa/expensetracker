from django.shortcuts import render, redirect
from django.contrib import messages
from tracker.models import CurrentBalance, TrackingHistory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username or password.")
            return redirect('/login/')

        login(request, user)
        return redirect('/')

    return render(request, 'login.html')


# Registration view
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists.")
            return redirect('/register/')

        new_user = User(username=username, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()

        messages.success(request, "User created successfully.")
        return redirect('/login/')  # Redirect to login after successful registration

    return render(request, 'register.html')


# Index view for adding transactions and displaying the dashboard
@login_required(login_url='/login/')
def index(request):
    if request.method == "POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        if not amount:
            messages.error(request, "Amount cannot be empty.")
            return redirect('/')

        try:
            amount = float(amount)
        except ValueError:
            messages.error(request, "Invalid amount entered.")
            return redirect('/')

        if amount == 0:
            messages.error(request, "Amount cannot be zero.")
            return redirect('/')

        current_balance, _ = CurrentBalance.objects.get_or_create(id=1)
        expense_type = "CREDIT" if amount >= 0 else "DEBIT"

        # Check if a similar transaction exists to avoid duplicates
        if TrackingHistory.objects.filter(amount=amount, description=description, expense_type=expense_type).exists():
            messages.error(request, "Transaction already exists.")
            return redirect('/')

        # Create a transaction and update the current balance
        TrackingHistory.objects.create(
            amount=amount,
            expense_type=expense_type,
            current_balance=current_balance,
            description=description
        )

        current_balance.current_balance += amount
        current_balance.save()

        messages.success(request, "Transaction added successfully.")
        return redirect('/')

    # Fetching current balance, income, and expenses
    current_balance, _ = CurrentBalance.objects.get_or_create(id=1)
    income = sum(th.amount for th in TrackingHistory.objects.filter(expense_type="CREDIT"))
    expense = sum(th.amount for th in TrackingHistory.objects.filter(expense_type="DEBIT"))

    context = {
        'income': income,
        'expense': expense,
        'transactions': TrackingHistory.objects.all(),
        'current_balance': current_balance
    }
    return render(request, 'index.html', context)


# Delete transaction view
@login_required(login_url='/login/')
def delete_transaction(request, id):
    try:
        tracking_history = TrackingHistory.objects.get(id=id)
        current_balance, _ = CurrentBalance.objects.get_or_create(id=1)

        current_balance.current_balance -= tracking_history.amount
        current_balance.save()

        tracking_history.delete()
        messages.success(request, "Transaction deleted successfully.")
    except TrackingHistory.DoesNotExist:
        messages.error(request, "Transaction not found.")

    return redirect('/')


# Logout view
def logout_view(request):
    logout(request)
    return redirect('/login/')
