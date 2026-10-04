from django.contrib import admin
from commerce.models import Product, Order, OrderItem, Payment
def register(model):
    return admin.site.register(model)

# Register your models here.
register(Product)
register(Order)
register(OrderItem)
register(Payment)

"""

class OrderItemInline(admin.TabularInline):
    
    #Allows adding/editing OrderItems directly inside the Order page.
    #Filters the product dropdown to ONLY show available products.
    
    model = OrderItem
    extra = 1
    fields = ("product", "price", "quantity")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            # Show products that have stock > 0 and are marked available
            kwargs["queryset"] = Product.objects.filter(is_available=True, stock__gt=0)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "order_status", "amount", "tx_ref", "created_at")
    list_filter = ("order_status", "created_at")
    search_fields = ("id", "user__email", "tx_ref")
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "price", "quantity")
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            # Restrict product choices when creating an OrderItem standalone
            kwargs["queryset"] = Product.objects.filter(is_available=True, stock__gt=0)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
"""
