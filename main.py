from flask import Flask, render_template, request, redirect, url_for, g, flash, send_from_directory, jsonify
import os, random, string, json
from werkzeug.utils import secure_filename
from src.mou import Platform
from src.myForm import myForm,addForm,fileDownload, manageForm
from src.con import *
from src.mydocker import my_docker, get_images_list
from src.pluginManage import plugin_add, plugin_delete, plugin_update
from src.imageManage import image_add, image_delete, image_list
from src.containerManage import containers_list, container_delete
from src.sourcesManage import sources_delete, sources_list, sources_modification

app = Flask(__name__)
app.config["SECRET_KEY"] = 'qqq123456'
app.config['JSON_AS_ASCII'] = False
app.debug = 'True'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#路由--------登录页面路由
@app.route('/login')
def login():
           return render_template('login.html')

#路由--------首页路由
@app.route('/', methods = ['GET', 'POST'])
def index():
        num = [0, 0, 0, 0]
        #读取框架配置参数
        main_condist = main_con()
        #读取接口列表
        moulists = readlist(main_condist)
        #计算语言数量
        num[0] = len(moulists)
        myform = myForm()       #前端页面表单构造
        languages = list()              #存放语言的空列表
        plugins = list()                #存放接口名称的空列表
        intypes = list()                #存放输入类型的空列表
        outtypes = list()               #存放输出类型的空列表
        text = ''                               #初始文本框的内容
        ext = ''                                #文件后缀
        filenames = list()              #存放上传的文件列表
        temppath = ''                           #工作路径

        if moulists == {}:
                return render_template('index.html',
                                                                languages = languages, selanguage = '',
                                                                plugins = plugins, seplugin = '', 
                                                                intypes = intypes,  seintype = '',
                                                                text = text, myform = myform,
                                                                nums = num, details = '',
                                                                ftype = 'text', filecode = 'none')

        #页面请求为GET
        if request.method == 'GET':
                #分离语言列表并排序
                for key in moulists:
                        languages.append(key)
                languages.sort()
                #分别分离接口名称，输入类型，输出名称并计算变量个数----start
                plugins = moulists[languages[0]]
                num[1]= len(plugins)
                con_temp = read_obiect_config(plugins[0], main_condist)
                intypes = con_temp['inputtype']
                num[2] = len(intypes)
                #分别分离接口名称，输入类型，输出名称并计算变量个数----end
                #返回模板
                return render_template('index.html',
                                                                languages = languages, selanguage = '',
                                                                plugins = plugins, seplugin = '', 
                                                                intypes = intypes,  seintype = '',
                                                                text = text, myform = myform,
                                                                nums = num, details = con_temp['detail'],
                                                                ftype = 'text', filecode = 'none')
        
        #页面请求方式为POST
        else:
                #获取页面参数
                language = request.form.get('language') #获取选中语言
                plugin = request.form.get('plugin')     #获取选中接口名称
                intype = request.form.get('intype')     #获取选中输入类型
                # outtype = request.form.get('outtype')   #获取选中输出类型
                filecode = request.form.get('filecode')         #获取隐藏的文件码
                sefilename = request.form.get('filename')       #获取当前选中文件
                ftype = 'text'                                                          #默认前端显示类型为文本
                href = ''                                                                       #初始href为空

                #分离语言列表
                for mous in moulists:
                        languages.append(mous)
                languages.sort()
                #分离接口名称列表
                plugins = moulists[language]
                num[1] = len(plugins)
                
                #页面刷新判断接口名称是否存在
                if isexit(plugin, plugins) == 0:
                        plugin = plugins[0]

                #读取该接口的配置参数
                con_temp = read_obiect_config(plugin, main_condist)

                intypes = con_temp['inputtype']
                num[2] = len(intypes)

                #收到来自前端页面的按钮点击
                if myform.validate_on_submit:

                        #运行按钮的动作
                        if myform.publish.data:
                                if filecode != 'none': 
                                        text = request.form.get('textarea')
                                        if text != '':
                                                temppath = main_condist['file_path'][0] + plugin + '/' + filecode + '/'
                                                # plat = Platform(plugin, temppath)
                                                docker = my_docker(plugin, main_condist, filecode)
                                                docker.containers_start()
                                                return redirect(url_for('resullt', pluginname = plugin, findfilecode = filecode))
                        
                        #删除按钮的动作
                        elif myform.delete.data:
                                if sefilename != None:
                                        delete_path = main_condist['file_path'][0] + plugin + '/' + filecode + '/data/' + sefilename
                                        if  os.path.isfile(delete_path):
                                                os.remove(delete_path)

                        #上传按钮的动作
                        elif myform.add.data:
                                ext = ''    #文件后缀
                                temppath = '' #文件路径
                                for f in request.files.getlist('sourcefile'):
                                        #如果没上传文件，就获取文本款的内容，根据选择的格式保存-------start
                                        if f.filename == '':
                                                text = request.form.get('textarea')
                                                if text != '' and text != None:
                                                        temppath = main_condist['file_path'][0] + plugin + '/' + filecode + '/data/'
                                                        if text != '内容不可读！':
                                                                if not os.path.isdir(temppath):
                                                                        filecode = ''.join(random.sample(main_condist['codestr'][0],main_condist['filecode_length'][0]))
                                                                        temppath = main_condist['file_path'][0] + plugin + '/' + filecode + '/data/'
                                                                        os.mkdir(temppath)
                                                                with open(temppath + con_temp['inputfilename'][0] + '.' + intype, 'w+') as fo:
                                                                        fo.writelines(text)
                                                                        break
                                                # else:
                                                #         return render_template('index.html',
                                                #                                                         languages = languages, selanguage = language,
                                                #                                                         plugins = plugins, seplugin = plugin, 
                                                #                                                         intypes = intypes,  seintype = intype,
                                                #                                                         outtypes = outtypes, seouttype = outtype,
                                                #                                                         text = text, myform = myform,
                                                #                                                         nums = num, details = con_temp['detail'],
                                                #                                                         ftype = 'text', filecode = filecode,
                                                #                                                         sefilename = sefilename)
                                        #如果没上传文件，就获取文本款的内容，根据选择的格式保存-------end

                                        #如果有上传文件，就循环保存文件------------------------------------------------------------------start
                                        else:
                                                filename = f.filename
                                                temppath = main_condist['file_path'][0] + plugin + '/' + filecode + '/data/'
                                                if not os.path.isdir(temppath):
                                                        filecode = ''.join(random.sample(main_condist['codestr'][0], int(main_condist['filecode_length'][0])))
                                                        temppath = main_condist['file_path'][0] + plugin + '/' + filecode + '/'
                                                        os.mkdir(temppath)
                                                        temppath = main_condist['file_path'][0] + plugin + '/' + filecode + '/data/'
                                                        os.mkdir(temppath)
                                                f.save(os.path.join(temppath, filename))
                                        #如果有上传文件，就循环保存文件---------------------------------------------------------------------end
                #分离输入输入类型并计算变量个数
                if filecode != '' and filecode != None and filecode != 'none':
                        #获取文件列表------------------------------------------------------------------------------satrt
                        temppath = main_condist['file_path'][0] + plugin + '/' + filecode + '/data/'
                        if os.path.isdir(temppath):
                                if os.path.isdir(temppath):
                                        for t_filename in os.listdir(temppath):
                                                if t_filename != '.filelist' and t_filename[0:16] != filecode and os.path.isfile(temppath + t_filename):
                                                        filenames.append(t_filename)
                                filenames.sort()
                                if len(filenames) != 0:
                                        #判断选中文件是否存在列表，取出后缀并寻找类型
                                        if isexit(sefilename, filenames) == 0:
                                                sefilename = filenames[0]
                                        try:
                                                ext = sefilename.rsplit('.', 1)[1]
                                        except:
                                                pass
                                        # fftype = filetype.guess(temppath + sefilename)
                                        # print(fftype.mime)
                                        ftype = type_find(ext, main_condist)
                                        if ftype == None and ext == '':
                                                ftype = 'text'
                                        #如果文件类型为图片，就构造href，传递给前端显示
                                        if ftype == 'images':
                                                href = temppath + sefilename
                                        #文件类型为文本，就读取并显示到文本框
                                        elif ftype == 'text':
                                                with open(temppath + sefilename, 'r') as tf:
                                                        try:
                                                                text = tf.read()
                                                        except:
                                                                text = '内容不可读！'
                                        #文件无类型，暂时保存，要修改
                                        elif ftype == None:
                                                with open(temppath + sefilename, 'r') as tf:
                                                        try:
                                                                text = tf.read()
                                                        except:
                                                                text = '内容不可读！'
                        #获取文件列表------------------------------------------------------------------------------end
                #返回模板
                return render_template('index.html',
                                                                languages = languages, selanguage = language,
                                                                plugins = plugins, seplugin = plugin, 
                                                                intypes = intypes,  seintype = intype,
                                                                text = text, myform = myform, filecode = filecode,
                                                                nums = num, details = con_temp['detail'], 
                                                                ftype = ftype, href = href,
                                                                filenames = filenames, sefilename = sefilename)

