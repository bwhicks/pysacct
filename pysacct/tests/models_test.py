from unittest import TestCase
from pysacct.models import Job, Step, VALID_SACCT_FIELDS


class TestStep(TestCase):

    def testrepr(self):
        step = Step(jobid='123')
        assert repr(step) == '<Step: 123>'

    def test_validation(self):
        with self.assertRaises(ValueError) as context:
            Step(foo='123')
        assert('foo is not a valid field' in str(context.exception))
        assert(', '.join(VALID_SACCT_FIELDS) in str(context.exception))


class TestJob(TestCase):

    def testrepr(self):
        step = Step(jobid='123')
        job = Job(step)
        assert repr(job) == '<Job: 123>'

    def test_validation(self):
        # Should raise an error because it is not value Step
        with self.assertRaises(TypeError) as context:
            Job('123')
        assert ('Job must be initialized from Step object'
                in str(context.exception))
