from django.contrib import admin
from .models import CurrentBalance, TrackingHistory, RequestLogs

# Admin Customization
admin.site.site_header = 'Expense Tracker'
admin.site.site_title = 'Expense Tracker'

class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = ["amount", "current_balance", "expense_type", "description", "created_at", "display_age"]
    actions = ["mark_as_credit", "mark_as_debit"]
    search_fields = ['expense_type', 'description']
    list_filter = ['expense_type']
    ordering = ['-created_at']

    def display_age(self, obj):
        return "Positive" if obj.amount > 0 else "Negative"

    @admin.action(description="Mark selected Expenses as Credit")
    def mark_as_credit(self, request, queryset):
        for obj in queryset:
            if obj.amount < 0:
                obj.amount = abs(obj.amount)
                obj.save()
        queryset.update(expense_type="CREDIT")

    @admin.action(description="Make it in Debit")
    def mark_as_debit(self, request, queryset):
        for obj in queryset:
            if obj.amount > 0:
                obj.amount = -abs(obj.amount)
                obj.save()
        queryset.update(expense_type="DEBIT")

admin.site.register(CurrentBalance)
admin.site.register(TrackingHistory, TrackingHistoryAdmin)
admin.site.register(RequestLogs)
