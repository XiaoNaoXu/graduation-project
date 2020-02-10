import os, tarfile

def tar_file(tar_name, filecode, pluginname):
    savepath = os.getcwd()
    tar_path = '/static/file/' + pluginname + '/' + filecode + '/'
    os.chdir(savepath + tar_path)
    with tarfile.open(tar_name, "w:gz") as tar:
        tar.add('data/' , arcname=os.path.basename('data/'))
    os.chdir(savepath)

def un_tar(file_name, file_path):
    tar = tarfile.open(file_name)
    names = tar.getnames()
    for name in names: 
        tar.extract(name, path = file_path)
    tar.close()