import os
from pysacct import settings
from unittest import TestCase

# Py2/3 compatibility
try:
    from imp import reload
except ImportError:
    pass


class TestSettings(TestCase):
    def test_override(self):
        # Make a temporary override file
        path = os.path.join(os.getcwd(), 'overrides.py')
        with open(path, 'w') as file:
            file.write('DERP = ["FOO", "BAR"]')
        # DERP should now be in the settings module on reload
        reload(settings)
        assert settings.DERP == ["FOO", "BAR"]

        # Delete the file to tidy up
        os.remove(path)
        assert not os.path.exists(path)
