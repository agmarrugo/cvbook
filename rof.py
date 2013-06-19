import numpy

def denoise(im, U_init, tolerance=0.1, tau=0.125, tv_weight=100):
  """Denoises |im| using the ROF image denoising model."""
  # THe code is from Jan Erik Solem's book; it's based on:
  # Chambolle 2005, eq 11 on p14 "Total variation minimization and a class of
  # binary MRF models"
  # http://www.cmap.polytechnique.fr/preprint/repository/578.pdf

  m, n = im.shape

  U = U_init
  Px = im
  Py = im
  error = 1

  while error > tolerance:
    Uold = U

    GradUx = numpy.roll(U, -1, axis=1)
    GradUy = numpy.roll(U, -1, axis=0)

    PxNew = Px + (tau / tv_weight) * GradUx
    PyNew = Py + (tau / tv_weight) * GradUy
    NormNew = numpy.maximum(1, numpy.sqrt(PxNew**2 + PyNew**2))

    Px = PxNew / NormNew
    Py = PyNew / NormNew

    RxPx = numpy.roll(Px, 1, axis=1)
    RyPy = numpy.roll(Py, 1, axis=0)

    DivP = (Px - RxPx) + (Py - RyPy)
    U = im + tv_weight * DivP

    error = numpy.linalg.norm(U - Uold) / numpy.sqrt(n * m)

  return U, im - U
