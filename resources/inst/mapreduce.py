"""
#
# Runs a dummy job.
# see inst/s3.py for a script to interact with s3 buckets
#

# make sure mrjob has been installed

export AWS_ACCESS_KEY_ID=''
export AWS_SECRET_ACCESS_KEY=''

# It is possible to chain multiple mapreduces together on the commandline because each one blocks until it completes :)
python mapreduce.py  --num-ec2-instances 1 -r emr -o 's3://dataiap.mit.edu.mroutput/UNIQUEFILENAME' --no-output 's3://dataiap.mit.edu.ap/World*'

# note: -o should be an output folder
# note: --no-output means don't stream back to terminal
# note: a multi-step mapreduce means each step takes ONLY the output of the previous step as the input
#       see mrjob/emr.py:1531-1546



# preallocate 12 instances by running a dummy workflow and not terminating it
python mrjob/tools/emr/create_job_flow.py --num-ec2-instances=12
# example jobid: j-3PL7GKD4ADK9K

# add a job to the flow
python mr_my_job.py -r emr --emr-job-flow-id=j-JOBFLOWID input_file.txt > out

# run other jobs if it's a multi-job process...
# it's nice because each job is blocks until it finishes
# so you don't need to sit and babysit

# terminate the job flows or we will lose money!
python -m mrjob.tools.emr.terminate_job_flow.py [options] j-JOBFLOWID

# see what job flows are running, etc.
python -m mrjob.tools.emr.audit_usage

"""


from mrjob.job import MRJob
import re

WORD_RE = re.compile(r"[\w']+")

# if YIELD_ALL is true, we yield all densities, otherwise,
# we yield just the extremes

class  MRTest(MRJob):
    """ A  map-reduce job that calculates the density """

    def mapper(self, _, line):
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield (word, sum(counts))



if __name__ == '__main__':
    MRTest.run()
