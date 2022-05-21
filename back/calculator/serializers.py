from rest_framework import serializers
from .models import Offer


class OfferSerializer(serializers.ModelSerializer):
    payment = serializers.IntegerField(read_only=True, default=0)
    class Meta:
        model = Offer
        fields = '__all__'
