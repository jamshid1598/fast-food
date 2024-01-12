from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import BaseModel


class Restaurant(BaseModel):
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'))
    lon = models.FloatField(_('Longitude'), default=0.0)
    lat = models.FloatField(_('Latitude'), default=0.0)
    address = models.CharField(_('Address'), max_length=255, blank=True, null=True)
    contact = models.CharField(_('Contact'), max_length=255, blank=True, null=True)

    class Meta:
        db_table = ' fast_food_restaurant'
        verbose_name = _('Fast-Food Restaurant')
        verbose_name_plural = _('Fast-Food Restaurant')

    def __str__(self):
        return self.name


class FastFood(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='fastfoods',
                                   blank=True, null=True, verbose_name=_('Restaurant'))
    image = models.ImageField(_("Image"), upload_to="fasd-food-images/", blank=True, null=True)
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"))
    price = models.FloatField(_("Price"), default=0.0)

    class Meta:
        db_table = 'fast_food'
        verbose_name = _("Fast Food")
        verbose_name_plural = _("Fast Food")

    def __str__(self):
        return self.name
