from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed,FileField, DataRequired
from wtforms.fields import simple, html5, core, TextAreaField
from wtforms import widgets, validators
from wtforms.validators import ValidationError, NoneOf, AnyOf
from src.con import language_choices, sources_choices


class myForm(FlaskForm):
    sourcefile = FileField(
        label='选择文件：',
        validators=[
            FileAllowed(['txt'])
            ]
    )
    delete = simple.SubmitField('删除')
    add = simple.SubmitField('上传')
    publish = simple.SubmitField('运行')

class addForm(FlaskForm):
    language = core.SelectField(
        label = '基础环境镜像：',
        choices = language_choices(),
    )
    pluginname = simple.StringField(
        label= '接口名称: ',
        widget=widgets.TextInput(),
        # validators=[DataRequired(message='接口名称不能为空'), 
        #                         NoneOf(['t1', 't2', 't10', '3'], message='wuxiao', values_formatter = 'caonima')]
        # render_kw={
        #     "placeholder":"请输入账号!",
        #     "required":'required'               #表示输入框不能为空，并有提示信息
        # }
    )
    inputfilename = simple.StringField(
        label = '输入文件名： ',
        widget=widgets.TextInput(),
        # validators=[DataRequired()]
    )
    inputtype = core.SelectMultipleField(
        label='输入数据类型：',
        choices=(
            ('txt', 'txt'),
            ('world', 'world'),
            ('jpg', 'jpg'),
            ('png', 'png')
        ),
        default=['txt', 'world', 'jpg', 'png']
    )
    outputfilename = simple.StringField(
        label = '输出文件名：',
        widget=widgets.TextInput()
    )
    outputtype = core.SelectMultipleField(
        label='输出数据类型：',
        choices=(
            ('txt', 'txt'),
            ('world', 'world'),
            ('jpg', 'jpg'),
            ('png', 'png')
        ),
        option_widget=widgets.CheckboxInput(),
        default=['txt', 'world', 'jpg', 'png']
    )
    sources = core.SelectField(
        label = '软件源：',
        render_kw={
            'class' : 'index-select'
        },
        choices=sources_choices()
    )
    textarea = TextAreaField(
        label='接口运行环境：',
        render_kw={
            'class' : 'text-control'
        },
        # validators=[DataRequired()]
    )
    pluginfile = FileField(
        label='文件选择：',
        # validators=[FileRequired(), 
        #                         FileAllowed(['jpg','jpeg','png','gif'])]
    )
    runCommand = simple.StringField(
        label = '运行命令：',
        widget=widgets.TextInput()
    )
    detail = TextAreaField(
        label='接口描述：',
        render_kw={
            'class' : 'text-detail'
        },
        # validators=[DataRequired()]
    )
    save = simple.SubmitField('检查')
    pulish = simple.SubmitField('提交')


class fileDownload(FlaskForm):
    alldownloadf = simple.SubmitField('全部下载')
    find= simple.SubmitField('查找')
    downloadf = simple.SubmitField('文件下载')

class manageForm(FlaskForm):
    edit = simple.SubmitField('编辑')
    delete = simple.SubmitField('删除')
    cancel = simple.SubmitField('取消')
    commit = simple.SubmitField('提 交')
    update = simple.SubmitField('从Github更新')
    backup = simple.SubmitField('备份')
    container_add = simple.SubmitField('增加容器')

    plugin = simple.SubmitField('接口管理')
    image = simple.SubmitField('镜像管理')
    container = simple.SubmitField('容器管理')
    sources = simple.SubmitField('软件源管理')
    image_add = simple.SubmitField('镜像添加')
    other_add = simple.SubmitField('其他添加')