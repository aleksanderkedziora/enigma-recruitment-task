from django.db import models
from django.utils.translation import gettext_lazy as _

from decimal import Decimal


class VatRate(models.IntegerChoices):
    STANDARD = 23, _('23% - Standard rate')
    REDUCED_8 = 8, _('8% - Reduced rate')
    REDUCED_5 = 5, _('5% - Reduced rate')
    ZERO = 0, _('0% - Zero rate')


class ProductCategory(models.Model):
    name = models.CharField(max_length=120, verbose_name=_('name'))


class Product(models.Model):
    name = models.CharField(
        max_length=120,
        verbose_name=_('name')
    )
    description = models.CharField(
        max_length=250,
        verbose_name=_('description')
    )
    price_netto = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name=_('netto')
    )
    vat_rate = models.IntegerField(
        choices=VatRate.choices,
        default=VatRate.STANDARD,
        verbose_name=_('vat rate')
    )
    image = models.ImageField(
        upload_to="products/%Y/%m/%d/",
        blank=True,
        verbose_name=_('image')
    )
    thumbnail = models.ImageField(
        upload_to='products/thumb/%Y/%m/%d/',
        blank=True,
        verbose_name=_('thumbnail')
    )

    category = models.ForeignKey(
        'products.ProductCategory',
        on_delete=models.SET_NULL,
        related_name='products',
        null=True
    )

    @property
    def price_brutto(self):
        return self.price_netto * Decimal(1 + (self.vat_rate / 100))
