from django.db import models
from django.utils.translation import gettext_lazy
from django.core.exceptions import ValidationError
from datetime import datetime

# Create your models here.


class Device(models.Model):

    class Meta:
        db_table = 'devices'
        verbose_name = 'Доступное оборудование'
        verbose_name_plural = 'Доступное оборудование'

    manufacturer = models.TextField(verbose_name="Производитель")
    model = models.TextField(verbose_name="Модель")

    def __str__(self):
        return f"{self.manufacturer} {self.model}"


class Customer(models.Model):

    class Meta:
        db_table = "customers"
        verbose_name = "Описание контрагента"
        verbose_name_plural = "Описание контрагентов"

    customer_name = models.TextField(verbose_name="Наименование организации")
    customer_address = models.TextField(verbose_name="Адрес")
    customer_city = models.TextField(verbose_name="Города")

    def __str__(self):
        return f"{self.customer_name} по адресу: {self.customer_address}"


class DeviceInField(models.Model):

    class Meta:
        db_table = "devices_in_fields"
        verbose_name = "Оборудование в полях"
        verbose_name_plural = "Оборудование в полях"

    serial_number = models.TextField(verbose_name="Серийный номер")
    customer = models.ForeignKey(to=Customer, verbose_name="Идентификатор пользователя", on_delete=models.RESTRICT)
    analyzer = models.ForeignKey(to=Device, verbose_name="Идентификатор оборудование", on_delete=models.RESTRICT)
    owner_status = models.TextField(verbose_name="Статус принадлежности")

    def __str__(self):
        return f"{self.analyzer} c/н {self.serial_number} в {self.customer}"


class Order(models.Model):
    statuses = (("open", "открыта"),
                ("closed", "закрыта"),
                ("in progress", "в работе"),
                ("need info", "нужна информация"),
                )

    class Meta:
        db_table = "orders"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    device = models.ForeignKey(to=DeviceInField, verbose_name="Оборудование", on_delete=models.RESTRICT)
    order_description = models.TextField(verbose_name="Описание")
    created_dt = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    last_update_dt = models.DateTimeField(verbose_name='Последнее изминение', blank=True, null=True)
    order_status = models.TextField(verbose_name="Статус заявки", choices=statuses)

    def save(self, *args, **kwargs):
        self.last_update_dt = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заявка №{self.id} для {self.device}"

