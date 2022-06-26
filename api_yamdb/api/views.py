from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status

from rest_framework.response import Response

from reviews.models import Category, Genre, Title
from api.serializers import CategorySerializer, GenresSerializer
from api.serializers import TitlesSerializer, TitlesPOSTSerializer
from api.permissions import ReadOnly, IsRoleAdmin


class ListPostDel(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    pass


class CategoryViewSet(ListPostDel):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsRoleAdmin | ReadOnly,)
    lookup_field = 'slug'


class GenreViewSet(ListPostDel):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsRoleAdmin | ReadOnly,)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsRoleAdmin | ReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitlesPOSTSerializer
        return TitlesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        out_objecy = TitlesSerializer(instance=Title.objects.last())
        return Response(out_objecy.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        out_objecy = TitlesSerializer(instance=self.get_object())
        return Response(out_objecy.data)
