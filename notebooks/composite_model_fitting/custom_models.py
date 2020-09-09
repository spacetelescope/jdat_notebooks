import astropy.constants as ac
import numpy as np

import astropy.modeling.models as models
from astropy.modeling import Fittable1DModel, Parameter


def ccm(wav, ebmv=1, rv=3.5):
    '''computes reddening correction according to the Cardelli, Clayton and Mathis 
    model (ApJ 1989 v345, p245)
    
    wav: wavelengths in microns (expect a numpy array of wavelengths
    ebmv: e(B-V) in magnitudes
    rv:  Rv = A(V)/E(B-V) 
    '''
    x = 1./wav
    irmask = (x >= 0.3) & (x <= 1.1)
    omask  = (x >  1.1) & (x <= 3.3)
    nuvmask1 = (x > 3.3) & (x <= 8.0) 
    nuvmask2 = (x >= 5.9) & (x <= 8.0)
    fuvmask = (x > 8.0) & (x <= 20.)
    a = 0*x
    b = 0*x
    # IR
    xir = x[irmask]**1.61
    a[irmask] = 0.574 * xir
    b[irmask] = -0.527 * xir
    # Optical (could do this better numerically)
    xopt = x[omask] - 1.82
    a[omask] = (1.0 + 0.17699 * xopt - 0.50477 * xopt**2 - 0.02427 * xopt**3 +
                  0.72085 * xopt**4 + 0.01979 * xopt**5 - 0.77530 * xopt**6 +
                  0.32999 * xopt**7)
    b[omask] = (0.0 + 1.41338 * xopt + 2.28305 * xopt**2 + 1.07233 * xopt**3 -
                  5.38434 * xopt**4 - 0.62551 * xopt**5 + 5.30260 * xopt**6 -
                  2.09002 * xopt**7)
    # Near UV
    xnuv1 = x[nuvmask1]
    a[nuvmask1] = 1.752 - 0.316 * xnuv1 - 0.104 / (0.341 + (xnuv1-4.67)**2)
    b[nuvmask1] = - 3.090 + 1.825 * xnuv1 + 1.206 / (0.263 + (xnuv1-4.62)**2)
    xnuv2 = x[nuvmask2] - 5.9
    a[nuvmask2] += -0.04473 * xnuv2**2 - 0.009779 * xnuv2**3
    b[nuvmask2] +=  0.21300 * xnuv2**2 + 0.120700 * xnuv2**3

    # Far UV
    xfuv = x[fuvmask] - 8.0
    a[fuvmask] = -1.073 - 0.628 * xfuv + 0.137 * xfuv**2 - 0.070 * xfuv**3
    b[fuvmask] = 13.670 + 4.257 * xfuv - 0.420 * xfuv**2 + 0.374 * xfuv**3

    result = 10 ** (-0.4 * ebmv * (rv * a + b))

    return result


def bipolar_gaussian(x, norm=1., mean=0., fwhm=1., skew=1.):
    '''A two-faced gaussian based on the version in stsdas.contrib.specfit

    Effectively, this gaussian has two different sigmas on each side of the
    mean. For values less than the mean, the sigma is as specified. For values
    greater than the mean, the new sigma = skew * specified sigma

    Units for fwhm are km/s
    norm represents total flux (presumably in arbitrary units)
    mean is called the centroid, but that seems misleading. It is the maximum
    of the dual faced gaussian.

    The units of mean and x should be consistent.
    '''
    sqrt2pi = np.sqrt(2.* np.pi)
    sigma = mean * fwhm / ac.c.to('km/s').value / 2.354820044
    val = 0. * x
    lowerx = (x > (mean - 10*sigma)) & (x < mean)
    upperx = (x < (mean + 10*sigma*skew)) & (x > mean)
    term = - ((x-mean)/sigma) ** 2 / 2.
    val[lowerx] = 2 * norm * np.exp(term[lowerx]) / sigma / sqrt2pi / (1. + skew)
    val[upperx] = 2 * norm * np.exp(term[upperx]/skew**2) / sigma / sqrt2pi / (1. + skew)
    return val



# Classes that extend Fittable1DModel to provide for specfit's needs.

class gaussian(Fittable1DModel):
    '''A two-faced gaussian based on the version in stsdas.contrib.specfit

    Effectively, this gaussian has two different sigmas on each side of the
    mean. For values less than the mean, the sigma is as specified. For values
    greater than the mean, the new sigma = skew * specified sigma

    Units for fwhm are km/s
    norm represents total flux (presumably in arbitrary units)
    mean is called the centroid, but that seems misleading. It is the maximum
    of the dual faced gaussian.

    The units of mean and x should be consistent.

    '''
    norm = Parameter(default=1)
    mean = Parameter(default=0)
    fwhm = Parameter(default=1)
    skew = Parameter(default=1)

    @staticmethod
    def evaluate(x, norm, mean, fwhm, skew):
        return bipolar_gaussian(x, norm, mean, fwhm, skew)


class ccmext(Fittable1DModel):
    '''computes reddening correction according to the Cardelli, Clayton and Mathis
    model (ApJ 1989 v345, p245)

    x: wavelengths in Angstrom (expect a numpy array of wavelengths
    ebmv: e(B-V) in magnitudes
    rv:  Rv = A(V)/E(B-V)

    '''
    ebmv = Parameter(default=1.0)
    rv = Parameter(default=3.5)

    @staticmethod
    def evaluate(x, ebmv, rv):
        return ccm(x/10000., ebmv, rv)


# these are not strictly necessary since the powerlaw could be instantiated
# directly from astropy. I keep then here as placeholders for future
# enhancements.
class powerlaw(models.PowerLaw1D):
    # Parameter names must be identical with the superclass'.
    # This requirement comes from the 'guimodel' project, in
    # which we deal with the innards of spectral components.
    def __init__(self, amplitude, x_0, alpha, **kwargs):
        super(powerlaw, self).__init__(amplitude, x_0, alpha, **kwargs)

class powerlaw_2(models.PowerLaw1D):
    def __init__(self, *args, **kwargs):
        amp = args[0]
        x0  = args[1]
        alpha  = args[2]
        super(powerlaw_2, self).__init__(amp, x0, alpha, **kwargs)


