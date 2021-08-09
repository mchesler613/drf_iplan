import socket
from pathlib import Path
from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE=str(Path(BASE_DIR)) + '/iplan.env'
myvars = dotenv_values(ENV_FILE)

if socket.gethostname() == myvars['LOCAL_HOSTNAME']:
    from iplan_drf.local_settings import *
else:
    from iplan_drf.prod_settings import *
