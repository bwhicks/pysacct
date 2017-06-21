"""
Models to represent SLURM jobs from sacct in a groovy Pythonic way.
"""
VALID_SACCT_FIELDS = [
    'Account', 'AdminComment', 'AllocCPUS', 'AllocGRES', 'AllocNodes',
    'AllocTRES', 'AssocID', 'AveCPU', 'AveCPUFreq', 'AveDiskRead',
    'AveDiskWrite', 'AvePages', 'AveRSS', 'AveVMSize', 'BlockID', 'Cluster',
    'Comment', 'ConsumedEnergy', 'ConsumedEnergyRaw', 'CPUTime', 'CPUTimeRAW',
    'DerivedExitCode', 'Elapsed', 'ElapsedRaw', 'Eligible', 'End', 'ExitCode',
    'GID', 'Group', 'JobID', 'JobIDRaw', 'JobName', 'Layout', 'MaxDiskRead',
    'MaxDiskReadNode', 'MaxDiskReadTask', 'MaxDiskWrite', 'MaxDiskWriteNode',
    'MaxDiskWriteTask', 'MaxPages', 'MaxPagesNode', 'MaxPagesTask', 'MaxRSS',
    'MaxRSSNode', 'MaxRSSTask', 'MaxVMSize', 'MaxVMSizeNode', 'MaxVMSizeTask',
    'MinCPU', 'MinCPUNode', 'MinCPUTask', 'NCPUS', 'NNodes', 'NodeList',
    'NTasks', 'Priority', 'Partition', 'QOS', 'QOSRAW', 'ReqCPUFreq',
    'ReqCPUFreqMin', 'ReqCPUFreqMax', 'ReqCPUFreqGov', 'ReqCPUS',
    'ReqGRES', 'ReqMem', 'ReqNodes', 'ReqTRES', 'Reservation',
    'ReservationId', 'Reserved', 'ResvCPU', 'ResvCPURAW', 'Start', 'State',
    'Submit', 'Suspended', 'SystemCPU', 'Timelimit', 'TotalCPU', 'UID', 'User',
    'UserCPU', 'WCKey', 'WCKeyID'
]


class Step(object):
    """An object presentation of a single sacct line which requires
    kwargs or a dict following the same format as `sacct -P`"""

    def __init__(self, sacct_line=None, **kwargs):

        for key, value in kwargs.items():
            if key.lower() not in (field.lower() for field in
                                   VALID_SACCT_FIELDS):
                raise ValueError(
                    (
                        '%s is not a valid field. Please choose from:\n'
                        '%s' % (key, ', '.join(VALID_SACCT_FIELDS))
                    )
                )
            setattr(self, key.lower(), value)

    def __repr__(self):
        return '<Step: %s>' % self.jobid


class Job(object):

    def __init__(self, step):
        if not isinstance(step, Step):
            raise TypeError('Job must be initialized from Step object')

        for k, v in step.__dict__.items():
            setattr(self, k, v)

    def __repr__(self):
        return '<Job: %s>' % self.jobid

    @property
    def jobsteps(self):
        return self._jobsteps

    @jobsteps.setter
    def jobsteps(self, value):
        if not isinstance(value, list):
            raise TypeError("jobsteps must be of type list")
        for item in value:
            if not isinstance(item, Step):
                raise ValueError('%s is not a Step object' % item)
            if (item.jobid).split('.')[0] != self.jobid:
                raise ValueError('jobstep must match the jobid of the associated job')

        self._jobsteps = value

    @jobsteps.deleter
    def jobsteps(self):
        del self._jobsteps
