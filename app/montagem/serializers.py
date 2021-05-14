from rest_framework import serializers

from core.models import Tag, Atributo, Montagem


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class AtributoSerializer(serializers.ModelSerializer):
    """Serializer for atributo objects"""

    class Meta:
        model = Atributo
        fields = ('id', 'name')
        read_only_fields = ('id',)


class MontagemSerializer(serializers.ModelSerializer):
    """Serialize a linha de montagem"""
    atributos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Atributo.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Montagem
        fields = (
            'id', 'titulo', 'atributos', 'tags', 'tempo_execucao',
            'preco', 'link'
        )
        read_only_fields = ('id',)


class MontagemDetailSerializer(MontagemSerializer):
    """Serialize o detalhe da linha de montagem"""
    atributos = AtributoSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class MontagemImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to linha de montagens"""

    class Meta:
        model = Montagem
        fields = ('id', 'image')
        read_only_fields = ('id',)
