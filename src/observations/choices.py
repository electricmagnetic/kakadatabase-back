from birds.choices import SEX_CHOICES, LIFE_STAGE_CHOICES

# Contributor

ACTIVITY_CHOICES = (
    ('', ''),
    ('orokonui', 'Visiting Orokonui'),
    ('tourist', 'Tourist'),
    ('local', 'Local'),
    ('school', 'School Group'),
    ('community', 'Community Group'),
    ('skier', 'Skier'),
    ('tramper', 'Tramper'),
    ('hunter', 'Hunter'),
    ('birder', 'Birder'),
    ('doc', 'DOC Staff'),
    ('research', 'Researcher'),
    ('other', 'Other'),
)

HEARD_CHOICES = (
    ('', ''),
    ('orokonui', 'Orokonui Ecosanctuary'),
    ('poster', 'Poster'),
    ('brochure', 'Brochure'),
    ('social', 'Social Media'),
    ('news', 'News'),
    ('friend', 'From a friend'),
    ('other', 'Other'),
)

# Observation

PRECISION_CHOICES = (
    (10, '(10m) GPS Coordinates'),
    (50, '(50m) Known Location'),
    (200, '(200m) Approximate Location'),
    (1000, '(1000m) General Area'),
    (5000, '(5000m) Educated Guess'),
)

OBSERVATION_TYPE_CHOICES = (
    ('sighted', 'Sighted'),
    ('heard', 'Heard'),
    ('distant', 'Sighted (distant)'),
)

STATUS_CHOICES = (
    ('new', 'New'),
    ('public', 'Verified (Public)'),
    (
        'Private', (
            ('private', 'Verified (Private)'),
            ('bad', 'Bad (Private)'),
        )
    ),
    ('Special', (('captive', 'Captive Sighting'), )),
)

# BirdObservation

BAND_CHOICES = (
    ('unknown', 'Couldn\'t tell'),
    ('unreadable', 'Banded, unreadable'),
    ('readable', 'Banded, readable'),
    ('unbanded', 'Not banded'),
)

SEX_CHOICES_UNSURE = (('', 'Unsure'), ) + SEX_CHOICES
LIFE_STAGE_CHOICES_UNSURE = (('', 'Unsure'), ) + LIFE_STAGE_CHOICES
