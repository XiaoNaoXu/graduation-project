import os
import shutil
from subprocess import check_call, check_output
from src.mydocker import my_docker
from src.con import main_con, readlist, dockerfile_built, localfile_delete, list_clear, read_obiect_config
from src.config2 import un_7z, un_bz2, un_gz, un_rar, un_tar, un_zip
from src.imageManage import image_delete
from src.containerManage import container_delete


def plugin_delete(plugin, moulists):
    main_condict = main_con()
    image_delete(plugin + ':' + main_condict['ImageTag'][0])
    list_clear(plugin, main_condict)
    localfile_delete(plugin, main_condict['SDFilePath'][0])
    localfile_delete(plugin, main_condict['MoudlesPath'][0])

def plugin_update(plugin, configs):
    pass

def update_in_github(main_condict, pluginname, config):
    update_project_url = 'git -C ' + main_condict['MoudlesPath'][0] + pluginname + '/ pull ' + config['gitprojecturl'][0] + ' ' 
    result = check_output(update_project_url, shell = True)
    if result.decode() == '已经是最新的。\n'    :
        docker = my_docker(pluginname = pluginname, main_config=main_condict, images=True, containers=False)
        docker.image_name_to_old()
        docker.image = docker.image_build()
        docker.reload(client=False, image=False)
        docker.image_remove(pluginname + ':' + main_condict['ImageTag'][0] + '.old')

def plugin_add(main_condict, pluginname, image, inputfilename, inputtype, 
                                dependon_install, detail, sources, files, runcommand):
    moudle_path = main_condict['MoudlesPath'][0] + pluginname + '/'
    register_type = ''
    if type(files) == str:
        register_type = 'github'
        git_project_url = "git clone " + files + ' ' + moudle_path
        print(git_project_url)
        check_call(git_project_url, shell = True)
    elif type(files) == list:
        register_type = 'file'
        if not os.path.exists(moudle_path):
            os.makedirs(moudle_path)
        for f in files:
            filename = f.filename
            """文件安全验证"""
            f.save(os.path.join(moudle_path, filename))
    # elif type(files) == 'werkzeug.datastructures.FileStorage':
    else:
        register_type = 'zip'
        if not os.path.exists(moudle_path):
            os.makedirs(moudle_path)
        file_name = moudle_path + files.filename
        files.save(file_name)
        file_ext = os.path.splitext(files.filename)[1]
        if file_ext == '.zip':
            un_zip(file_name, moudle_path)
        elif file_ext == '.tar':
            un_tar(file_name, moudle_path)
        elif file_ext == '.gz':
            un_gz(file_name, moudle_path)
        elif file_ext == '.rar':
            un_rar(file_name, moudle_path)
        elif file_ext == '.7z':
            un_7z(file_name, moudle_path)
        elif file_ext == '.bz2':
            un_bz2(file_name, moudle_path)
        os.remove(file_name)
        while True:
            listdirs = os.listdir(moudle_path)
            if len(listdirs) == 1 and os.path.isdir(moudle_path + listdirs[0]):
                for filet in os.listdir(moudle_path + listdirs[0]):
                    try:
                        shutil.move(moudle_path + listdirs[0] + '/' + filet, moudle_path)
                    except Exception as err:
                        print(err)
            # elif len(listdirs) == 2:
            #     filefolder = None
            #     if os.path.isdir(moudle_path + listdirs[0]) and listdirs[0] == 'README.md':
            #         filefolder = moudle_path + listdirs[0]
            else:
                break
            shutil.rmtree(moudle_path + listdirs[0])
        
    # with open(moudle_path + '/__init__.py', mode='r') as f:
    #         pass
    with open(moudle_path + '/Dockerfile', mode='w+') as f:
        f.write(dockerfile_built(main_condict, pluginname, image, dependon_install, sources))
    with open(moudle_path + '/.Config', mode='w+') as f:
        f.truncate()
        f.write('[arguments]')
        f.write('\nimage = ' + image)
        f.write('\nregistertype = ' + register_type)
        if register_type == 'github':
            f.write('\ngitprojecturl = ' + files)
        f.write('\ninputfilename = ' + inputfilename)
        intype = ','.join(inputtype)
        f.write('\ninputtype = ' + intype)
        f.write('\nsources = ' + sources)
        f.write('\nruncommand = ' + runcommand)
        f.write('\npluginrootpath = ' + main_condict['ContainerMoudelPath'][0])
        f.write('\n##################################\n')
        f.writelines(detail)
        f.write('\n##################################\n')
    try:
        my_docker(pluginname, main_condict)
    except Exception as err:
        print('my_docker: ', err)
        plugin_delete(pluginname, readlist(main_condict))
    with open(main_condict['MoudlesPath'][0] + 'list', 'r+') as f:
        lines = f.readlines()
        f.seek(0,0)
        row = -1
        row1 = 0
        for line in f.readlines():
            row1 += 1
            if line.strip() == ('[' + image + ']'):
                row = row1
        if row == -1:
            lines.insert(row1 + 1,  '\n[' + image + ']' + '\n')
            lines.insert(row1 + 2,  '    ' + pluginname + '\n')
        else:
            lines.insert(row,  '    ' + pluginname + '\n')
        f.seek(0,0)
        f.truncate()
        f.writelines(lines)
    os.makedirs(main_condict['SDFilePath'][0] + pluginname)
