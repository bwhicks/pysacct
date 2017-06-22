"""
Models to represent SLURM jobs from sacct in a groovy Pythonic way.
"""
import json
from pysacct.settings import VALID_SACCT_FIELDS


def validate_fields(obj, **kwargs):
    for key, value in kwargs.items():
        if key.lower() not in (field.lower() for field in
                               VALID_SACCT_FIELDS):
            raise ValueError(
                (
                    '%s is not a valid field. Please choose from:\n'
                    '%s' % (key, ', '.join(VALID_SACCT_FIELDS))
                )
            )
        setattr(obj, key.lower(), value)


'''
class Step(object):
    """An object presentation of a single sacct line which requires
    kwargs following the same format as `sacct -P`"""

    def __init__(self, **kwargs):
        validate_fields(self, **kwargs)

    def __repr__(self):
        return '<Step: %s>' % self.jobid

    def __str__(self):
        return '<Step: %s>' % self.jobid

    def to_JSON(self):
        return json.dumps(self.__dict__)

'''


class Job(object):
    """
    Object representation of a SLURM job, with any steps as `Job.jobsteps`.
    Can be created from kwargs or dict passed as kwargs.
    """

    def __init__(self, **kwargs):
        validate_fields(self, **kwargs)

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key.strip('_'), value

    def __repr__(self):
        return '<Job: %s>' % dict(self)

    def __str__(self):
        return "<Job: {'jobid': %s}>" % self.jobid

    # Fall back for a valid field that is empty
    def __getattr__(self, name):
        if name.lower().strip('_') in (field.lower() for field in
                   VALID_SACCT_FIELDS):
            return None
        raise ValueError('%s is not a valid field for a Job object' % name)

    @property
    def jobid(self):
        return self._jobid

    @jobid.setter
    def jobid(self, value):
        try:
            self._jobid = int(value)
        except ValueError:
            self._jobid = value

    @jobid.deleter
    def jobid(self):
        delattr(self, '_jobid')

    @property
    def jobsteps(self):
        return self._jobsteps

    @jobsteps.setter
    def jobsteps(self, value):
        if not isinstance(value, list):
            raise TypeError("Jobsteps must be of type list")
        for item in value:
            if not isinstance(item, Job):
                raise TypeError('%s is not a Job object' % item)
            if (str(item.jobid)).split('.')[0] != str(self.jobid):
                raise ValueError('Job and jobstep must match on JobID')

        self._jobsteps = value

    @jobsteps.deleter
    def jobsteps(self):
        del self._jobsteps

    def to_JSON(self):
        jobsteps = []
        if self.jobsteps:
            jobsteps = [dict(step) for step in self.jobsteps]
            delattr(self, 'jobsteps')

        job_dict = dict(self)
        job_dict['jobsteps'] = jobsteps
        return json.dumps(job_dict)
