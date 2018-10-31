#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

.. codeauthor:: Rasmus Handberg <rasmush@phys.au.dk>
"""

from __future__ import division, with_statement, print_function, absolute_import
from six.moves import range
import argparse
import os
import numpy as np
from datetime import datetime
from astropy.io import fits
import glob

__version__ = '0.1'

def fits2txt(fname, overwrite=False):

	bname = os.path.basename(fname)
	bname = bname.replace('.fits.gz', '').replace('.fits', '')
	savefile = os.path.join(os.path.dirname(fname), bname + '.dat')
	
	if not overwrite and os.path.exists(savefile):
		return savefile

	now = datetime.now()

	with fits.open(fname, mode='readonly', memmap=True) as hdu:
		# Headers:
		starid = hdu[0].header['TICID']
		sector = hdu[0].header['SECTOR']
		datarel = hdu[0].header['DATA_REL']
		cadence = hdu['LIGHTCURVE'].header['TIMEDEL']*86400
		if cadence < 40:
			cadence = 20
		elif cadence < 200:
			cadence = 120
		else:
			cadence = 1800

		if hdu[0].header.get('ORIGIN', '') == 'NASA/Ames':
			photmeth = 'SAP'
			corrmeth = 'PDC ' + hdu[1].header.get('PDCMETHD', '')
			version = ''
			fileid = ''
			# Data columns:
			time = hdu['LIGHTCURVE'].data['TIME']
			time_unit = hdu['LIGHTCURVE'].columns['TIME'].unit # days, BJD - 2457000
			
			flux_raw = hdu['LIGHTCURVE'].data['SAP_FLUX']
			flux_raw_err = hdu['LIGHTCURVE'].data['SAP_FLUX_ERR']
			flux_raw_err_unit = hdu['LIGHTCURVE'].columns['SAP_FLUX'].unit
			
			flux_corr = hdu['LIGHTCURVE'].data['PDCSAP_FLUX']
			flux_corr_err = hdu['LIGHTCURVE'].data['PDCSAP_FLUX_ERR']
			flux_corr_err_unit = hdu['LIGHTCURVE'].columns['PDCSAP_FLUX'].unit
			
			quality = hdu['LIGHTCURVE'].data['QUALITY']
		else:
			photmeth = hdu[1].header.get('PHOTMETH', '')
			corrmeth = hdu[1].header.get('CORRMETH', '')
			version = hdu[0].header['VERSION']
			fileid = hdu[0].header.get('FILEID', None)
			# Data columns:
			time = hdu['LIGHTCURVE'].data['TIME']
			time_unit = hdu['LIGHTCURVE'].columns['TIME'].unit # days, BJD - 2457000
			
			flux_raw = hdu['LIGHTCURVE'].data['FLUX_RAW']
			#if 'FLUX_RAW_ERR' in hdu['LIGHTCURVE'].data.keys():
			#	flux_raw_err = hdu['LIGHTCURVE'].data['FLUX_RAW_ERR']
			#else:
			flux_raw_err = np.full(len(time), np.NaN)
			flux_raw_err_unit = hdu['LIGHTCURVE'].columns['FLUX_RAW'].unit
			
			flux_corr = hdu['LIGHTCURVE'].data['FLUX_CORR']
			flux_corr_err = hdu['LIGHTCURVE'].data['FLUX_CORR_ERR']
			flux_corr_err_unit = hdu['LIGHTCURVE'].columns['FLUX_CORR'].unit
			
			quality = hdu['LIGHTCURVE'].data['QUALITY']
			
	# Write output file:
	with open(savefile, 'w', newline='\r\n') as fid:
		fid.write("# TESS Asteroseismic Science Operations Center\n")
		fid.write("# Created using fits2txt version %s on %s\n" % (__version__, now))
		fid.write("# TIC identifier:    %d\n" % starid)
		fid.write("# Sector:            %s\n" % sector)
		fid.write("# Cadence:           %d\n" % cadence)
		fid.write("# Data Release:      %d\n" % datarel)
		fid.write("# Version:           %s\n" % version)
		fid.write("# Photometry method: %s\n" % photmeth)
		fid.write("# Correction method: %s\n" % corrmeth.strip())
		fid.write("# Unique ID:         %s\n" % fileid)
		fid.write("#\n")
		fid.write("# Column 1: Time (%s)\n" % time_unit)
		fid.write("# Column 2: Raw flux (%s)\n" % flux_raw_err_unit)
		fid.write("# Column 3: Raw flux error (%s)\n" %  flux_raw_err_unit)
		fid.write("# Column 4: Corrected flux (%s)\n" % flux_corr_err_unit)
		fid.write("# Column 5: Corrected flux error (%s)\n" % flux_corr_err_unit)
		fid.write("# Column 6: Quality flags\n")
		fid.write("#-------------------------------------------------\n")
		for i in range(len(time)):
			fid.write("%15.9f  %22.15e  %22.15e  %22.15e  %22.15e  %9d\n" % (
				time[i],
				flux_raw[i],
				flux_raw_err[i],
				flux_corr[i],
				flux_corr_err[i],
				quality[i]
			))
		fid.write("#-------------------------------------------------\n")
		
	return savefile


if __name__ == '__main__':
	# Parse command line arguments:
	parser = argparse.ArgumentParser(description='Convert TESS FITS files to ASCII.')
	parser.add_argument('-q', '--quiet', help='Only report warnings and errors.', action='store_true')
	parser.add_argument('-r', '--recursive', help='Run recursive.', action='store_true')
	parser.add_argument('-f', '--force', help='Force overwrite of existing files.', action='store_true')
	parser.add_argument('file')
	args = parser.parse_args()

	print(args)
	if args.recursive:
		args.file = args.file.replace('*', '**')

	for fname in glob.iglob(args.file, recursive=args.recursive):
		if not os.path.isfile(fname): continue
		if fname.endswith('.fits') or fname.endswith('.fits.gz'):
			fits2txt(fname, overwrite=args.force)
		elif not args.quiet:
			print("Skipping non-FITS file '%s'." % fname)