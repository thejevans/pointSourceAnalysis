#!/bin/sh

###########################################################
# This is a bash script that write a dag, which defines
# your jobs with a submit file, and any arguments (i.e.
# your python script, I/O files, and/or any arguments that
# you would have passed when running your python scripts
# locally). Note that this file simplies 'write', you don't
# have to use bash at all; python works as well. (I just
# wanted to force myself to learn another language)
#
# To run this script:
# $ ./builddag.sh > my_dag.dag
#
# Regardless of how you generate the output, the dag,
# my_dag.dag, is the dagman file that you will submit.
# Each job in this my_dag.dag is defined by the keyword
# "JOB" followed by an unique job id and the submit file:
#
# JOB job_id submit.sub
#
# Often, your python scripts take arguments. To change
# the arguments for each of jobs, you can use the "VARS"
# keyword:
#
# VARS $job_id job_name=\"$job_name\" infile=\"$infile\"
#
# NOTE:: MAKE SURE NONE OF THE PATHS HERE POINTS TO I3HOME
#        EITHER /data/condor_build/ OR /data/i3store0/ OR
#        /data/i3scratch0/
#
# After you have the dag file (my_dag.dag), you can submit
# your jobs via:
#
# $ condor_submit_dag -config dagman.config my_dag.dag
#
# dagmain.config is where you can set the max jobs per
# time, number of jobs per interval, etc.
############################################################

##################################################################
#### recall my command line:
#### python dumb.py --outfile <string> -nsteps <int>
####                --coeff <float> --sleep <float> --verbose
##################################################################

jobbase='ang_res_vs_bin_size'
script="/data/i3store0/users/jevans96/point_source_analysis/scripts/March2018/plot_ang_res_vs_bin_size.py"
maindir="/data/i3store0/users/jevans96/point_source_analysis/distributed_outputs/data_March2018/"
stdargs="/data/i3store0/users/jevans96/point_source_analysis/converted_point_source_data/SplineMPEmax.MuEx.MC.npy /data/i3store0/users/jevans96/point_source_analysis/converted_point_source_data/Data.2015.29652698sec.npy"

### seq <min> <stepsize> <max>
for a in `seq 0.25 0.05 3.5`; do
    for b in `seq 1.5 0.5 3.0`; do
        outfile="${maindir}bin_${a}_index_${b}.pkl"
        command="python ${script} ${outfile} ${stdargs} ${a} ${b}"
        jobname=$jobbase.$a.$b
        JOBID=$jobbase.$a.$b
        echo JOB $JOBID /data/i3store0/users/jevans96/point_source_analysis/scripts/March2018/dagman/submit.sub
        echo VARS $JOBID JOBNAME=\"$jobname\" command=\"$command\"
    done
done
