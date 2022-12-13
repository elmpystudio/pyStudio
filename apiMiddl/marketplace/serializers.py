from rest_framework import serializers
from .models import *
from accounts.models import *
from django_filters.rest_framework import DjangoFilterBackend

#class TagSerializer(serializers.Serializer):
#    name = serializers.CharField(max_length=200)

class PurchaseSerializer(serializers.Serializer):
    offering = serializers.PrimaryKeyRelatedField(queryset=Offering.objects.all(), write_only=True)
    price = serializers.DecimalField(decimal_places=2,max_digits=10, write_only=True)
    period = serializers.IntegerField(write_only=True)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]

class SubscriptionOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionOption
        fields = ["price", "period"]

class WriteOfferingSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100, write_only=True)
    description = serializers.CharField(write_only=True)
    briefDescription = serializers.CharField(write_only=True)
    tags = TagSerializer(many=True, write_only=True)
    price = serializers.FloatField(write_only=True)
    #subscriptionOptionsData = SubscriptionOptionSerializer(many=True, write_only=True)

    # item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), write_only=True, required=False, allow_null=True)

    def create(self, validated_data):
        user = self.context['request'].user
        tags = []

        #for tag in validated_data['tags']:
        for tag in validated_data.pop('tags'):
            try:
                t = Tag.objects.get(name=tag['name'])
            except Tag.DoesNotExist:
                t = Tag.objects.create(**tag)

            tags.append(t)

        """
        subs_data = validated_data.pop('subscriptionOptionsData')
        subs = []
        for sub_data in subs_data:
            subs.append(SubscriptionOption.objects.create(**sub_data))
        """

        print(validated_data)
        offer = Offering.objects.create(owner=user, **validated_data)
        #offer.subscriptionOptions.set(subs)
        offer.tags.set(tags)

        offer.save()

        return {"result": True, "id": offer.id}
            

class ReadOfferingSerializer(serializers.ModelSerializer):
    subscriptionOptions = SubscriptionOptionSerializer(many=True,read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    type = serializers.ReadOnlyField()

    class Meta:
        model = Offering
        fields = "__all__"

class DashboardItemsSerializer(serializers.ModelSerializer):

    popular = SubscriptionOptionSerializer(many=True,read_only=True)
    recent = SubscriptionOptionSerializer(many=True,read_only=True)
    recommmended = SubscriptionOptionSerializer(many=True,read_only=True)
