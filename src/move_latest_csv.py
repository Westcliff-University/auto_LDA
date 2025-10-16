
from platform import platform
import glob
import os
import getpass
from contextlib import chdir 
from datetime import datetime, timedelta

def move_latest_csv(destination, from_path = f'/Users/{getpass.getuser()}/Downloads/'):
    """
    Provide the absolute destination.
    """
    dl_path = os.path.abspath(from_path)
    os.makedirs(destination, exist_ok = True)

    if 'Window' in platform():
        new_dir = os.getcwd() + "\\" + destination
    else:
        new_dir = os.getcwd() + "/" + destination

    with chdir(dl_path):

        list_of_files = glob.glob("*_separated*.csv")

        latest_file = max(list_of_files, key = os.path.getmtime)
        # latest_file.rfind('/')
        # There is an extra second of minute at the end because the GAP
        # reports are named identically if they're downloaded from the same
        # source within the same minute
        if 'Window' in platform():
            os.rename(latest_file, os.path.abspath(new_dir + latest_file[latest_file.rfind('/'):-4] + "\\" + datetime.today().strftime('%y%m%d%H%M%S') + '.csv'))
        else:
            os.rename(latest_file, os.path.abspath(new_dir + latest_file[latest_file.rfind('/'):-4] + datetime.today().strftime('%Y%M%D%H%M%S') + '.csv'))