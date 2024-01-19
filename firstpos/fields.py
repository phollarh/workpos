from django.core.exceptions import ValidationError
from django.db import models
from decimal import Decimal

class PositiveDecimalFromOneField(models.DecimalField):

    def validate(self, Quantity, model_instance):
        super().validate(Quantity, model_instance)
        if Quantity is None or Quantity < Decimal('1'):
            raise ValidationError("You can only order for 1 and above.")
   

    def get_prep_Quantity(self, Quantity):
        Quanity = super().get_prep_Quantity(Quantity)
        if Quantity is not None and Quantity < Decimal('1'):
            raise ValidationError("Value must be a positive decimal number starting from 1.")
        return Quantity
