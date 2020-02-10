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