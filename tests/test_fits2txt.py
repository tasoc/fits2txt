#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. codeauthor:: Rasmus Handberg <rasmush@phys.au.dk>
"""

from __future__ import division, print_function, with_statement, absolute_import
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from fits2txt import fits2txt

def test_fits2txt():
	"""Test of background estimator"""

	# Load the first image in the input directory:
	INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input', 'hlsp_tess-data-alerts_tess_phot_00025155310-s01_tess_v1_lc.fits.gz')

	# Run the converter:
	OUTPUT_FILE = fits2txt(INPUT_FILE, overwrite=True)
	assert os.path.exists(OUTPUT_FILE), "Output file not created"	
	
	# This should simply return the same file name:
	OUTPUT_FILE2 = fits2txt(INPUT_FILE, overwrite=False)
	assert OUTPUT_FILE == OUTPUT_FILE2, "Output files are not the same"
	
	# Check that we can load the file in using simple numpy:
	data = np.loadtxt(OUTPUT_FILE)
	assert data.shape == (20076, 6), "Not the correct data shape"
	
	
if __name__ == '__main__':
	test_fits2txt()
