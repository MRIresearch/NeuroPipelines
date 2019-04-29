#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
import os
import glob
import numpy as np
import pydicom
import datetime

__version__=0.1

def get_parser():
	from argparse import ArgumentParser
	from argparse import RawTextHelpFormatter

	parser = ArgumentParser(description="Python DICOM manipulation for XNAT."
		"Testing.",formatter_class=RawTextHelpFormatter)
	parser.add_argument('dicomdir', action='store',
		help='The root directory that contains the dicom folder.')
	parser.add_argument('--logname', action='store',
		help='name for the log file (without extension) which will be created in work directory.')
	parser.add_argument('stagedir', action='store',
		help='The directorywhere dicoms will be staged for BIDSkit.')
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
	STAGEDIR=os.path.abspath(opts.stagedir)
	if opts.workdir:
		WORKDIR=os.path.abspath(opts.workdir)
	else:
		WORKDIR=os.getcwd()

	if opts.logname:
		BASELOGNAME=opts.logname
	else:
		BASELOGNAME='dicomTransform'

	TIMESTAMP=datetime.datetime.now().strftime("%m%d%y%H%M%S%p")
	LOGFILENAME=BASELOGNAME + '_' + TIMESTAMP + '.log'
	LOGFILE = open(os.path.join(WORKDIR,LOGFILENAME), 'w')

	subjects = [f for f in glob.glob(ROOTDIR + '/*') if os.path.isdir(f)]

	for subject in subjects:
		subid=os.path.basename(subject)
		SUBJECTDIROUT=os.path.join(STAGEDIR,subid)
		logtext(LOGFILE,"processing subject " + subject)

		sesdicoms={}
		dicomdirs=[]
		for session in os.listdir(subject):
			logtext(LOGFILE, "Processing Session: " + session)
			for dicomdir in os.listdir(subject + '/' + session):
				logtext(LOGFILE, "Processing Dicom: " + dicomdir)
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

					ds = pydicom.dcmread(dcmfile)
					#hard coded for testing below
					subnum = ''.join([i for i in subid if i.isdigit()])
					PROJECT="CORT-TMS"
					ds.PatientComments="Project:{PROJECT} Subject:{subnum} Session:{session}".format(PROJECT=PROJECT, subnum=subnum, session=session)

					#hard coded for testing below
					#ds.PatientComments="Project:CORT-TMS Subject:002 Session:post"

					dicomfile=os.path.basename(dcmfile)
					outputdir=os.path.join(SUBJECTDIROUT + '/' + session, dicomdir)
					if not os.path.exists(outputdir):
						os.makedirs(outputdir)
					output_filename=(os.path.join(outputdir,dicomfile))
					ds.save_as(output_filename)
			logtext(LOGFILE,"Transforms completed for session "+session + " of subject " + subject)

	logtext(LOGFILE,"All Transforms completed for subject ." + subject)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()
