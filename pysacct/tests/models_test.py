from unittest import TestCase
from pysacct.models import Job, VALID_SACCT_FIELDS


class TestJob(TestCase):

    def test_init(self):
        # Making a job with default settings should work
        job = Job(jobid='123')
        assert isinstance(job, Job)

        # Making one with a field not supported by sacct shouldn't
        with self.assertRaises(ValueError) as context:
            job = Job(jobid='123', foo='bar')
        assert 'foo is not a valid field.' in str(context.exception)
        assert ', '.join(VALID_SACCT_FIELDS) in str(context.exception)

    def test_getattr(self):
        job = Job(jobid='123')
        # Nor should adding one
        with self.assertRaises(ValueError) as context:
            job.foo
        assert 'foo is not a valid field' in str(context.exception)

    def test_repr(self):
        job = Job(jobid='123', user='bhicks')
        job_str = repr(job)
        assert '<Job:' in job_str
        assert '>' in job_str
        assert "'user': 'bhicks'" in job_str
        assert "'jobid': 123" in job_str

    def test_str(self):
        job = Job(jobid='123', user='bhicks')
        assert str(job) == "<Job: {'jobid': 123}>"

    def test_jobid(self):
        job = Job(jobid='123')
        # Should be an int because it can be converted
        assert isinstance(job.jobid, int)
        # Should remain a str because it can't be
        job = Job(jobid='123.batch')
        assert isinstance(job.jobid, str)

        # Delete works as expected
        delattr(job, 'jobid')
        # Technically the attribute exists but will always return None
        assert not job.jobid

    def test_jobsteps(self):
        # A job and its step with the same jobid before . can be matched
        job = Job(jobid='123')
        job_step = Job(jobid='123.batch')
        job.jobsteps = [job_step]
        assert job.jobsteps == [job_step]

        # Adding anything other than a list should result in a type error
        with self.assertRaises(TypeError) as context:
            job.jobsteps = ''
        assert 'Jobsteps must be of type list' in str(context.exception)

        # Adding a list with non Job objects should produce a TypeError
        with self.assertRaises(TypeError) as context:
            job.jobsteps = ['foo', 'bar']
        assert 'foo is not a Job object' in str(context.exception)

        # Adding a job that doesn't have the same JobID should fail
        with self.assertRaises(ValueError) as context:
            job.jobsteps = [Job(jobid='456')]
        assert 'Job and jobstep must match on JobID' in str(context.exception)