#路由--------添加接口页面路由
@app.route('/addplug', methods = ['GET', 'POST'])
def addplug():
        num = [0, 0, 0, 0]
        #读取框架配置参数
        main_condist = main_con()
        #读取接口列表
        moulists = readlist(main_condist)
        #计算语言数量
        num[0] = len(moulists)
        myform = addForm()   #添加接口页面表单构造
        myform.sources.choices = sources_choices()
        myform.language.choices = language_choices()
        lines = list()               #存放接口列表名称的空列表   

        #请求方式为GET
        if request.method == 'GET':
                return render_template('addplug.html', myform = myform)
        
        #请求方式为POST
        else:
                #接口的名称，因为需要判断是否重名，所以提前获取
                pluginname = myform.pluginname.data
                #前段页面添加叫提交
                if myform.validate_on_submit:
                        mous = []
                        for key in moulists:
                                mous += moulists[key]
                        if pluginname in mous:
                                flash('该名称已存在！')
                                return render_template('addplug.html', myform = myform)
                        if myform.pulish.data:
                                # 针对接口选择的基础镜像
                                image = myform.language.data 
                                #当数据为键入时保存的文件的名字
                                inputfilename = myform.inputfilename.data
                                #当数据为键入时保存的文件的类型
                                inputtype = myform.inputtype.data
                                #所需
                                dependon_install = myform.textarea.data
                                detail = myform.detail.data
                                sources = myform.sources.data
                                files = request.files.getlist('pluginfile')
                                plugin_add(main_condist, pluginname, image, inputfilename, inputtype, dependon_install, detail, sources, files)
                                return render_template('addplug.html', myform = myform)
                        elif myform.save.data:
                                return render_template('addplug.html', myform = myform)
        return render_template('addplug.html', myform = myform)

