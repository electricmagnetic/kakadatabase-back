from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import mixins

from .serializers import ReportObservationSerializer


class ReportObservationViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    throttle_scope = 'report'
    permission_classes = (AllowAny, )
    serializer_class = ReportObservationSerializer
