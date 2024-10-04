from django.shortcuts import render, redirect
from tracker.models import CurrentBalance, TrackingHistory


def index(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        # Ensure the amount is not None and is not an empty string
        if amount is None or amount.strip() == "":
            return render(request, 'index.html', {'error': 'Amount is required'})

        # Convert the amount to float if it's valid
        amount = float(amount)

        current_balance, created = CurrentBalance.objects.get_or_create(id=1)
        expense_type = "CREDIT"

        if amount < 0:
            expense_type = "DEBIT"

        tracking_history = TrackingHistory.objects.create(
            amount=amount, expense_type=expense_type,
            current_balance=current_balance, description=description
        )

        current_balance.current_balance += amount
        current_balance.save()

        print(description, amount, expense_type, tracking_history)
        return redirect('/')

    return render(request, 'index.html')