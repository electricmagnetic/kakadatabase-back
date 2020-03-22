""" DRF router configuration """

from rest_framework.routers import DefaultRouter

from bands.views import BandComboViewSet
from birds.views import BirdViewSet
from observations.views import ObservationViewSet, BirdObservationViewSet
from report.views import ReportObservationViewSet

router = DefaultRouter()

router.register(r'band_combos', BandComboViewSet, 'BandCombo')
router.register(r'birds', BirdViewSet, 'Bird')
router.register(r'observations', ObservationViewSet, 'Observation')
router.register(r'bird_observations', BirdObservationViewSet, 'BirdObservation')
router.register(r'report', ReportObservationViewSet, 'ReportObservation')
