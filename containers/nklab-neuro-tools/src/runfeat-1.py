#!/usr/bin/env python
#Code to run FSL feat 1st analysis
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
#from builtins import *

import os
import shutil
import glob
import subprocess
import argparse
from datetime import datetime
import pickle
import statusfeat as statfeat


def retrieveStatus(the_filename):
	with open(the_filename, 'rb') as f:
		try:
			jobstat = pickle.load(f)
			return jobstat
		except EOFError as e:
			return {}
	    

def saveStatus(jobstat, statusfile):
	with open(statusfile, 'wb') as f:
		pickle.dump(jobstat, f)

#Parse arguments
parser = argparse.ArgumentParser(description="Setup all parameters for feat analysis.")
parser.add_argument("--workdir",help="the top level directory.")
parser.add_argument("--design",help="design directory.")
parser.add_argument("--designfile",help="design fsf to run.")
parser.add_argument("--funcdir",help="top level directory that contains subject func data.")
parser.add_argument("--roidir",help="top level directory that contains subject roi regions.")
parser.add_argument("--evdir",help="top level directory where roi time series will be extracted to.")
parser.add_argument("--resultsdir",help="top level directory that contains subject results.")
parser.add_argument("--subid",help="subjects to analyse")
parser.add_argument("--batchsize",help="maximum number of jobs to run in batch")
parser.add_argument("--regen",help="regenerate evs and design files")
parser.add_argument("--rerun",help="on HPC restart jobs marked as running")
args=parser.parse_args()

if args.workdir:
	workdir=os.path.abspath(args.workdir)
else:
	workdir=os.getcwd()

if args.evdir:
	evdir=os.path.abspath(args.evdir)
else:
	evdir=os.path.join(workdir,'evs')
if not os.path.exists(evdir):
	os.makedirs(evdir)

if args.resultsdir:
	resultsdir=os.path.abspath(args.resultsdir)
else:
	resultsdir=os.path.join(workdir,'results')
if not os.path.exists(resultsdir):
	os.makedirs(resultsdir)

if args.design:
	designdir=os.path.abspath(args.design)
else:
	designdir=os.path.join(workdir,'designs')

if args.designfile:
	designfile=os.path.join(designdir, args.designfile)
else:
	designfile= os.path.join(designdir,'seed_design.fsf')

if args.funcdir:
	topfuncdir=os.path.abspath(args.funcdir)
else:
	topfuncdir=os.path.join(workdir,'func')

if args.roidir:
	toproidir=os.path.abspath(args.roidir)
else:
	toproidir=os.path.join(workdir,'roi')

if args.subid:
	subid=args.funcdir.subid.split(':')
else:
	subid=[]

if args.batchsize:
	maxjobs=int(args.batchsize)
else:
	maxjobs=4

if args.regen:
	regen='Y'
else:
	regen='N'

if args.rerun:
	rerun='Y'
else:
	rerun='N'

#testing so for now use just one sub-id
#subid="sub-01"

#get all functional files for a subject sub-id
#shellCommandList=["ls", "-R", topfuncdir+'/'+subid]
#files = subprocess.check_output(shellCommandList)
#funcfilelist = files.split('\n')
#funcfiles = [s for s in funcfilelist if '.nii' in s] 

#get all functional files for a subject sub-id
shellCommandList=["ls",  topfuncdir]
files = subprocess.check_output(shellCommandList)
funcfilelist = files.split('\n')
funcfiles = [s for s in funcfilelist if '.nii' in s] 

#get all rois for a subject sub-id
#shellCommandList=["ls", "-R", toproidir+'/'+subid]
#files = subprocess.check_output(shellCommandList)
#roifilelist = files.split('\n')
#roifiles = [s for s in roifilelist if '.nii' in s]

shellCommandList=["ls",  toproidir]
files = subprocess.check_output(shellCommandList)
roifilelist = files.split('\n')
roifiles = [s for s in roifilelist if '.nii' in s]

