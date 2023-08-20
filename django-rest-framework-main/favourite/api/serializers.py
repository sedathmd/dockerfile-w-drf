from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from favourite.models import Favourite


class FavouriteListCreateSerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'

    #konu kullanicinin favorilerindeyse bir daha ekletmez
    def validate(self, attrs):
        queryset = Favourite.objects.filter(post=attrs["post"], user=attrs["user"])
        if queryset.exists():
            raise serializers.ValidationError("Already in favourites")
        return attrs

class FavouriteSerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['content']