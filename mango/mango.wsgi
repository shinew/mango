import sys
import os
sys.path.insert(0, "/var/www/mango/mango")

os.chdir("/var/www/mango/mango")
from endpoints import app as application

