// function ScrollHolder()  
// {  
//     //add event to window  
//     this.addWindowListener = function(sEventType, fnHandler) {  
//         if (window.addEventListener) {  
//             window.addEventListener(sEventType, fnHandler, false);  
//         } else if (window.attachEvent) {  
//             window.attachEvent("on" + sEventType, fnHandler);  
//         } else {  
//             window["on" + sEventType] = fnHandler;  
//         }  
//     }  
      
//     //remember scrolling information when window is unloading  
//     this.whenUnload = function()  
//     {  
//         var scrollTop = document.documentElement.scrollTop;  
//         document.cookie = "scrollTop="+scrollTop;  
//     }  
      
//     //set current scroll bar the last page scroll bar position  
//     this.whenLoad = function()  
//     {  
//         var scrollTop = document.cookie.match(new RegExp("(^| )scrollTop=([^;]*)(;|$)"));  
//         if(scrollTop==null)  
//             scrollTop = 0;  
//         window.scrollTo(0,scrollTop[2]);  
//     }  
      
//     //run this script  
//     this.run = function()  
//     {  
//         this.addWindowListener("unload", this.whenUnload);  
//         this.addWindowListener("load", this.whenLoad);  
//     }  
// }  
  
// var scrollHolder = new ScrollHolder();  
// scrollHolder.run();  

window.onload = function(){
    //获取上次滚动条滚动距离
    var x = window.localStorage.getItem("x");
    document.documentElement.scrollTop = x;
}
//监听滚动事件
window.onscroll = function(e){
     //保存当前滚动条滚动距离
     var x = document.documentElement.scrollTop  | document.body.scrollTop;
     window.localStorage.setItem("x",x);
}

label = {
    1 : '多文件上传',
    2 : '从GitHub获取',
    3 : '压缩包上传',
    4 : '暂留'
}


function submit11(form){
    var reg = /^\s*|\s*$/g;
    var pluginfile;
    var selectlabel = document.getElementById('selectlabel').innerHTML;
    for(var i = 0; i < 5; ++i){
        if(selectlabel == label[i]){
            pluginfile = document.getElementById('pluginfile'+ i);
            if(i == 1){
                for(var i = 0; i < pluginfile.files.length; i++){
                    if(pluginfile.files[i].name.split(' ').length > 1){
                        alert('文件名：'  + pluginfile.files[i].name + '中含有空格！')
                        return false;
                    }
                }
            }
            else if(i == 2){
                var content = pluginfile.value;
                var sp = content.split('.');
                if(sp[1] != 'git'){
                    alert('仓库地址：'  + content + '格式不正确！');
                    return false;
                }
            }
            break;
        }
    }
    return false;
    if (form.pluginname.value.replace(reg,'') == ""){
        alert ("请输入接口名称");
        return false;
    }
    else if (form.inputfilename.value.replace(reg,'') == ""){
        alert ("请输入文件名");
        return false;
    }
    else if (form.textarea.value.replace(reg,'') == ""){
        alert ("请输入接口运行环境");
        return false;
    }
    else if (form.pluginfile1.value.replace(reg,'') == ""){
        alert ("文件");
        return false;
    }
    else if (form.runCommand.value.replace(reg,'') == ""){
        alert ("请输入运行命令");
        return false;
    }
    else if (form.detail.value.replace(reg,'') == ""){
        alert ("请输入描述信息");
        return false;
    }
    else {
        return true;
    }
}

function substitute(eletID){
    content = {
        1 : '<label>请选择文件</label>\
            <input id="pluginfile" multiple="multiple" name="pluginfile" type="file">' ,
        2 : '<label>GitHub仓库地址：</label>\
            <input id="pluginfile" style="width: 20rem" name="pluginfile" type="text">' ,
        3 : '<label>请选择压缩文件</label>\
            <input id="pluginfile" name="pluginfile" type="file">' ,
        4 : '<label>请选择文件</label>\
            <input id="pluginfile" multiple="multiple" name="pluginfile" type="file"> '
    };
    var t = document.getElementById('row5rcol1');
    var selectlabel = document.getElementById('selectlabel');
    var x = 1;
    for(var i = 1; i <= 4; i++){
        if(t.innerHTML == content[i]){
            x = i;
            break;
        }
    }
    if(eletID.id == 'last'){
        if(x == 1){
            x = 5;
        }
        selectlabel.value = label[x-1];
        t.innerHTML = content[x-1];
    }
    else if(eletID.id == 'next' ){
        if( x == 4){
            x = 0;
        }
        selectlabel.value = label[x+1];
        t.innerHTML = content[x+1];
    }
    return false;
}

