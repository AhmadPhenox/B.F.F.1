from typing import List

from django.contrib.auth import get_user_model
from django.db.models import Q
from ninja import Router
from pydantic import UUID4

from account.authorization import GlobalAuth
from commerce.models import Product, Label, Category, Item
from commerce.schemas import ProductOut, LabelOut, CategoryOut, ProductCreate, AddToCartPayload
from django.shortcuts import get_object_or_404

from config.utils.schemas import MessageOut

User = get_user_model()

commerce_controller = Router(tags=['products'])
order_controller = Router(tags=['order'])



@commerce_controller.get('products', response={
    200: List[ProductOut],
})
def list_products(request, q: str = None, price_lte: int = None, price_gte: int = None):
    products = Product.objects.all()

    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )

    if price_lte:
        products = products.filter(discounted_price__lte=price_lte)

    if price_gte:
        products = products.filter(discounted_price__gte=price_gte)

    return products


@commerce_controller.get('products/{id}', response={
    200: ProductOut
})
def retrieve_product(request, id):
    return get_object_or_404(Product, id=id)


@commerce_controller.get('Label', response={
    200: List[LabelOut],
})
def list_label(request):
    label = Label.objects.all()
    # label = Label.filter(name='tshirt')
    return label


@commerce_controller.get('Label/{id}', response={
    200: LabelOut
})
def retrieve_Label(request, id):
    return get_object_or_404(Label, id=id)



@commerce_controller.get('Categorys', response={
    200: List[CategoryOut],
})
def list_Categorys(request):
    categorys = Category.objects.all()
    # Categorys = Categorys.filter(name='tshirt')
    return categorys


@commerce_controller.get('Categorys/{id}', response={
    200: CategoryOut
})
def retrieve_Category(request, id):
    return get_object_or_404(Category, id=id)


@commerce_controller.post('products', response={
    201: ProductOut,
    400: MessageOut
})
def create_product(request, payload: ProductCreate):
    try:
        product = Product.objects.create(**payload.dict(), is_active=True)
    except:
        return 400, {'detail': 'something wrong happened!'}

    return 201, product



@order_controller.post('add-to-cart', auth=GlobalAuth(), response=MessageOut)
def add_to_cart(request, payload: AddToCartPayload):
    payload_validated = payload.copy()
    user = User.objects.get(id=request.auth['pk'])
    if payload.qty < 1:
        payload_validated.qty = 1

    try:
        item = Item.objects.get(product_id=payload.product_id)
    except Item.DoesNotExist:
        Item.objects.create(product_id=payload.product_id, user=user, item_qty=payload_validated.qty,
                            ordered=False)
        return 200, {'detail': 'item added to cart successfully!'}

    item.item_qty += payload_validated.qty
    item.save()
    return 200, {'detail': 'item qty updated successfully!'}


@order_controller.post('increase-item/{item_id}', auth=GlobalAuth(), response=MessageOut)
def increase_item_qty(request, item_id: UUID4):
    user = User.objects.get(id=request.auth['pk'])
    item = get_object_or_404(Item, id=item_id, user=user)
    item.item_qty += 1
    item.save()

    return 200, {'detail': 'Item qty increased successfully!'}


@order_controller.post('decrease-item/{item_id}', auth=GlobalAuth(), response=MessageOut)
def decrease_item_qty(request, item_id: UUID4):
    user = User.objects.get(id=request.auth['pk'])
    item = get_object_or_404(Item, id=item_id, user=user)
    item.item_qty -= 1
    print(item.item_qty)
    item.save()
    if item.item_qty == 0:
        item.delete()
    return 200, {'detail': 'Item qty decreased successfully!'}


@order_controller.delete('delete_item/{item_id}', auth=GlobalAuth(), response=MessageOut)
def delete_item(request, item_id: UUID4):
    user = User.objects.get(id=request.auth['pk'])
    item = get_object_or_404(Item, id=item_id, user=user)
    item.delete()
    return 200, {'detail': 'Item deleted !'}




