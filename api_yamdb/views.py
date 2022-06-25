from rest_framework import mixins
from rest_framework import viewsets

from reviews.models import Category, Genre, Title
from api.serializers import CategorySerializer, GenresSerializer
from api.serializers import TitlesSerializer, TitlesPOSTSerializer
from api.permissions import SuperOrAdminOrReadOnly


class ListPostDel(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    pass


class CategoryViewSet(ListPostDel):
    queryset = Category.objects.all()
    #permission_classes = SuperOrAdminOrReadOnly
    lookup_field = 'slug'


class GenreViewSet(ListPostDel):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    #permission_classes = SuperOrAdminOrReadOnly
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    #permission_classes = SuperOrAdminOrReadOnly

    # def get_serializer_class(self):
    #     if self.request.method in ('POST', 'PATCH',):
    #         return TitlesPOSTSerializer
    #     return TitlesSerializer

    def create(self, validated_data):
        print(validated_data.data['category'])
        slug_category = validated_data.data['category']
        category_object = list(Category.objects.filter(slug=slug_category))
        validated_data.data['category'] = category_object
        title = Title.objects.create(**validated_data)
        return title