/*
 *名称:图片上传本地预览插件 v1.1
 *作者:周祥
 *时间:2013年11月26日
 *介绍:基于JQUERY扩展,图片上传预览插件 目前兼容浏览器(IE 谷歌 火狐) 不支持safari
 *插件网站:http://keleyi.com/keleyi/phtml/image/16.htm
 *参数说明: Img:图片ID;Width:预览宽度;Height:预览高度;ImgType:支持文件类型;Callback:选择文件显示图片后回调方法;
 * 参考：http://blog.csdn.net/yippeelyl/article/details/39324027
 *使用方法:
 <div>
 <img id="ImgPr" width="120" height="120" /></div>
 <input type="file" id="up" />
 把需要进行预览的IMG标签外 套一个DIV 然后给上传控件ID给予uploadPreview事件
 $("#up").uploadPreview({ Img: "ImgPr", Width: 120, Height: 120, ImgType: ["gif", "jpeg", "jpg", "bmp", "png"], Callback: function () { }});
 */

imgType = [ 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'ai', 'cdr', 'eps ', 'pic', 'tif','jpg']; //  图片    1
wordType = ['doc', 'docx', 'dot', 'dotx', 'docm', 'dotm'];//2
excelType = ['xlsm', 'xltx', 'xltm', 'xlsb', 'xlam', 'xls','xlsx'];//3
pptType = ['ppt', 'pps', 'pptx', 'ppsx'];//4
pdfType = ['pdf'];//5
videoType = ['avi', 'rmvb', 'rm', 'asf', 'divx', 'mpg', 'mpeg', 'mpe', 'wmv', 'mp4', 'mkv', 'vob', 'wav', 'aif', 'au',
             'mp3', 'ram', 'wma', 'mmf', 'amr', 'aac', 'flac'];//6

jQuery.fn.extend({
    uploadPreview: function (opt) {
        var _self = this;
        var _this = $(this);
        opt = jQuery.extend({Callback: function () {}}, opt);
        $(opt.imgi).on("click",function(){
            opt.li.remove();
        });
        _self.getObjectURL = function (file) {
            var url = null;
            if (window.createObjectURL != undefined) {
                url = window.createObjectURL(file)
            } else if (window.URL != undefined) {
                url = window.URL.createObjectURL(file)
            } else if (window.webkitURL != undefined) {
                url = window.webkitURL.createObjectURL(file)
            }
            return url
        };
        _this.change(function () {
            if (this.value) {
                var pic = opt.img;
                if (RegExp("\.(" + imgType.join("|") + ")$", "i").test(this.value.toLowerCase())) {
                    var browserVersion = window.navigator.userAgent.toUpperCase();
                    //兼容chrome、火狐7+、360浏览器5.5+等，应该也兼容ie10，HTML5实现预览
                    if (this.files) {
                        pic.setAttribute('src', _self.getObjectURL(this.files[0]));
                    }else if(browserVersion.indexOf("MSIE") > -1) {
                        if(browserVersion.indexOf("MSIE 6") > -1) { //ie6
                            pic.setAttribute("src", fileObj.value);
                        } else { //ie[7-9]
                            if(browserVersion.indexOf("MSIE 9") > -1){
                                this.select();
                                this.blur();
                            }
                            var newPreview = opt.div;
                            newPreview.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod='scale',src='" + document.selection.createRange().text + "')";
                            pic.style.display = "none";
                        }
                    } else if(browserVersion.indexOf("FIREFOX") > -1) { //firefox
                            var firefoxVersion = parseFloat(browserVersion.toLowerCase().match(/firefox\/([\d.]+)/)[1]);
                            if(firefoxVersion < 7) { //firefox7以下版本
                                pic.setAttribute("src", fileObj.files[0].getAsDataURL());
                            } else { //firefox7.0+
                                pic.setAttribute("src", window.URL.createObjectURL(fileObj.files[0]));
                            }
                        } else {
                            pic.setAttribute("src", fileObj.value);
                        }
                    opt.Callback()
                }else{
                    console.info(999)
                    initFileList(pic,this.value.toLowerCase());
                }

            }
        })
    }
});

