""" DRF router configuration """

from rest_framework.routers import DefaultRouter

from birds.views import BirdViewSet
from observations.views import ObservationViewSet, BirdObservationViewSet

router = DefaultRouter()

router.register(r'birds', BirdViewSet, 'Bird')
router.register(r'observations', ObservationViewSet, 'Observation')
router.register(r'bird_observations', BirdObservationViewSet, 'BirdObservation')
