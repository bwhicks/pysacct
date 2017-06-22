'''
Settings module for pysacct.

These provide defaults, look for a `overrides.py` specified by either an
environment variable or in the working dir from which pysacct is invoked, and
finally override based on environment variables.
'''
import os

# Fields that sacct may produce -- amend as necessary if you have anything
# custom
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

# Get the current working path and lookfor an overrides.py
filepath = os.path.join(os.getcwd(), 'overrides.py')
# Override if the environmental var exists
filepath = getattr(os.environ, 'PYSACCT_OVERRIDES', filepath)
if os.path.exists(filepath):
    import imp
    import sys
    module_name = "pysacct.overrides"
    module = imp.new_module(module_name)
    module.__file__ = filepath
    sys.modules[module_name] = module
    exec(open(filepath, "rb").read())
