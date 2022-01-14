from django.contrib import admin

from commerce.models import (
    Product,
    Category,
    Label, Item, ProductImage, Order,

)


admin.site.register(Product)
admin.site.register(Label)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Order)



class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'item_qty')


admin.site.register(Item, ItemAdmin)