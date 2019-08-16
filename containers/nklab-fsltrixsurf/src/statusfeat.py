#!/usr/bin/env python
#Code to run FSL feat 1st analysis
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
#from builtins import *

import os
import glob
import subprocess
import argparse
from datetime import datetime
import pickle


def retrieveStatus(the_filename):
	with open(the_filename, 'rb') as f:
		try:
			jobstat = pickle.load(f)
			return jobstat
		except EOFError as e:
			return {}

def printStatus(workdir=None, statusfile=None):
    jobstat={}
    queue=[]
    runs=[]
    done=[]
    errors=[]
    info=[datetime.now().isoformat(),'Not Done' ]
    if workdir == None:
        workdir=os.getcwd()
    if statusfile==None:
    	statusfile=os.path.join(workdir,'jobstatus.cf')
    else:
		statusfile=os.path.join(workdir,statusfile)
    if os.path.exists(statusfile):
	    jobstat = retrieveStatus(statusfile)
	    if len(jobstat) > 0:
	        print('job stats....\n')
	        queue = jobstat['queue']
	        done = jobstat['done']
	        runs = jobstat['runs']
	        errors = jobstat['errors']
	        info = jobstat['info']
	        print('Job started:' + info[0] + ' and ended: ' + info[1])
	        print('------------------------------------------\n')
	        if len(runs)> 0:
	            print('There are ' + str(len(runs)) + ' jobs running.')
	            for job in runs:
	    	        print('\njobid: '+ str(job[0]) + '\nlocation: ' + job[1])  
	        else:
	    	    print('There are no jobs currently running.')
	        print('........................................\n')
	        if len(queue)> 0:
	            print('There are '+ str(len(queue)) + ' jobs left to complete. These are:')
	            for job in queue:
	    	        print('\njobid: '+ str(job[0]) + '\nlocation: ' + job[1])        
	        else:
	    	    print('There are no jobs left to complete.')
	        print('........................................\n')
	        if len(done)> 0:
	            print('There are '+ str(len(done)) + ' jobs that have successfully completed. These are:')
	            for job in done:
	    	        print('\njobid: '+ str(job[0]) + '\nlocation: ' + job[1])        
	    	        print('started: '+ job[5] + ' ended: ' + job[6])
	        else:
	    	    print('No jobs have successfully completed yet.')
	        print('........................................\n')
	        if len(errors)> 0:
	            print('There are '+ str(len(errors)) + ' jobs that have completed with errors. These are:')
	            for job in errors:
	    	        print('\njobid: '+ str(job[0]) + '\nlocation: ' + job[1])        
	    	        print('started: '+ job[5] + ' ended: ' + job[6])
	        else:
	    	    print('No jobs have completed with errors.')
	    else:
		    print('No jobs are currently running.')
    else:
	    print('No jobs are currently running.')


if __name__ == '__main__':	    
	#Parse arguments
	parser = argparse.ArgumentParser(description="Setup all parameters for feat analysis.")
	parser.add_argument("--workdir",help="the top level directory.")
	parser.add_argument("--statusfile",help="the status file to use.")
	args=parser.parse_args()

	if args.workdir:
		workdir=os.path.abspath(args.workdir)
	else:
		workdir=os.getcwd()

	if args.statusfile:
		statusfile=os.path.join(workdir,args.statusfile)
	else:
		statusfile=os.path.join(workdir,'jobstatus.cf')

	printStatus(workdir, statusfile)








