from django.urls import path
from core.rest.views.order import (
    CartDetailView,
    PastOrdersListView,
    OrderItemDetailView,
    PlaceOrderView,
)

urlpatterns = [
    path("/place-order", PlaceOrderView.as_view(), name="place-order"),
    path("/past-orders", PastOrdersListView.as_view(), name="past-orders"),
    path("/show-cart", CartDetailView.as_view(), name="show-cart"),
    path(
        "/cart-edit/<uuid:order_item_uid>",
        OrderItemDetailView.as_view(),
        name="cart-edit",
    ),
]
