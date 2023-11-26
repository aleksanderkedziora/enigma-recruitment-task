from django.db import models
from django.utils.translation import gettext_lazy as _

from decimal import Decimal

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

import sys

from django.conf import settings


class VatRate(models.IntegerChoices):
    STANDARD = 23, _('23% - Standard rate')
    REDUCED_8 = 8, _('8% - Reduced rate')
    REDUCED_5 = 5, _('5% - Reduced rate')
    ZERO = 0, _('0% - Zero rate')


class ProductCategory(models.Model):
    name = models.CharField(max_length=120, verbose_name=_('name'))

    def __str__(self):
        return self.name


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
        return round(self.price_netto * (1 + Decimal(str(self.vat_rate / 100))), 2)

    @property
    def short_description(self) -> str:
        return f"{self.name} - {self.price_brutto} PLN"

    def _set_thumbnail(self) -> None:
        img = Image.open(self.image)
        img_name = self.image.name.split('.')[0]

        output_thumb = BytesIO()
        output_size = (img.width, img.height)

        if img.width > settings.MAX_THUMBNAIL_WIDTH:
            height_width_ratio = img.size[1] / img.size[0]
            thumbnail_height = int(settings.MAX_THUMBNAIL_WIDTH * height_width_ratio)
            output_size = (settings.MAX_THUMBNAIL_WIDTH, thumbnail_height)

        img.thumbnail(output_size)
        img.save(output_thumb, format='JPEG', quality=90)

        self.thumbnail = InMemoryUploadedFile(
            output_thumb,
            'ImageField',
            f"{img_name}_thumb.jpg",
            'image/jpeg',
            sys.getsizeof(output_thumb),
            None
        )

    def save(self, *args, **kwargs):
        self._set_thumbnail()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.short_description

    def __repr__(self):
        return self.short_description