#路由--------直接点击结果页面路由
@app.route('/result', methods = ['GET','POST'])
def result(text = ''):
        num = [0, 0, 0, 0]
        moulists = dict()
        main_condist = dict()
        #读取框架配置参数
        main_condist = main_con()
        #读取接口列表
        moulists = readlist(main_condist)
        #计算语言数量
        num[0] = len(moulists)
        ext = ''
        href = ''
        filecode = ''
        file_path = ''
        sefilename = ''
        filenames = list()
        file_list = dict()
        templist = list()
        filedownload = fileDownload()
        tap = '文件码无效或已失效!'
        if request.method == 'GET':
                return render_template('result.html',filedownload = filedownload, text12 = text)
        else:
                #前段页面，按钮点击事件
                if filedownload.validate_on_submit:
                        filecode = request.form.get('id')
                        file_path = './static/file'
                        if os.path.isdir(file_path) and filecode != '':
                                for tpath in os.listdir(file_path):
                                        if os.path.isdir(file_path + '/' + tpath + '/' + filecode) :
                                                tap = ''
                                                path = file_path + '/' + tpath + '/' + filecode + '/'
                                                temp = path.split('/')
                                                temp = temp[len(temp) - 2]
                                                sefilename = request.form.get('filecode')
                                                for dirs in os.listdir(path + 'result/'):
                                                        if os.path.isfile(path + 'result/' + dirs) and dirs != temp + '.zip':
                                                                file_list[dirs] = path + 'result/' + dirs
                                                for key in file_list:
                                                        filenames.append(key)
                                                filenames.sort()
                                                #下载单个文件
                                                if filedownload.downloadf.data and sefilename != '':
                                                        filename = sefilename
                                                        path = file_list[filename][0:(len(file_list[filename]) - len(filename))]
                                                        if os.path.isfile(path + filename):
                                                                return send_from_directory(path, filename, as_attachment=True)
                                                #文件打包下载
                                                elif filedownload.alldownloadf.data:
                                                        for key in file_list:
                                                                filename = key
                                                                path = file_list[filename][0:(len(file_list[filename]) - len(filename))]
                                                                temp = path.strip().split('/')
                                                                tempt = temp[len(temp) - 2] + temp[len(temp) - 1]
                                                                path = path[0:(len(path) - len(tempt) - 1)]
                                                                filename = zip_file(path, filecode, 'w')
                                                                if os.path.isfile(path + filename):
                                                                        return send_from_directory(path, filename, as_attachment=True)
                                                #文件码查找
                                                elif filedownload.find.data:
                                                        pass
                                                if sefilename == None  or isexit(sefilename, filenames) == 0:
                                                        sefilename = filenames[0]
                                                try:
                                                        ext = sefilename.split('.')[1]
                                                except:
                                                        pass
                                                ftype = type_find(ext, main_condist)
                                                if ftype == None and ext == '':
                                                        ftype = 'text'
                                                #如果文件类型为图片，就构造href，传递给前端显示
                                                if ftype == 'images':
                                                        href =  file_list[sefilename]
                                                #文件类型为文本，就读取并显示到文本框
                                                elif ftype == 'text':
                                                        with open(file_list[sefilename], 'r') as tf:
                                                                try:
                                                                        text = tf.read()
                                                                except:
                                                                        text = '内容不可读！'
                                                #文件无类型，暂时保存，要修改
                                                else:
                                                        with open(file_list[sefilename], 'r') as f:
                                                                try:
                                                                        text = f.read()
                                                                except:
                                                                        text = '内容不可读！'
                                                return render_template('result.html',
                                                                                                filedownload = filedownload, 
                                                                                                text12 = text, findfilecode = filecode,
                                                                                                tap = tap, ftype = ftype, href = href,
                                                                                                filecodes = filenames, sefilecode = sefilename)
                return render_template('result.html',filedownload = filedownload, text12 = text, tap = tap)

