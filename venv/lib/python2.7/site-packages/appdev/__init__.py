import os
for module in os.listdir(os.path.dirname(__file__)):
  if module == '__init__.py' or module[-3:] != '.py':
    continue
  __import__(module[:-3], locals(), globals())
del module # pylint: disable=W0631

__version__ = '0.0.1'
__all__ = []
USER_AGENT = 'AppDev Core Modules %s' % __version__
