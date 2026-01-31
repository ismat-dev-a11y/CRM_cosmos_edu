from django.contrib import admin
from .models import Payment
from unfold.admin import ModelAdmin

@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = (
        'user',
        'course',
        'amount_display',  # O'zgartirildi
        'provider_display',  # O'zgartirildi
        'status_display',  # O'zgartirildi
        'payment_date',
    )

    list_filter = ('status', 'provider', 'course')
    search_fields = ('user__username', 'receipt_number')

    readonly_fields = (
        'receipt_number',
        'payment_date',
    )

    fieldsets = (
        ('Asosiy', {
            'fields': ('user', 'course', 'amount', 'provider', 'status')
        }),
        ('Izoh', {
            'fields': ('note',)
        }),
    )

    @admin.display(description='Summa')
    def amount_display(self, obj):
        # Decimal ni avval float ga o'tkazib, keyin formatlash
        try:
            amount = float(obj.amount) if obj.amount else 0
            return f"{amount:,.0f} so'm"
        except:
            return "0 so'm"

    @admin.display(description='Provider')
    def provider_display(self, obj):
        # Faqat matn qaytarish
        return obj.get_provider_display()

    @admin.display(description='Holat')
    def status_display(self, obj):
        # Faqat matn qaytarish
        return obj.get_status_display()