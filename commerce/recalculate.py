from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce
from commerce.models import Order 

def recalculate_null_orders():
    # Find orders where amount is null or zero
    orders_to_update = Order.objects.filter(amount__isnull=True) | Order.objects.filter(amount=0)
    
    updated_count = 0
    for order in orders_to_update.prefetch_related('items'):
        # Calculate sum of (price * quantity) for related OrderItems
        calculated_total = order.items.aggregate(
            total=Coalesce(
                Sum(F('price') * F('quantity'), output_field=DecimalField()), 
                0.00
            )
        )['total']
        
        order.amount = calculated_total
        order.save(update_fields=['amount'])
        updated_count += 1
        
    print(f"Successfully updated {updated_count} orders.")

# Execute the script
# recalculate_null_orders()