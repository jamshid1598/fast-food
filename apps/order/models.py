from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import BaseModel


class OrderStatus(models.TextChoices):
    WAITING = "waiting", _("Waiting")
    CONFIRMED = "confiemd", _("Confirmed")
    COMPLETED = "completed", _("Completed")
    CANCELLED = "cancelled", _("Cancelled")


class Order(BaseModel):
    restaurant = models.ForeignKey('fastfood.Restaurant', on_delete=models.SET_NULL, related_name='orders',
                             blank=True, null=True, verbose_name='Restaurant')
    user = models.ForeignKey('users.Users', on_delete=models.SET_NULL, related_name='orders',
                             blank=True, null=True, verbose_name='User')
    total_price = models.FloatField(_('Total price'), default=0.0)
    status = models.CharField(_('Status'), max_length=100, choices=OrderStatus.choices, default=OrderStatus.WAITING)
    lon = models.FloatField(_('Longitute'), default=0.0)
    lat = models.FloatField(_('Latitude'), default=0.0)
    address = models.CharField(_('Address'), max_length=255, blank=True, null=True)
    delivery_time = models.CharField(_('Delivery time'), max_length=50)

    class Meta:
        db_table = 'order_order'
        ordering = ['-created_at']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        full_name = self.user.full_name if self.user else ""
        return full_name


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems', verbose_name=_('Order'))
    fastfood = models.ForeignKey('fastfood.FastFood', on_delete=models.SET_NULL, null=True,
                                 related_name='orderitems', verbose_name=_('Fast-food'))
    name = models.CharField(_('Name'), max_length=255)
    count = models.IntegerField(_('Count'), default=0)
    price = models.FloatField(_('Price'), default=0.0)

    class Meta:
        db_table = 'order_orderitem'
        ordering = ['-created_at']
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return "%s - %s" % (self.name, self.count)
