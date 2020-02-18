import os
import shutil

root_pwd = os.getcwd()
s_path = root_pwd + '/data/'
d_path = root_pwd + '/result/'
if os.path.isdir(s_path):
    for files in os.listdir(s_path):
        try:
            os.mkdir(path + 'result/')
        except:
            pass
        if os.path.isfile(s_path + files):
            shutil.copyfile(s_path + files, d_path + files)
