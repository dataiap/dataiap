"""
Runs a dummy job.

export AWS_ACCESS_KEY_ID=''
export AWS_SECRET_ACCESS_KEY=''
python mapreduce.py  --num-ec2-instances 1 -r emr -o 's3://dataiap.mit.edu.mroutput/UNIQUEFILENAME' --no-output 's3://dataiap.mit.edu.ap/World*'

# preallocate a bunch of instances by running a dummy workflow and not
# terminating it
python mrjob/tools/emr/create_job_flow.py --num-ec2-instances=12
# example jobid: j-3PL7GKD4ADK9K

# add a job to the flow
python mr_my_job.py -r emr --emr-job-flow-id=j-JOBFLOWID input_file.txt > out

# run other jobs if it's a multi-job process...
# it's nice because each job is blocks until it finishes
# so you don't need to sit and babysit

# terminate the job flows or we will lose money!
python -m mrjob.tools.emr.terminate_job_flow.py [options] j-JOBFLOWID



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