#路由--------计算跳转结果页面路由
@app.route('/resullt/<pluginname>, <findfilecode>', methods = ['GET', 'POST'])
def resullt(pluginname, findfilecode):
        num = [0, 0, 0, 0]
        #读取框架配置参数
        main_condist = main_con()
        #读取接口列表
        moulists = readlist(main_condist)
        #计算语言数量
        num[0] = len(moulists)
        ext = ''
        text = ''
        href = ''
        filename = ''
        sefilecode = ''
        ftype = ''
        file_list = dict()
        templist = list()
        filedownload = fileDownload()
        
        if request.method == 'GET':
                path = main_condist['file_path'][0] + pluginname + '/' + findfilecode + '/result/'
                if os.path.isdir(path):
                        for filet in os.listdir(path):
                                if os.path.isfile(path + filet):
                                        file_list[filet] = path + filet
                for key in file_list:
                        templist.append(key)
                templist.sort()
                if templist != []:
                        if isexit(sefilecode, templist) == 0:
                                sefilecode = templist[0]
                        try:
                                ext = sefilecode.split('.')[1]
                        except:
                                pass
                        ftype = type_find(ext, main_condist)
                        if ftype == None and ext == '':
                                ftype = 'text'
                        #如果文件类型为图片，就构造href，传递给前端显示
                        if  ftype == 'images':
                                href = '.' + file_list[sefilecode]
                        #文件类型为文本，就读取并显示到文本框
                        elif ftype == 'text':
                                with open(file_list[sefilecode], 'r') as f:
                                        try:
                                                text = f.read()
                                        except:
                                                text = '内容不可读！'
                        #文件无类型，暂时保存，要修改
                        else:
                                with open(file_list[sefilecode], 'r') as f:
                                        try:
                                                text = f.read()
                                        except:
                                                text = '内容不可读！'
                return render_template('result.html',
                                                                filedownload = filedownload, sefilecode = sefilecode,
                                                                text12 = text, ftype = ftype, href = href,
                                                                filecodes = templist, findfilecode = findfilecode)
        else:
                findfilecode = request.form.get('id')
                sefilecode = request.form.get('filecode')
                temp_path = main_condist['file_path'][0]
                if os.path.isdir(temp_path):
                        for dirs in os.listdir(temp_path):
                                if os.path.isdir(temp_path + dirs + '/' + findfilecode + '/'):
                                        pluginname = dirs
                path = main_condist['file_path'][0] + pluginname + '/' + findfilecode + '/result/'
                if os.path.isdir(path):
                        for filet in os.listdir(path):
                                if os.path.isfile(path + filet):
                                        file_list[filet] = path + filet
                        if filedownload.validate_on_submit:
                                sefilecode = request.form.get('filecode')
                                #下载单个文件
                                if filedownload.downloadf.data:
                                        filename = sefilecode
                                        path = file_list[filename][0:(len(file_list[filename]) - len(filename))]
                                        if os.path.isfile(path + filename):
                                                return send_from_directory(path, filename, as_attachment=True)
                                #文件打包下载
                                elif filedownload.alldownloadf.data:
                                        for key in file_list:
                                                filename = key
                                                path = file_list[filename][0:len(file_list[filename]) - len(filename)]
                                                temp = path.strip().split('/')
                                                tempt = temp[len(temp) - 2] + temp[len(temp) - 1]
                                                path = path[0:(len(path) - len(tempt) - 1)]
                                                filename = zip_file(path, findfilecode, 'w')
                                                if os.path.isfile(path + filename):
                                                        return send_from_directory(path, filename, as_attachment=True)
                                #文件码查找
                                elif filedownload.find.data:
                                        templist.clear()
                                        file_list.clear()
                                        path = main_condist['file_path'][0] + pluginname + '/' + findfilecode + '/result/'
                                        if os.path.isdir(path):
                                                for filet in os.listdir(path):
                                                        if os.path.isfile(path + filet):
                                                                file_list[filet] = path + filet
                                for key in file_list:
                                        templist.append(key)
                                templist.sort()
                                if isexit(sefilecode, templist) == 0:
                                        sefilecode = templist[0]
                                try:
                                        ext = sefilecode.split('.')[1]
                                except:
                                        pass
                                ftype = type_find(ext, main_condist)
                                if ftype == None and ext == '':
                                        ftype = 'text'
                                #如果文件类型为图片，就构造href，传递给前端显示
                                if  ftype == 'images':
                                        href = '.' + file_list[sefilecode]
                                #文件类型为文本，就读取并显示到文本框
                                elif ftype == 'text':
                                        with open(file_list[sefilecode], 'r') as f:
                                                try:
                                                        text = f.read()
                                                except:
                                                        text = '内容不可读！'
                                #文件无类型，暂时保存，要修改
                                else:
                                        with open(file_list[sefilecode], 'r') as f:
                                                try:
                                                        text = f.read()
                                                except:
                                                        text = '内容不可读！'
                return render_template('result.html',
                                                                filedownload = filedownload, sefilecode = sefilecode,
                                                                text12 = text, pluginname = pluginname, href = href, ftype = ftype,
                                                                filecodes = templist, findfilecode = findfilecode)