#for each subject 
#subevdir = os.path.join(evdir,subid)
#subresults=os.path.join(resultsdir,subid)
#subdesign=os.path.join(designdir,subid)
subevdir = evdir
subresults=resultsdir
subdesign=designdir

jobstat={}
queue=[]
runs=[]
done=[]
errors=[]
info=[datetime.now().isoformat(),'Not Done' ]
jobid=0
statusChange=False

statusfile=os.path.join(workdir,'jobstatus.cf')
if os.path.exists(statusfile):
	jobstat = retrieveStatus(statusfile)
	if len(jobstat) > 0:
	    print('Continuing....')
	    statfeat.printStatus(None, None)
	    queue = jobstat['queue']
	    done = jobstat['done']
	    runs = jobstat['runs']
	    info = jobstat['info']
	    errors = jobstat['errors']
	    if len(runs)>0 and rerun=="Y":
	    	print("\njobs that were previously running will be added to queue to run again.\n")
	    	queue = queue + runs
	    	statusChange=True
	    	for job in runs:
	    		try:
	    		    shutil.rmtree(job[1])
	    		except OSError as e:
	    			pass
	    	runs=[]
	    if len(errors) > 0:
	    	print("\nretrying jobs that completed with errors\n")
	    	queue = queue + errors
	    	statusChange=True
	    	for job in errors:
	    		try:
	    		    shutil.rmtree(job[1])
	    		except OSError as e:
	    			pass
	    	errors = []
	        
	    #create snapshot of jobs
if statusChange:
	#create snapshot of jobs
	jobstat['queue']=queue
	jobstat['done']=done
	jobstat['runs']=runs
	jobstat['errors']=errors
	jobstat['info']=info
	saveStatus(jobstat, statusfile)
	statusChange=False
	statfeat.printStatus(None)


if len(queue)==0:
    for inputfile in funcfiles:
	    #get unique prefix for each funcfile!
	    subels=inputfile.split('_')
	    prefix=subels[0] #hard code for now
	    #prefix=subid+'-'+subels[0] #hard code for now

	    #inputfile=os.path.join(topfuncdir,subels[1]+'/'+subels[2]+'/'+subels[3]+'/'+subels[4] + '/' +subels[5] + '/'+subels[6] + '/'+ inputfile) #hard code for now
	    inputfile=os.path.join(topfuncdir, inputfile) #hard code for now

	    if not os.path.exists(subevdir):
		    os.makedirs(subevdir)
	    if not os.path.exists(subresults):
		    os.makedirs(subresults)
	    if not os.path.exists(subdesign):
		    os.makedirs(subdesign)
	    for roifile in roifiles:
		    roisuffix=roifile.split('.')[0]
		    evfile=os.path.join(subevdir,roisuffix+'_' +prefix + '_ts.txt')
		    featresults=os.path.join(subresults,roisuffix +'_' +prefix)
		    subdesignfile=os.path.join(subdesign,roisuffix+'_' +prefix + '.fsf')
		    #roifile=os.path.join(toproidir,'sub-01'+'/'+roifile)
		    roifile=os.path.join(toproidir,roifile)
		    if not os.path.exists(evfile) or regen=='Y':
			   thisprocstr = str("fslmeants -i " + inputfile + " -o " + evfile + " -m " + roifile)
			   subprocess.Popen(thisprocstr,shell=True).wait()
		    if not os.path.exists(subdesignfile) or regen=='Y':
			   thisprocstr = str("cp " + designfile + " " + subdesignfile)
			   subprocess.Popen(thisprocstr,shell=True).wait()

			   thisprocstr = "sed -i 's#<<outputdir>>#" + featresults + "#g' " + subdesignfile
			   subprocess.Popen(thisprocstr,shell=True).wait()

			   thisprocstr = "sed -i 's#<<inputfile>>#"+inputfile +"#g' " + subdesignfile
			   subprocess.Popen(thisprocstr,shell=True).wait()

			   thisprocstr = "sed -i 's#<<evfile>>#"+ evfile +"#g' "+ subdesignfile
			   subprocess.Popen(thisprocstr,shell=True).wait()

		    jobid=jobid+1
		    queue.append([jobid,featresults+'.feat', inputfile, evfile, subdesignfile, 'Not Started', 'Not Done'])


