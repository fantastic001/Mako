from distutils.core import setup
setup(
  name = 'mako',
  packages = ['mako', 'mako.lib', "mako.lib.schedule", "mako.lib.ams", "mako.lib.ams.actions", "mako.lib.reporting", "mako.lib.reporting.month", "mako.lib.reporting.quarter", "mako.lib.database", "mako.desktop", "mako.lib.table"], # this must be the same as the name above
  version = '0.2.1',
  description = 'Mako is a tool for organizing your projects, schedules, events and to help you live more agile life.',
  author = 'Stefan Nožinić',
  author_email = 'stefan@lugons.org',
  url = 'https://github.com/fantastic001/Mako', # use the URL to the github repo
  download_url = 'https://github.com/fantastic001/Mako/tarball/0.2',
  keywords = ['agile', 'schedules', 'projects', 'organization'], 
  package_dir = {'mako': 'src/'},
  classifiers = [],
  scripts = ["bin/mako"],
  install_requires=["ArgumentStack", "YAPyOrg"] # dependencies listed here 
)
