from django.core.exceptions import ValidationError

from kakadatabase.parameters import COLOURS, SEPARATORS

def validate_separators(value):
    """ Validate that there is max one leg separator and max two band separators """

    if value.count(SEPARATORS['LEG']) > 1:
        raise ValidationError(
            'Invalid number of leg separators',
            params={'value': value},
        )

    if value.count(SEPARATORS['BAND']) > 2:
        raise ValidationError(
            'Invalid number of band separators',
            params={'value': value},
        )

def validate_combo(value):
    """ Check that the combo is valid after parsing """

    if value == '':
        raise ValidationError('Combo parsing found no valid data. Data has not been modified.')
