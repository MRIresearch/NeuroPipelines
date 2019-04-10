#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
import os
import glob
from sklearn.cluster import KMeans
import numpy as np
import pydicom
import datetime
from distutils.dir_util import copy_tree
from subprocess import call
from shutil import copyfile
from shutil import rmtree
import json
import sys

__version__=0.1

def get_parser():
	from argparse import ArgumentParser
	from argparse import RawTextHelpFormatter

	parser = ArgumentParser(description="Dicom to BIDS converter using BIDSkit."
		"BIDSkit and dcm2niix need to be installed.",formatter_class=RawTextHelpFormatter)
	parser.add_argument('dicomdir', action='store',
		help='The root directory that contains the dicom folders to convert to BIDS.')
	parser.add_argument('stagedir', action='store',
		help='The directorywhere dicoms will be staged for BIDSkit.')
	parser.add_argument('bidsdir', action='store',
		help='The directory where BIDSkit will place the bids files')
	parser.add_argument('--bidskit', action='store',
		help='The path to dcm2bids.py in BIDSkit library')
	parser.add_argument('--sessions', action='store',type=str, nargs='*',
		help='session names separated by space (without the ses- prefix) e.g. --sessions pre post')
	parser.add_argument('--workdir', action='store',
		help='Work directory for output of log file and other temporary files')
	parser.add_argument('--bidstranslator', action='store',
		help='location of the bids translator file created by BIDSkit if it already exists.')
	parser.add_argument('--logname', action='store',
		help='name for the log file (without extension) which will be created in work directory.')
	parser.add_argument('--bypass', action='store_true', default=False,
		help='Only run dicom copy for subjects that have not been copied over before')
	parser.add_argument('--stageonly', action='store_true', default=False,
		help='Use this flag to just stage the dicoms into appropriate hierachy for BIDSKIT')
	parser.add_argument('--convertonly', action='store_true', default=False,
		help='Use this flag if second pass of BIDS kit is required and translator file is already in situ')
	parser.add_argument('--incremental', action='store_true', default=False,
		help='Use this flag if just adding a new subject. Otherwise work directory and derivatives directories will be deleted.')
	parser.add_argument('--exceptionlist', action='store',
		help='File containing list of exception dicoms to be manually identifed due to problems with the obtained datetime')
	parser.add_argument('--noprompt',action='store_true', default=False,
		help='Use this flag to bypass prompts. Necessary for running on the HPC')
	parser.add_argument('--noanon', action='store_true', default=False,help='do not anonymize json files')
	parser.add_argument('--version', action='version', version='nklab-bids-convert v{}'.format(__version__))
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
	OUTPUTDIR=os.path.abspath(opts.bidsdir)
	if opts.workdir:
		WORKDIR=os.path.abspath(opts.workdir)
	else:
		WORKDIR=os.getcwd()

	BIDSROOTDIR= os.path.dirname(STAGEDIR)
	BIDSKITROOTDIR = os.path.join(BIDSROOTDIR, 'derivatives', 'conversion')
	BIDSKITWORKDIR = os.path.join(BIDSROOTDIR, 'work', 'conversion')
	ProtocolTranslator=os.path.join(BIDSKITROOTDIR,"Protocol_Translator.json")
	origProtocolTranslator=os.path.join(BIDSKITROOTDIR,"origProtocol_Translator.json")

	if opts.bidskit:
		BIDSKIT=os.path.abspath(opts.bidskit)
	else:
		BIDSKIT="/opt/bin/bidskit"

	if opts.sessions:
		SESSIONS=opts.sessions
		CLUSTER=len(SESSIONS)
	else:
		CLUSTER=0

	if opts.bidstranslator:
		BIDSTRANSLATOR=os.path.abspath(opts.bidstranslator)
	else:
		BIDSTRANSLATOR=None

	if opts.exceptionlist:
		EXCEPTIONFILE=os.path.abspath(opts.exceptionlist)
	else:
		EXCEPTIONFILE=None

	if opts.logname:
		BASELOGNAME=opts.logname
	else:
		BASELOGNAME='nklab-bids-convert'

	bCONVERTONLY=opts.convertonly
	bBYPASS=opts.bypass
	bNOPROMPT=opts.noprompt
	bNOANON= opts.noanon
	bINCREMENTAL= opts.incremental
	bSTAGEONLY=opts.stageonly

	# always run conversions only incrementally
	if bCONVERTONLY:
		bINCREMENTAL=True

	TIMESTAMP=datetime.datetime.now().strftime("%m%d%y%H%M%S%p")
	LOGFILENAME=BASELOGNAME + '_' + TIMESTAMP + '.log'
	LOGFILE = open(os.path.join(WORKDIR,LOGFILENAME), 'w')
	BackupProtocolTranslator=os.path.join(BIDSKITROOTDIR,"backup_Protocol_Translator_" + TIMESTAMP +  ".json")

	FINALERRORS=""

	#add code to only search for directories
	subjects = [f for f in glob.glob(ROOTDIR + '/*') if os.path.isdir(f)]

	for subject in subjects:

		SUBJECTDIROUT=os.path.join(STAGEDIR,os.path.basename(subject))

		logtext(LOGFILE,"processing subject " + subject)
		if CLUSTER > 0:
			logtext(LOGFILE,"setting up BIDS hierarchy for " + str(CLUSTER) + " sessions > " + str(SESSIONS))
		else:
			logtext(LOGFILE,"setting up BIDS hierarchy without sessions")

		if os.path.exists(SUBJECTDIROUT):
			logtext(LOGFILE, "Subject " + subject + " already exists.")
			if bBYPASS:
				logtext(LOGFILE, "Processing will skip to next subject")
				continue
			else:
				logtext(LOGFILE, "Existing files will be overwritten")

		dicomdirs=[]
		for root, dirs, files in os.walk(subject,topdown=False):
			for name in dirs:
				subdir=os.path.join(root,name)
				#need a better method below for case insensitive and user supplied globbing
				if len(glob.glob(subdir + '/*.dcm')) > 0 or len(glob.glob(subdir + '/*.IMA')) > 0:
					dicomdirs.append(subdir)
				if len(glob.glob(subdir + '/*.DCM')) > 0 or len(glob.glob(subdir + '/*.ima')) > 0:
					dicomdirs.append(subdir)
		acquisitions=[]
		datetime_str=""
		for dicomdir in dicomdirs:
			dcmfiles=glob.glob(dicomdir+'/*.dcm')
			if len(dcmfiles) == 0:
				dcmfiles=glob.glob(dicomdir+'/*.DCM')
				if len(dcmfiles) == 0:
					dcmfiles=glob.glob(dicomdir+'/*.IMA')
					if len(dcmfiles) == 0:
						dcmfiles=glob.glob(dicomdir+'/*.ima')
			dcmfile=dcmfiles[0]
			logtext(LOGFILE, "Processing DICOM : " + dcmfile)
			ds = pydicom.dcmread(dcmfile)
			try:
				date = ds.AcquisitionDate
				time = ds.AcquisitionTime
				datetime_str=date + ' ' + time
			except:
				logtext(LOGFILE, "Date and/or time missing for DICOM : " + dcmfile)
				FINALERRORS=FINALERRORS + "Date and/or time missing for DICOM : " + dcmfile + "\n"
				logtext(LOGFILE, "Ensure that this DICOM is defined in exception.json and then run conversion again")
				FINALERRORS=FINALERRORS + "Ensure that this DICOM is defined in exception.json and then run conversion again." + "\n\n"
				if len(datetime_str) == 0:
					datetime_str=datetime.datetime.now()

			if "." in datetime_str:
				datetime_obj=datetime.datetime.strptime(datetime_str, '%Y%m%d %H%M%S.%f')
			else:
				datetime_obj=datetime.datetime.strptime(datetime_str, '%Y%m%d %H%M%S')
			datestamp=datetime.datetime.timestamp(datetime_obj)
			acquisitions.append(datestamp)

		if CLUSTER>1:
			if not EXCEPTIONFILE == None:
				exceptionFile=open(EXCEPTIONFILE)
				exceptions=json.load(exceptionFile)
				for key in exceptions:
					twin=exceptions[key]
					twin=twin[0]
					exceptionIndex=None
					correctIndex=None
					for i,j in enumerate(dicomdirs):
						if key in j:
							exceptionIndex=i
						if twin in j:
							correctIndex=i
					if exceptionIndex != None and correctIndex != None:
						acquisitions[exceptionIndex]=acquisitions[correctIndex]
                        
			X=[[x,1] for x in acquisitions]
			Y=np.array(X)
			kmeans = KMeans(n_clusters=CLUSTER, random_state=0).fit(Y)
			labels = kmeans.predict(Y)

			timelabels=[]
			for index,value in enumerate(labels):
				timelabels.append([acquisitions[index],value])

			timelabels.sort()
			sortedlabels=[x[1] for x in timelabels]

			mapping=[]
			for i,v in enumerate(sortedlabels):
				if i==0:
					newvalue=v
					newindex=0
					mapping.append([v, newindex])
				else:
					if v != newvalue:
						newvalue=v
						newindex=newindex+1
						mapping.append([v, newindex])


			sessionlist=[]
			outputlist=[]
			for session in SESSIONS:
				sessionlist.append([])
				dirpath=os.path.join(STAGEDIR,os.path.basename(subject))
				dirpath=os.path.join(dirpath, session)
				outputlist.append(dirpath)

			for index, label in enumerate(labels):
				for map in mapping:
					if map[0]==label:
						newindex=map[1] 
				sessionlist[newindex].append(dicomdirs[index])

		elif CLUSTER == 1:
			newlist=dicomdirs.copy()
			sessionlist=[newlist]
			dirpath=os.path.join(STAGEDIR,os.path.basename(subject))
			dirpath=os.path.join(dirpath, SESSIONS[0])
			outputlist=[dirpath]

		else:
			newlist=dicomdirs.copy()
			sessionlist=[newlist]
			outputlist=[os.path.join(STAGEDIR,os.path.basename(subject))]

		for index, output  in enumerate(outputlist):
			for subdir in sessionlist[index]:
				outpath=os.path.join(output,os.path.basename(subdir))
				logtext(LOGFILE,"copying "+subdir + " to " + outpath)
				copy_tree(subdir,outpath)

	logtext(LOGFILE,"Copying of dicoms for all subjects completed.")

	if bSTAGEONLY:
		logtext(LOGFILE,"Please run BIDSKIT manually later or run this program without --stageonly.")
		sys.exit() 

	if CLUSTER < 2:
		NOSESSIONS="--no-sessions"
	else:
		NOSESSIONS=""

	if bNOANON:
		NOANON="--noanon"
	else:
		NOANON=""

	#adding some "intelligence" - if incremental provided but clearly BIDSKIT hasn't been run then make non-incremental
	if bINCREMENTAL:
		logtext(LOGFILE,"Running BIDSConvert incrementally.")
		SELCONVERT="--selective_convert "
		if not os.path.exists(BIDSKITWORKDIR):
			logtext(LOGFILE,"BIDSKIT doesnt seem to have been run before - disabling incremental run")
			SELCONVERT=""
			bINCREMENTAL=False
	else:
		logtext(LOGFILE,"Running BIDSConvert in a non-incremental fashion. All previous files in work and derivatives directories will be deleted.")
		SELCONVERT=""

	if os.path.exists(ProtocolTranslator):
		copyfile(ProtocolTranslator,BackupProtocolTranslator)
		logtext(LOGFILE,"protocol translator backed up as " + BackupProtocolTranslator)
	elif os.path.exists(origProtocolTranslator):
		copyfile(origProtocolTranslator,BackupProtocolTranslator)
		logtext(LOGFILE,"original protocol translator backed up as " + BackupProtocolTranslator)

	bSTOPCODE=False
	if not os.path.exists(ProtocolTranslator) and BIDSTRANSLATOR == None:
		logtext(LOGFILE,"Cannot find an existing Protocol_translator.json - code will terminate after first pass. Please rerun after Protocol Translator has been provided" )
		bSTOPCODE=True

	if not bCONVERTONLY:
		if not bINCREMENTAL:
			if os.path.exists(BIDSKITROOTDIR):
				logtext(LOGFILE,"Deleting the folder " + BIDSKITROOTDIR )
				rmtree(BIDSKITROOTDIR)
			if os.path.exists(BIDSKITWORKDIR):
				logtext(LOGFILE,"Deleting the folder " + BIDSKITWORKDIR)
				rmtree(BIDSKITWORKDIR)

		logtext(LOGFILE, "Running Bidskit for the first time.")
		#Now run bidskit for the first time
		callstring=("python3 -u {bidskit}/dcm2bids.py -i {dicom} -o {source} {nosessions} --overwrite {selconv} {noanon}").format(bidskit=BIDSKIT, dicom=STAGEDIR,source=OUTPUTDIR, nosessions=NOSESSIONS,noanon=NOANON,selconv=SELCONVERT)
		call(callstring, shell=True)
		logtext(LOGFILE, "protocol translator file created - please edit with new values")
		if not os.path.exists(origProtocolTranslator):
			copyfile(ProtocolTranslator,origProtocolTranslator)
			logtext(LOGFILE,"protocol translator backed up as " + origProtocolTranslator)

	if not os.path.exists(BackupProtocolTranslator):
		if os.path.exists(ProtocolTranslator):
			copyfile(ProtocolTranslator,BackupProtocolTranslator)
			logtext(LOGFILE,"protocol translator backed up as " + BackupProtocolTranslator)
		elif os.path.exists(origProtocolTranslator):
			copyfile(origProtocolTranslator,BackupProtocolTranslator)
			copyfile(origProtocolTranslator,ProtocolTranslator)
			logtext(LOGFILE,"original protocol translator copied to " + BackupProtocolTranslator + " and " + ProtocolTranslator)
		else:
			logtext(LOGFILE, "No existing protocol translatorfound")
			if BIDSTRANSLATOR == None:
				logtext(LOGFILE, "You must supply a protocol_translator.json to convert to bids. Either use the --bidstranslator parameter or manually supply one in ./derivatives/conversion directory")
				sys.exit(0)
				#http://clalance.blogspot.com/2011/01/exiting-python-program.html
				#os._exit(1)
			else:
				copyfile(BIDSTRANSLATOR, BackupProtocolTranslator)
				logtext(LOGFILE, "backing up provided " + BIDSTRANSLATOR + " as " + BackupProtocolTranslator)
	else:
		if not os.path.exists(ProtocolTranslator):
			copyfile(BackupProtocolTranslator, ProtocolTranslator)
			logtext(LOGFILE,"protocol translator recovered from " + BackupProtocolTranslator)

	if BIDSTRANSLATOR != None:
		copyfile(BIDSTRANSLATOR, ProtocolTranslator)
		logtext(LOGFILE, "copying the translator file provided to the bids directory")

	origProt=open(BackupProtocolTranslator)
	origProtJson=json.load(origProt)
	newProt=open(ProtocolTranslator)
	newProtJson=json.load(newProt)

	missingKeys=[]
	newkeys=newProtJson.keys()
	for key in origProtJson:
		if key not in newkeys:
			missingKeys.append(key)

	if len(missingKeys)>0:
		logtext(LOGFILE,"The following keys are missing in your Translator file and may need to be included > " + str(missingKeys))

	logtext(LOGFILE, "The Translator file has been created/copied. Please check all is well and then press enter when ready to do the final conversion")

	if not bNOPROMPT:
		try:
			input("Press enter to continue with second pass of BidsKit")
		except SyntaxError:
			pass
		except EOFError:
			pass

	# run bidskit for second time
	callstring=("python3 -u {bidskit}/dcm2bids.py -i {dicom} -o {source} {nosessions} --overwrite").format(bidskit=BIDSKIT, dicom=STAGEDIR,source=OUTPUTDIR, nosessions=NOSESSIONS)
	call(callstring, shell=True)

	logtext(LOGFILE,"BIDS kit conversion completed - please review error messages and rerun with --convertonly flag if there are any errors.")

	#Check again!
	origProt=open(BackupProtocolTranslator)
	origProtJson=json.load(origProt)
	newProt=open(ProtocolTranslator)
	newProtJson=json.load(newProt)

	missingKeys=[]
	newkeys=newProtJson.keys()
	for key in origProtJson:
		if key not in newkeys:
			missingKeys.append(key)

	if len(missingKeys)>0:
		logtext(LOGFILE,"The following keys are missing in your Translator file and may need to be included > " + str(missingKeys))

	logtext(LOGFILE,FINALERRORS)
	LOGFILE.close()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()
