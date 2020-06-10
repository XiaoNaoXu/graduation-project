import os, tarfile, gzip, rarfile, zipfile
from subprocess import check_call

def tar_file(tar_name, filecode, pluginname):
    savepath = os.getcwd()
    tar_path = '/static/file/' + pluginname + '/' + filecode + '/'
    os.chdir(savepath + tar_path)
    with tarfile.open(tar_name, "w:gz") as tar:
        tar.add('data/' , arcname=os.path.basename('data/'))
    os.chdir(savepath)

def un_tar(file_name, file_path):
    print(file_name, file_path)
    tar = tarfile.open(file_name)
    names = tar.getnames()
    for name in names: 
        tar.extract(name, path = file_path)
    tar.close()

def un_zip(file_name, file_path):
    zip_file = zipfile.ZipFile(file_name)
    for names in zip_file.namelist():
        zip_file.extract(names,file_path)
    zip_file.close()

def un_gz(file_name, file_path):
    un_tar(file_name, file_path)

def un_rar(file_name, file_path):
    print('111111111111111111111')
    rar = rarfile.RarFile(file_name)
    rar.extractall(path=file_path)
    rar.close()

def un_bz2(file_name, file_path):
    pass

def un_7z(file_name, file_path):
    pass

def sources_type(filepath):
    with open(filepath, 'r') as f:
        src_content = f.readlines()
        for src in src_content:
            if src != '' and src != None:
                print(src.strip().split(' ')[0])
                if src.strip().split(' ')[0] == 'deb':
                    return 'deb'
                else:
                    return 'replace'
        

def dockerfile_built_only_image(main_condict, new_image, image, dependon_install, sources):
    temp_str = ''
    temp_str2 = 'FROM ' + image + '\nCOPY * ' + main_condict['ContainerMoudelPath'][0]
    if sources_type(main_condict['SourcesPath'][0] + sources + '/sources.list') == 'deb':
        with open(main_condict['ImagesPath'][0] + new_image + '/sources.list', mode='w+') as f:
            with open(main_condict['SourcesPath'][0] + sources + '/sources.list', mode='r+') as f2:
                f.write(f2.read())
        temp_str2 += '\nCOPY sources.list /etc/apt/' + '\nCOPY * ' + main_condict['ContainerMoudelPath'][0] + '\nRUN apt-get update  '           
    else:
        sel_sources = sources.split('-')[0] + 'SourcesReplace'
        with open(main_condict['SourcesPath'][0] + sources + '/sources.list', mode='r+') as f2:
            rep_content = f2.read().strip()
            for length in range(len(main_condict[sel_sources])):
                if length == 0:
                    temp_str2 += '\nRUN sed -i "s/' + main_condict[sel_sources][length].strip() +'/' + rep_content + '/g" /etc/apt/sources.list \ ' 
                else:
                    temp_str2 += '\n\t&& sed -i "s/' + main_condict[sel_sources][length].strip() +'/' + rep_content + '/g" /etc/apt/sources.list \ ' 
            temp_str2 += '\n\t&& apt-get update '
        if dependon_install != ''  and dependon_install != None:
            temp_str = '\nRUN '
            dependon_install = dependon_install.split('\r\n')
            for run in dependon_install:
                if run.strip() != '':
                    if temp_str == '\nRUN ':
                        temp_str += run.strip() + ' -y \ '
                    else:
                        temp_str += ' \n    && ' + run.strip() + ' -y \ '
    return  temp_str2 + temp_str
