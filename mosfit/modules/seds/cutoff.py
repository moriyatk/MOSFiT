import numpy as np
from astropy import constants as c

from mosfit.modules.seds.sed import SED

CLASS_NAME = 'Cutoff'


class Cutoff(SED):
    """Apply a cutoff in the UV to the SED.
    """

    def process(self, **kwargs):
        self._seds = kwargs['seds']
        self._band_indices = kwargs['all_band_indices']
        self._frequencies = kwargs['all_frequencies']
        for si, sed in enumerate(self._seds):
            bi = self._band_indices[si]
            if bi >= 0:
                wav_arr = self._sample_wavelengths[bi]
            else:
                wav_arr = [c.c.cgs.value / self._frequencies[si]]

            norm = np.sum(sed)

            # Account for UV absorption: 0% transmission at 0 A, 100% at 3500A
            sed[wav_arr < 3500] *= (2.857e-2 * wav_arr[wav_arr < 3500])

            # Normalize SED so no energy is lost
            sed *= norm / np.sum(sed)

            self._seds[si] = sed

        return {'seds': self._seds}
