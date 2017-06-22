pysacct
=======

This is a small Python module with a simple aim: read the output of SLURM's
``sacct`` command with the ``-P`` setting for piped output.

Description
-----------
Eventually, this module should include (among other things) an actual command
to call ``sacct`` and import the output of the log as Python objects.

Right now, there is a model for each line of ``sacct`` that can store jobsteps
in a list on its ``jobsteps`` property, provided they have matching JobIDs
up to the period.

There are also unit tests of the current functionality

Installation
------------
For now, the easiest solution is to ``git clone`` the repository and use the
models as you see fit. ``settings.py`` will look for any overrides to the
``VALID_SACCT_FIELDS`` setting in ``overrides.py`` in your working directory
or another path specified by the ``PYSACCT_OVERRIDES`` environmental variable

Testing
-------
The unit tests, such as they are with such a minimal framework, can be run
after ``pip install -r dev-requirements.txt`` by simply typing ``pytest`` from
the repository route (or ``python -m pytest`` if for some reason your install of
Python doesn't add ``pytest`` to your ``PATH`` variable.)

Goals
-----
The eventual aim of this utility is two-fold. First, to provide the routines to
call ``sacct``, get the reports on jobs run, then convert them to organized
Python objects that can be transformed into dictionaries or JSON as a data exchange
format that is more flexible than a CSV or text dump.

Second, to provide a utility that will do all of these things in such a way that
integrating its output with an optional external database will be pratical.
