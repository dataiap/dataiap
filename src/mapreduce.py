"""
Runs a dummy job.

export AWS_ACCESS_KEY_ID=''
export AWS_SECRET_ACCESS_KEY=''
python mapreduce.py  --num-ec2-instances 1 -r emr 's3://dataiap.mit.edu.ap/World*' > output.dat

# preallocate a bunch of instances by running a dummy workflow and not
# terminating it
python mrjob/tools/emr/create_job_flow.py --num-ec2-instances=12

# add a job to the flow
python mr_my_job.py -r emr --emr-job-flow-id=j-JOBFLOWID input_file.txt > out


# terminate the job flows or we will lose money!
python -m mrjob.tools.emr.terminate_job_flow.py [options] j-JOBFLOWID



"""


from mrjob.job import MRJob

# if YIELD_ALL is true, we yield all densities, otherwise,
# we yield just the extremes

class  MRTest(MRJob):
    """ A  map-reduce job that calculates the density """

    def mapper(self, _, line):
        yield '1', line

if __name__ == '__main__':
    MRTest.run()
