import swisseph as swe

import astroapp.utils.swiss_ephemeris_setup

from django.conf import settings

# Configure le chemin des éphémérides
swe.set_ephe_path(settings.SWISSEPH_EPHEMERIS_PATH)