todo = len(queue)
finished = len(done)
running = len(runs)
errored = len(errors)
initnumjobs = todo+finished+errored+running
statusChange=True

#create snapshot of jobs
if statusChange:
	#create snapshot of jobs
	jobstat['queue']=queue
	jobstat['done']=done
	jobstat['runs']=runs
	jobstat['errors']=errors
	jobstat['info']=info
	saveStatus(jobstat, statusfile)
	statusChange=False

while (finished + errored ) < initnumjobs:

	if maxjobs > running and len(queue)>0:
		#start a new job
		newjob=queue[0]
		queue.remove(newjob)
		newjob[5]=datetime.now().isoformat()
		runs.append(newjob)
		thisprocstr = "feat " + newjob[4] + " &"
		subprocess.Popen(thisprocstr,shell=True).wait()
		statusChange=True

	#create snapshot of job
	if statusChange:
			#create snapshot of jobs
	    jobstat['queue']=queue
	    jobstat['done']=done
	    jobstat['runs']=runs
	    jobstat['errors']=errors
	    jobstat['info']=info
	    saveStatus(jobstat, statusfile)
	    statusChange=False

	#check running jobs to see if job is complete, if it is then
	#reduce running
	#update complete
	for job in runs:
		featdirresults=os.path.join(job[1],'report.html')
		logerrresults=os.path.join(job[1],'logs/*.e[0-9]*')
		finishtext=[]
		errortext=[]
		if os.path.exists(featdirresults):
		    with open(featdirresults, 'r') as f:
			    filetext = f.readlines()
			    finishtext=[s for s in filetext if "Finished" in s]
			    errortext = [s for s in filetext if "<font color=red>Error" in s]
		logerrors=glob.glob(logerrresults)
		featError=False
		for loge in logerrors:
			with open(loge, 'r') as fe:
				errtext = fe.readlines()
				if len(errtext) > 0:
					#we have errors
					featError=True
					break
		#possible to get error in feat1 or maybe feat1
		feat1errtext=[]
		feat1=os.path.join(job[1],'logs/feat1')
		if os.path.exists(feat1):
			with open(feat1, 'r') as f:
				filetext = f.readlines()
				feat1errtext=[s for s in filetext if "ERROR MESSAGE:" in s]
		if len(feat1errtext)>0:
			featError=True
		feat1aerrtext=[]
		feat1a=os.path.join(job[1],'logs/feat1a_init')
		if os.path.exists(feat1a):
			with open(feat1a, 'r') as f:
				filetext = f.readlines()
				feat1aerrtext=[s for s in filetext if "ERROR MESSAGE:" in s]
		if len(feat1aerrtext)>0:
			featError=True
		if len(finishtext)==1 and not featError and len(errortext)==0:
			#job completed
			runs.remove(job)
			job[6]=datetime.now().isoformat()
			done.append(job)
			statusChange=True
			
		elif featError:
			#job errored out
			runs.remove(job)
			job[6]=datetime.now().isoformat()
			errors.append(job)
			statusChange=True

			
	todo = len(queue)
	finished = len(done)
	running = len(runs)
	errored = len(errors)

	#create snapshot of job
	if statusChange:
			#create snapshot of jobs
	    jobstat['queue']=queue
	    jobstat['done']=done
	    jobstat['runs']=runs
	    jobstat['errors']=errors
	    jobstat['info']=info
	    saveStatus(jobstat, statusfile)
	    statusChange=False

#job completed
#archive jobstatus.cf
info[1]=datetime.now().isoformat()
jobstat['info']=info
saveStatus(jobstat, statusfile)
suffix=str(datetime.now().isoformat())
thisprocstr = "mv " + statusfile + " " + statusfile + '.' + suffix
subprocess.Popen(thisprocstr,shell=True).wait()
