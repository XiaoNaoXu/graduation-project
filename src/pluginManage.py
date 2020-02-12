import os
from src.mydocker import my_docker
from src.con import main_con, readlist
from src.imageManage import image_delete
from src.containerManage import container_delete

def localfile_delete(filename, path):
    if os.path.isdir(path + filename):
        for files in os .listdir(path + filename):
            localfile_delete(files, path + filename + '/')
        try:
            os.rmdir(path + filename)
        except Exception as err:
            print('localfile_delete: ', err)
    else:
        try:
            os.remove(path + filename)
        except Exception as err:
            print('localfile_delete: ', err)


def plugin_delete(plugin, moulists):
    temp = list()
    main_condict = main_con()
    image_delete(plugin + ':' + main_condict['image_tag'][0])
    for key in list(moulists.keys()):
        for mou in moulists[key]:
            if plugin == mou:
                moulists[key].remove(plugin)
                break
        if moulists[key] == []:
            moulists.pop(key)
        else:
            temp.append('[' + key + ']\n')
            for mou in moulists[key]:
                temp.append('    ' + mou + '\n')
    with open(main_condict['moudles_path'][0] + 'list', 'w+') as f:
        f.truncate()
        f.writelines(temp)
    localfile_delete(plugin, main_condict['file_path'][0])
    localfile_delete(plugin, main_condict['moudles_path'][0])

def plugin_update(plugin, configs):
    pass

def sources_type(filepath):
    with open(filepath, 'r') as f:
        src_content = f.read().strip()
        if src_content == 'deb':
            return 'deb'
        else:
            return 'replace'

def plugin_add(main_condist, pluginname, image, inputfilename, inputtype, dependon_install, detail, sources, files):
    if not os.path.exists(main_condist['moudles_path'][0] + pluginname):
        os.mkdir(main_condist['moudles_path'][0] + pluginname)
        with open(main_condist['moudles_path'][0] + 'list', 'r+') as f:
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
        os.mkdir(main_condist['file_path'][0] + pluginname)
    # with open(main_condist['moudles_path'][0] + pluginname + '/__init__.py', mode='r') as f:
    #         pass
    with open(main_condist['moudles_path'][0] + pluginname + '/Dockerfile', mode='w+') as f:
        temp_str = ''
        temp_str2 = 'FROM ' + image + '\nCOPY * ' + main_condist['container_moudel_path'][0]
        if sources_type(main_condist['sources_path'][0] + sources + '/sources.list') == 'deb':
            with open(main_condist['moudles_path'][0] + pluginname + '/sources.list', mode='w+') as f:
                with open(main_condist['sources_path'][0] + sources + '/sources.list', mode='r+') as f2:
                    f.write(f2.read())
            temp_str2 += '\nCOPY sources.list /etc/apt/' + '\nCOPY * ' + main_condist['container_moudel_path'][0] + '\nRUN apt-get update \ ' \
                                        + '\n && mkdir -p /home/plugin/data \ ' + '\n && mkdir -p /home/plugin/result '                               
        else:
            sel_sources = sources.split('-')[0] + '_sources_replace'
            with open(main_condist['sources_path'][0] + sources + '/sources.list', mode='r+') as f2:
                rep_content = f2.read().strip()
                for length in range(len(main_condist[sel_sources])):
                    if length == 0:
                        temp_str2 += '\nRUN sed -i "s/' + main_condist[sel_sources][length].strip() +'/' + rep_content + '/g" /etc/apt/sources.list \ ' 
                    else:
                        temp_str2 += '\n\t&& sed -i "s/' + main_condist[sel_sources][length].strip() +'/' + rep_content + '/g" /etc/apt/sources.list \ ' 
                temp_str2 += '\n\t&& apt-get update \ ' + '\n\t&& mkdir -p /home/plugin/data \ ' + '\n\t&& mkdir -p /home/plugin/result '
        if dependon_install != ''  and dependon_install != None:
            temp_str = '\nRUN '
            dependon_install = dependon_install.split('\r\n')
            for run in dependon_install:
                if run.strip() != '':
                    if temp_str == '\nRUN ':
                        temp_str += run.strip() + ' -y \ '
                    else:
                        temp_str += ' \n        && ' + run.strip() + ' -y \ '
        f.write(temp_str2 + temp_str)
    with open(main_condist['moudles_path'][0] + pluginname + '/.Config', mode='w+') as f:
        f.write('\n\n[arguments]')
        f.write('\ninputfilename = ' + inputfilename)
        intype = ','.join(inputtype)
        f.write('\ninputtype = ' + intype)
        f.write('\nsources = ' + sources)
        f.write('\n##################################\n')
        f.writelines(detail)
        f.write('\n##################################\n')
    for f in files:
        filename = f.filename
        """文件安全验证"""
        f.save(os.path.join(main_condist['moudles_path'][0] + pluginname + '/', filename))
    try:
        my_docker(pluginname, main_condist)
    except Exception as err:
        print('my_docker: ', err)
        plugin_delete(pluginname, readlist(main_condist))
