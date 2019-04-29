#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
import os
import glob
import numpy as np
import datetime
from pydicom import dcmread
from pynetdicom import AE,StoragePresentationContexts
from pynetdicom.sop_class import MRImageStorage
import json


__version__=0.1

AEPORT=8104
AEIP='150.135.97.180'
AETITLE='XNAT'
PROJECT="CORT-TMS"

def get_parser():
	from argparse import ArgumentParser
	from argparse import RawTextHelpFormatter

	parser = ArgumentParser(description="Python DICOM transfer for XNAT."
		"Testing.",formatter_class=RawTextHelpFormatter)
	parser.add_argument('dicomdir', action='store',
		help='The root directory that contains the dicom folder of dicoms to send.')
	parser.add_argument('--config', action='store',
		help='File containing  config info for managing dicoms.')
	parser.add_argument('--logname', action='store',
		help='name for the log file (without extension) which will be created in work directory.')
	parser.add_argument('--workdir', action='store',
		help='Work directory for output of log file and other temporary files')

	return parser

def logtext(logfile, textstr):
	stamp=datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S%p")
	textstring=stamp + '  ' + textstr
	print(textstring)
	logfile.write(textstring+'\n')

def main():
	opts = get_parser().parse_args()
	ROOTDIR=os.path.abspath(opts.dicomdir)
	if opts.workdir:
		WORKDIR=os.path.abspath(opts.workdir)
	else:
		WORKDIR=os.getcwd()

	if opts.config:
		CONFIGFILE=os.path.abspath(opts.config)
	else:
		CONFIGFILE=None

	exclusions=[]
	if not CONFIGFILE == None:
		configFile=open(CONFIGFILE)
		configs=json.load(configFile)
		configFile.close()
		exclusions=configs["Exclude"]

	if opts.logname:
		BASELOGNAME=opts.logname
	else:
		BASELOGNAME='dicomTransfer'

	TIMESTAMP=datetime.datetime.now().strftime("%m%d%y%H%M%S%p")
	LOGFILENAME=BASELOGNAME + '_' + TIMESTAMP + '.log'
	LOGFILE = open(os.path.join(WORKDIR,LOGFILENAME), 'w')

	subjects = [f for f in glob.glob(ROOTDIR + '/*') if os.path.isdir(f)]

	for subject in subjects:
		subid=os.path.basename(subject)
		logtext(LOGFILE,"processing subject '" + subid + "' located at " + subject)

		#configure as a SCP
		ae = AE()
		ae.requested_contexts = StoragePresentationContexts
		#ae.add_requested_context(MRImageStorage)

		sesdicoms={}
		dicomdirs=[]
		for session in os.listdir(subject):
			logtext(LOGFILE, "Processing Session: " + session)
			for dicomdir in os.listdir(subject + '/' + session):
				logtext(LOGFILE, "Processing Dicom: " + dicomdir)
				skipdicom=False

				for index, value in enumerate(exclusions):
					if value.upper() in dicomdir.upper():
						logtext(LOGFILE, dicomdir + " will be excluded. continuing to next dicom")
						skipdicom=True
						break

				if skipdicom:
					continue

				fulldicomdir=subject + "/" + session + "/" + dicomdir
				#improve code below by using list.append and iterating over wildcards [dcm DCM IMA ima]

				dcmfiles=sorted(glob.glob(fulldicomdir+'/*.dcm'))
				if len(dcmfiles) == 0:
					dcmfiles=sorted(glob.glob(fulldicomdir+'/*.DCM'))
					if len(dcmfiles) == 0:
						dcmfiles=sorted(glob.glob(fulldicomdir+'/*.IMA'))
						if len(dcmfiles) == 0:
							dcmfiles=sorted(glob.glob(fulldicomdir+'/*.ima'))

				for dcmfile in dcmfiles:
					logtext(LOGFILE, "Processing DICOM : " + dcmfile)

					ds = dcmread(dcmfile)
					subnum = ''.join([i for i in subid if i.isdigit()])
					
					ds.PatientComments="Project:{PROJECT} Subject:{subnum} Session:{session}".format(PROJECT=PROJECT, subnum=subnum, session=session)
					assoc = ae.associate(AEIP, AEPORT,ae_title=AETITLE.encode('UTF-8'))
					if assoc.is_established:
						# Use the C-STORE service to send the dataset
						# returns the response status as a pydicom Dataset
						status = assoc.send_c_store(ds)

						# Check the status of the storage request
						if status:
							# If the storage request succeeded this will be 0x0000
							print('C-STORE request status: 0x{0:04x}'.format(status.Status))
						else:
							print('Connection timed out, was aborted or received invalid response')
						# Release the association
						assoc.release()
					else:
						print('Association rejected, aborted or never connected')


			logtext(LOGFILE,"Transforms completed for session "+session + " of subject " + subject)

	logtext(LOGFILE,"All Transforms completed for subject ." + subject)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()
