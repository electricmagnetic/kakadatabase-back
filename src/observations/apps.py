from django.apps import AppConfig
from django.db.models.signals import pre_save

from .signals import run_geocode


class ObservationsConfig(AppConfig):
    name = 'observations'

    def ready(self):
        Observation = self.get_model('Observation')
        pre_save.connect(run_geocode, sender='observations.Observation')
