import os
from src.mydocker import my_docker
from src.con import main_con, readlist, dockerfile_built, localfile_delete, list_clear
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


def plugin_add(main_condict, pluginname, image, inputfilename, inputtype, dependon_install, detail, sources, files, runcommand):
    if not os.path.exists(main_condict['MoudlesPath'][0] + pluginname):
        os.makedirs(main_condict['MoudlesPath'][0] + pluginname)
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
    # with open(main_condict['MoudlesPath'][0] + pluginname + '/__init__.py', mode='r') as f:
    #         pass
    with open(main_condict['MoudlesPath'][0] + pluginname + '/Dockerfile', mode='w+') as f:
        f.write(dockerfile_built(main_condict, pluginname, image, dependon_install, sources))
    with open(main_condict['MoudlesPath'][0] + pluginname + '/.Config', mode='w+') as f:
        f.truncate()
        f.write('[arguments]')
        f.write('\ninputfilename = ' + inputfilename)
        intype = ','.join(inputtype)
        f.write('\ninputtype = ' + intype)
        f.write('\nsources = ' + sources)
        f.write('\nruncommand = ' + runcommand)
        f.write('\npluginrootpath = ' + main_condict['ContainerMoudelPath'][0])
        f.write('\n##################################\n')
        f.writelines(detail)
        f.write('\n##################################\n')
    for f in files:
        filename = f.filename
        """文件安全验证"""
        f.save(os.path.join(main_condict['MoudlesPath'][0] + pluginname + '/', filename))
    try:
        my_docker(pluginname, main_condict)
    except Exception as err:
        print('my_docker: ', err)
        plugin_delete(pluginname, readlist(main_condict))
