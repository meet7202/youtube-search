import django_filters
from functools import reduce
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, status, viewsets, pagination, status

from .serializers import YTVideoSerializer
from .models import YoutubeVideo


# class YTListAPIView(APIView):
#     queryset = YoutubeVideo.objects.all()
#     serializer_class = YTVideoSerializer
#     pagination_class = pagination.PageNumberPagination
#     #filter_class = YTFilter

#     def get_serializer(self, *args, **kwargs):
#         serializer_class = self.serializer_class
#         return serializer_class(*args, **kwargs)

#     def get(self, request):
#         q = self.request.query_params.get('q', None)
#         if q:
#             self.queryset = self.queryset.filter(key_words__name__in=[q])
#             return Response(data=self.serializer_class(self.queryset, many=True).data, status=200)
#         else:
#             return Response({"No"}, status=400)

class PNPagination(pagination.PageNumberPagination):
    page_size = 5
    ordering = ('-published_at')

class YTTagsFilter(django_filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        key_words = [x.lower() for x in value.split(',')]
        q = Q()
        for word in key_words:
            q |= (Q(**{'%s__%s' % ('key_words__name', 'icontains'): word}) |
                Q(**{'%s__%s' % ('key_words__name', 'in'): word}) |
                Q(**{'%s__%s' % ('title', 'icontains'): word}) |
                Q(**{'%s__%s' % ('description', 'icontains'): word})
                )
        return qs.filter(q).distinct()

class YTFilter(django_filters.FilterSet):
    q = YTTagsFilter()

    class Meta:
        model = YoutubeVideo
        fields = ['q']

class YTListAPIViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = YoutubeVideo.objects.all()
    serializer_class = YTVideoSerializer
    pagination_class = PNPagination
    filter_class = YTFilter
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    def list(self, request, *args, **kwargs):
        return super(YTListAPIViewset, self).list(request, args, kwargs)