//添加中需要此方法预览
function initFileList(pic,filePath){
    var filename=filePath.replace(/.*(\/|\\)/, "");
    var fileExt=((/[.]/.exec(filename)) ? /[^.]+$/.exec(filename.toLowerCase()) : '')[0].toLowerCase();
    if($.inArray(fileExt, imgType)>=0){
        pic.setAttribute("src", filePath);
    }else if($.inArray(fileExt, excelType)>=0){
        pic.setAttribute("src", "/static/img/default_excel.png");
    }else if ($.inArray(fileExt, wordType)>=0) {
        pic.setAttribute("src", "/static/img/default_word.png");
    }else if($.inArray(fileExt, pptType)>=0){
        pic.setAttribute("src", "/static/img/default_ppt.png");
    }else if($.inArray(fileExt, videoType)>=0){
        pic.setAttribute("src", "/static/img/default_video.png");
    }else if($.inArray(fileExt, pdfType)>=0){
        pic.setAttribute("src", "/static/img/default_pdf.png");
    }else{
        pic.setAttribute("src", "/static/img/default_other.png");
    }
}
function initFileListForDetail(myul,dataList,tablename){
    var htmlBuf = new StringBuffer();
    $.each(dataList, function (index, item) {
        var url="/getFile/?Fid=" + item["_id"] + "&FtableName="+tablename;
        htmlBuf.append('<li>');
        htmlBuf.append('<div class="top">');
        htmlBuf.append('<a href='+url+' title="' + item.filename.substring(32, item.filename.length) + '">');
        var filename=item.filename.replace(/.*(\/|\\)/, "");
        var fileExt=((/[.]/.exec(filename)) ? /[^.]+$/.exec(filename.toLowerCase()) : '')[0].toLowerCase();
        if($.inArray(fileExt, imgType)>=0){
            htmlBuf.append('<img src='+url+'></a>');
        }else if($.inArray(fileExt, excelType)>=0){
            htmlBuf.append('<img src="/static/img/default_excel.png"/></a>');
        }else if ($.inArray(fileExt, wordType)>=0) {
            htmlBuf.append('<img src="/static/img/default_word.png"/></a>');
        }else if($.inArray(fileExt, pptType)>=0){
            htmlBuf.append('<img src="/static/img/default_ppt.png"/></a>');
        }else if($.inArray(fileExt, videoType)>=0){
            htmlBuf.append('<img src="/static/img/default_video.png"/></a>');
        }else if($.inArray(fileExt, pdfType)>=0){
            htmlBuf.append('<img src="/static/img/default_pdf.png"/></a>');
        }else{
            htmlBuf.append('<img src="/static/img/default_other.png"/></a>');
        }
        htmlBuf.append('<a href='+url+'>' + item.filename + '</a>');
        htmlBuf.append('</div>');
        htmlBuf.append('</li>');
    });
    myul.html(htmlBuf.arrayToString().toString());
}
/*查看附件初始化*/
function initFileSeeByOne(myid,myurl,tablename){
    var fileurl="/getFile/?Fid="+myurl.substring(0,24)+"&FtableName="+tablename;
    var a_id="#a_"+myid;
    var id="#"+myid;
    if (myurl!=""&&myurl!=null&&myurl!=undefined){
        var filename=myurl.replace(/.*(\/|\\)/, "");
        var fileExt=((/[.]/.exec(filename)) ? /[^.]+$/.exec(filename.toLowerCase()) : '')[0].toLowerCase();
        if($.inArray(fileExt, imgType)>=0){
            $(id).attr("src",fileurl)
        }else if($.inArray(fileExt, excelType)>=0){
            $(id).attr("src","/static/img/default_excel.png");
        }else if ($.inArray(fileExt, wordType)>=0) {
            $(id).attr("src","/static/img/default_word.png");
        }else if($.inArray(fileExt, pptType)>=0){
            $(id).attr("src","/static/img/default_ppt.png");
        }else if($.inArray(fileExt, videoType)>=0){
            $(id).attr("src","/static/img/default_video.png");
        }else if($.inArray(fileExt, pdfType)>=0){
            $(id).attr("src","/static/img/default_pdf.png");
        }else{
            $(id).attr("src","/static/img/default_other.png");
        }
        $(a_id).attr("href", fileurl);
    }else {
        $(id).attr("src","/static/img/default_img.png");
    }
}
/*修改附件初始化*/
function initFileEditByOne(myid,myurl,tablename){
    var fileurl="/getFile/?Fid="+myurl.substring(0,24)+"&FtableName="+tablename;
    var edit_id="#edit_"+myid;
    var id="#"+myid;
    if (myurl!=""&&myurl!=null&&myurl!=undefined){
        var filename=myurl.replace(/.*(\/|\\)/, "");
        var fileExt=((/[.]/.exec(filename)) ? /[^.]+$/.exec(filename.toLowerCase()) : '')[0].toLowerCase();
        if($.inArray(fileExt, imgType)>=0){
            $(edit_id).attr("src", fileurl);
        }else if($.inArray(fileExt, excelType)>=0){
            $(edit_id).attr("src","/static/img/default_excel.png");
        }else if ($.inArray(fileExt, wordType)>=0) {
            $(edit_id).attr("src","/static/img/default_word.png");
        }else if($.inArray(fileExt, pptType)>=0){
            $(edit_id).attr("src","/static/img/default_ppt.png");
        }else if($.inArray(fileExt, videoType)>=0){
            $(edit_id).attr("src","/static/img/default_video.png");
        }else if($.inArray(fileExt, pdfType)>=0){
            $(edit_id).attr("src","/static/img/default_pdf.png");
        }else{
            $(edit_id).attr("src","/static/img/default_other.png");
        }
        $(id).val(fileurl);
    }else {
        $(edit_id).attr("src","/static/img/default_img.png");
        $(id).val(fileurl);
    }
}
/*单个图片预览或者附件下载初始化
* type 类型 src 或者 href
* myid 要赋值的标签id
* data 原始数据
* tablename 请求的表*/
function initHrefOrSrc(type,myid,data,tablename){
    var myurl="/getFile/?Fid="+data.substring(0,24)+"&FtableName="+tablename;
    $(myid).attr(type,myurl);
}
function returnStrHref(data,tablename){
    var filehref="/getFile/?Fid="+data.substring(0,24)+"&FtableName="+tablename;
    var dataname= data.substring(25,data.length);
    var myurl='<a href="' + filehref+ '" title="下载附件" style="margin-right: 5px;" role="button" download="' +dataname + '">'+dataname+'</a>'
    return myurl
}