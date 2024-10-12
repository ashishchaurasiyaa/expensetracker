from django.db import models


class CurrentBalance(models.Model):
    current_balance = models.FloatField(default=0)

    def __str__(self) -> str:
        return str(self.current_balance)


class TrackingHistory(models.Model):
    current_balance = models.ForeignKey(CurrentBalance, on_delete=models.CASCADE)
    amount = models.FloatField(editable=False)
    expense_type = models.CharField(max_length=6, choices=(('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')))
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.amount} {self.expense_type} for {self.description} expense"


class RequestLogs(models.Model):
    request_info = models.TextField()
    request_type = models.CharField(max_length=100)
    request_method = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.request_method} - {self.request_type} at {self.created_at}'
