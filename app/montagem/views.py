from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Atributo, Montagem

from montagem import serializers


class BaseMontagemAttrViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Visualizacoes de base de propriedade do usuario"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retorna objetos apenas para o usuario autenticado atual"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(montagem__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseMontagemAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class AtributoViewSet(BaseMontagemAttrViewSet):
    """Manage atributos in the database"""
    queryset = Atributo.objects.all()
    serializer_class = serializers.AtributoSerializer


class MontagemViewSet(viewsets.ModelViewSet):
    """Manage linha d emontagem in the database"""
    serializer_class = serializers.MontagemSerializer
    queryset = Montagem.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Recupere as linhas demontagem para o usuario autenticado"""
        tags = self.request.query_params.get('tags')
        atributos = self.request.query_params.get('atributos')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if atributos:
            atributo_ids = self._params_to_ints(atributos)
            queryset = queryset.filter(atributos__id__in=atributo_ids)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.MontagemDetailSerializer
        elif self.action == 'upload_image':
            return serializers.MontagemImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Cria uma nova linha de montagem"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload de umagem para uma linha de montagem"""
        montagem = self.get_object()
        serializer = self.get_serializer(
            montagem,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