#路由--------管理接口页面路由
@app.route('/manage', methods = ['GET','POST'])
def manage():
        num = [0, 0, 0, 0]
        row_flag  = 0
        #读取框架配置参数
        main_condist = main_con()
        #读取接口列表
        moulists = readlist(main_condist)
        #计算语言数量
        num[0] = len(moulists)
        mous = dict()
        images = dict()
        containers = dict()
        sources_dict = dict()
        other_data = dict()
        manageform = manageForm()
        for image in moulists:
                for mou in moulists[image]:
                        mous[mou] = {'image' : image, 'edit_flag' : [0, 0]}
                        mous[mou].update(read_obiect_config(mou, main_condist))

        if request.method == 'GET':
                return render_template('manage.html',manageform = manageform, mous = mous)
        else:
                sename = request.form.get('txt')
                sesource = request.form.get('source')
                if sesource == None or sesource == '':
                        try:
                                sesource =  mous[sename]['sources'][0]
                        except:
                                pass
                sources = get_sources()
                manage_select = request.form.get('manage_select')
                if manage_select == None or manage_select == '':
                        manage_select = 'plugin'
                if manageform.validate_on_submit:
                        if manageform.plugin.data:
                                manage_select = 'plugin'
                        elif manageform.image.data:
                                manage_select = 'image'
                        elif manageform.container.data:
                                manage_select = 'container'
                        elif manageform.sources.data:
                                manage_select = 'sources'
                        elif manageform.image_add.data:
                                manage_select = 'image_add'
                        elif manageform.other_add.data:
                                manage_select = 'other_add'
                        if manage_select == 'plugin':
                                if manageform.delete.data:
                                        plugin_delete(sename, moulists)
                                        mous.pop(sename)
                                elif manageform.edit.data:
                                        mous[sename]['edit_flag'][0] = mous[sename]['edit_flag'][1] + 1
                                elif manageform.commit.data:
                                        mous[sename]['edit_flag'][0] = mous[sename]['edit_flag'][1]
                                elif manageform.cancel.data:
                                        mous[sename]['edit_flag'][0] = mous[sename]['edit_flag'][1]
                        elif manage_select == 'image':
                                images_t = sorted(image_list().items(), key = lambda x:x[0])
                                for image in images_t:
                                        images[image[0]] = image[1]
                                # images = image_list()
                                if manageform.delete.data:
                                        image_delete(sename)
                                        images.pop(sename)
                                elif manageform.container_add.data:
                                        con_docker_object = my_docker(sename, config = main_condist, filecode='--no-filecode', images=True, containers=False )
                                        container_name = sename.split(':')[0] + '_' + ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 10))
                                        con_docker_object.container_ceate(container_name)
                        elif manage_select == 'container':
                                containers = containers_list(main_condist)
                                if manageform.delete.data:
                                        container_delete(sename)
                                        containers.pop(sename)
                        elif manage_select == 'sources':
                                sources_dict = sources_list(sources, main_condist)
                                if manageform.delete.data:
                                        sources_delete(sename, main_condist)
                                        sources_dict.pop(sename)
                                elif manageform.edit.data:
                                        sources_dict[sename][1] = 1
                                elif manageform.commit.data:
                                        sources_content = request.form.get('sources-content')
                                        if sources_modification(sename, sources_content, main_condist) == True:
                                                print(sources_content)
                                                sources_dict[sename][0] = sources_content
                                elif manageform.cancel.data:
                                        pass
                                return jsonify(sources_dict)
                        elif manage_select == 'image_add':
                                if manageform.commit.data:
                                        other_data['basic_image'] = request.form.get('basic-image')
                                        other_data['install_content'] = request.form.get('install-content')
                                        other_data['source_select'] = request.form.get('source-select')
                                        other_data['image_tag'] = request.form.get('image-tag')
                                        docker_object = my_docker('--no-plugin', config = main_condist, filecode='--no-filecode', images=False, containers=False )
                                        docker_object.basic_image_build(other_data['basic_image'], 
                                                                                                                other_data['image_tag'],
                                                                                                                other_data['source_select'],
                                                                                                                other_data['install_content']
                                                                                                                )
                                        flash(docker_object.run_log)
                        elif manage_select == 'other_add':
                                if manageform.commit.data:
                                        sources_name = request.form.get('sources-name')
                                        if os.path.isdir(main_condist['sources_path'][0]) and not os.path.isdir(main_condist['sources_path'][0] + sources_name):
                                                os.mkdir(main_condist['sources_path'][0] + sources_name)
                                        sources_content = request.form.get('sources-content')
                                        with open(main_condist['sources_path'][0] + sources_name + '/sources.list', 'w+') as f:
                                                f.write(sources_content)
                return render_template('manage.html',manageform = manageform, mous = mous,
                                                                sources = sources, sesource = sesource, manage_select = manage_select, 
                                                                images = images, containers = containers, sources_dict = sources_dict,
                                                                other_data = other_data)


#路由---------帮助页路由
@app.route('/help', methods = ['GET','POST'])
def help():
        num = [0, 0, 0, 0]
        moulists = dict()
        main_condist = dict()
        #读取框架配置参数
        main_condist = main_con()
        #读取接口列表
        moulists = readlist(main_condist)
        #计算语言数量
        num[0] = len(moulists)
        if request.method == 'GET':
                return render_template('help.html')
        else:
                return render_template('help.html')

# @app.errorhandler(404)
# def miss(e):
#     return render_template('404.html')
 
# @app.errorhandler(500)
# def error(e):
#     return render_template('500.html')

#列表接口维护
# def keeplist():
#         #moulists.clear()
#         moulists = readlist(main_condist)


        
#程序入口
if __name__ == "__main__":
        #运行
        app.run(host='0.0.0.0', port=8080)
        # app.run()