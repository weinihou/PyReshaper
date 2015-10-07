#!/usr/bin/env python
"""
Script to generate NetCDF data needed for testing

Copyright 2015, University Corporation for Atmospheric Research
See the LICENSE.rst file for details
"""

import Nio
import numpy as np


def make_data(nlat=19,
              nlon=36,
              ntime=10,
              slices=['tslice{}.nc'.format(i) for i in xrange(5)],
              scalars=['scalar{}.nc'.format(i) for i in xrange(2)],
              timvars=['timvar{}.nc'.format(i) for i in xrange(2)],
              tvmvars=['tvmvar{}.nc'.format(i) for i in xrange(2)],
              tsvars=['tsvar{}.nc'.format(i) for i in xrange(4)],
              fattrs={'attr1': 'attribute one', 'attr2': 'attribute two'}):
    """
    Using PyNIO, generate data needed for unit tests
    """

    # Generate nslice time slices
    filenames = []
    for i in xrange(len(slices)):

        # Open the file for writing
        fname = slices[i]
        filenames.append(fname)
        fobj = Nio.open_file(fname, 'w')

        # Write attributes to file
        for name, value in fattrs.iteritems():
            setattr(fobj, name, value)

        # Create the dimensions in the file
        fobj.create_dimension('lat', nlat)
        fobj.create_dimension('lon', nlon)
        fobj.create_dimension('time', None)

        # Create the coordinate variables & add attributes
        lat = fobj.create_variable('lat', 'f', ('lat',))
        lon = fobj.create_variable('lon', 'f', ('lon',))
        time = fobj.create_variable('time', 'f', ('time',))

        # Set the coordinate variable attributes
        setattr(lat, 'long_name', 'latitude')
        setattr(lon, 'long_name', 'longitude')
        setattr(time, 'long_name', 'time')
        setattr(lat, 'units', 'degrees north')
        setattr(lon, 'units', 'degrees east')
        setattr(time, 'units', 'days from 01-01-0001')

        # Set the values of the coordinate variables
        lat[:] = np.linspace(-90, 90, nlat, dtype=np.float32)
        lon[:] = np.linspace(-180, 180, nlon, endpoint=False, dtype=np.float32)
        time[:] = np.arange(i * ntime, (i + 1) * ntime, dtype=np.float32)

        # Create the scalar variables
        for n in xrange(len(scalars)):

            vname = scalars[n]
            v = fobj.create_variable(vname, 'd', ())
            setattr(v, 'long_name', 'scalar{}'.format(n))
            setattr(v, 'units', '[{}]'.format(vname))
            v.assign_value(np.float64(n * 10))

        # Create the time-invariant metadata variables
        for n in xrange(len(timvars)):

            vname = timvars[n]
            v = fobj.create_variable(vname, 'd', ('lat', 'lon'))
            setattr(v, 'long_name', 'time-invariant metadata {}'.format(n))
            setattr(v, 'units', '[{}]'.format(vname))
            v[:] = np.ones((nlat, nlon), dtype=np.float64)

        # Create the time-variant metadata variables
        for n in xrange(len(tvmvars)):

            vname = tvmvars[n]
            v = fobj.create_variable(vname, 'd', ('time', 'lat', 'lon'))
            setattr(v, 'long_name', 'time-variant metadata {}'.format(n))
            setattr(v, 'units', '[{}]'.format(vname))
            v[:] = np.ones((ntime, nlat, nlon), dtype=np.float64)

        # Create the time-variant metadata variables
        for n in xrange(len(tsvars)):

            vname = tsvars[n]
            v = fobj.create_variable(vname, 'd', ('time', 'lat', 'lon'))
            setattr(v, 'long_name', 'time-series variable {}'.format(n))
            setattr(v, 'units', '[{}]'.format(vname))
            v[:] = np.ones((ntime, nlat, nlon), dtype=np.float64)

    return

if __name__ == '__main__':
    make_data()
