from rest_framework import serializers

from .models import Stock, Product, StockProduct


class ProductSerializer(serializers.ModelSerializer):
        title = serializers.CharField(max_length=60)
        class Meta:
            model = Product
            fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(min_value=1)
    product = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=18, decimal_places=2)
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity','price']

class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['address', 'products']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        for item in positions:
            i = StockProduct.objects.create(stock=stock, **item)
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        for item in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=item.get('product'),
                defaults={'price': item.get('price'), 'quantity': item.get('quantity')})
        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock
