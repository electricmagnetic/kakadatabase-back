""" DRF router configuration """

from rest_framework.routers import DefaultRouter

from birds.views import BirdViewSet

router = DefaultRouter()

router.register(r'birds', BirdViewSet, 'Bird')
