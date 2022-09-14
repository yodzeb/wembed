#!/var/www/txt/wembed/venv/bin/python3

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/txt/wembed/www/cgi/')
print ("starting")
from hello import app as application
