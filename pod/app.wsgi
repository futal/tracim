APP_CONFIG = "/home/daccorsi/sources/pod/pod/development.ini"

#Setup logging
import logging
# logging.config.fileConfig(APP_CONFIG)

#Load the application
from paste.deploy import loadapp
application = loadapp('config:%s' % APP_CONFIG)
application.debug = True

