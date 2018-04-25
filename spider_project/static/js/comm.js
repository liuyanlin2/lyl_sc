//去除字符串空格alert(s.NoSpace());
String.prototype.NoSpace = function() {
	return this.replace(/\s+/g, "");
}
//拼接字符串
function StringBuffer() {
    this._strs = new Array();
}
StringBuffer.prototype.append = function (str) {
    this._strs.push(str);
};
StringBuffer.prototype.arrayToString = function () {
    return this._strs.join("");
};
//url字符串截取为数组var Request = GetRequest();var menuid = Request["menuid"];
function GetRequest() {
    var url = location.search; //获取url中"?"符后的字串
    var theRequest = new Object();
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        strs = str.split("&");
        for (var i = 0; i < strs.length; i++) {
            theRequest[strs[i].split("=")[0]] = unescape(strs[i].split("=")[1]);
        }
    }
    return theRequest;
}
$(function () {
    //初始化头部菜单
    initTopMenus();
    //头部菜单栏的点击事件
    $(document).on("click", ".nav-home-title li", function () {
        var nextPage = $(this).index();
        $(".nav-home-title li").css("background", "");
        $(".nav-home-title li").eq(nextPage).css("background", "#000");
        $("#content").load($(this).data("url"),function(response,status,xhr){
            if(status=="success"){
                $(".content-main-left").css("height", $(window).height() - 65);
                $(".content-main-right").css("height", $(window).height() - 65);
            }else if(status=="error"){
                myAlertTop("加载错误，请稍后重试")
            }else if(status=="timeout"){
                myAlertTop("加载超时，请稍后重试")
            }
        });
    })
});

//页面尺寸改变时重新计算
$(window).resize(function () {
    $(".content-main-left").css("height", $(window).height() - 65);
    $(".content-main-right").css("height", $(window).height() - 65);
});


function toStr(str){
    if(str=="null" || str==null){
        return "";
    }else{
        return str;
    }
}
/*--------------初始化头部功能---------------*/
function initTopMenus() {
    var Request = GetRequest();
    var menuid = Request["menuid"];
    if (menuid === undefined || menuid === "") {
        return false;
    }
    $.getJSON("/getHomePermission/",{"FparentId":menuid}, function (responseData) {
        var htmlBuf = new StringBuffer();
        $.each(responseData.result, function (subindex, subitem) {
            if(subindex == 0){
                $("#page_title").text(subitem.FmenuName);
            } else if (subindex == 1) {
                htmlBuf.append('<li style="background: #000;" data-url="' + subitem.Furl + '">' + subitem.FmenuName + '</li>');
                $("#content").load(subitem.Furl,function(response,status,xhr){
                    if(status=="success"){
                        $(".content-main-left").css("height", $(window).height() - 65);
                        $(".content-main-right").css("height", $(window).height() - 65);
                    }else if(status=="error"){
                        myAlertTop("加载错误，请稍后重试")
                    }else if(status=="timeout"){
                        myAlertTop("加载超时，请稍后重试")
                    }
                });
            } else {
                htmlBuf.append('<li data-url="' + subitem.Furl + '">' + subitem.FmenuName + '</li>')
            }
        });
        $(".nav-home-title").html(htmlBuf.arrayToString().toString());
    });
}
/*-------------------头部自定义提示框------------------------------*/

function getListAlert(responseData) {
    if (responseData.istrue == "error") {
        myAlertTop(responseData.msg);
        return;
    }else if(responseData.istrue == "nodata"){
        myAlertTop(responseData.msg);
    }
}
function getModalListAlert(responseData) {
    if (responseData.istrue == "error") {
        myAlertTop(responseData.msg);
        return;
    }
}
function myAlertTop(title) {
    $("#myalert_text").text(title);
    $("#myalert").animate({top: "0px"}, 500);
    setTimeout(function () {
        $("#myalert").stop().animate({top: "-46px"}, 500)
    }, 2600);
}
function myBootboxAlert(msg) {
    bootbox.alert({
        title: '提示',
        message: msg,
        callback: function () { /* your callback code */
        }
    });
}
/************************省和市的初始化方法***************************/
function getOption(FparentId, id,initId) {
    //$.ajaxSettings.async = false;
    $.getJSON('/getChinaMap/', {"FparentId": FparentId}, function (responseData) {
        var htmlarry = new StringBuffer();
        $.each(responseData.result, function (index, item) {
            htmlarry.append('<option value="' + item.Fid + '">' + item.Fname + '</option>')
        });
        $(id).html(htmlarry.arrayToString().toString());
        if (initId!="0"){
            $(id).find("option[value='" + initId + "']").attr("selected", true);
        }
    })
}
/************************省和市的初始化方法***************************/
function initOption(FareaId) {
    var FprovinceId=FareaId.substring(0,2)+"0000";
    var FcityId=FareaId.substring(0,4)+"00";
    getOption("0", "#FprovinceId",FprovinceId);
    getOption(FprovinceId, "#FcityId",FcityId);
    getOption(FcityId, "#FareaId",FareaId);
}
/************************绑定部门的方法***************************/
function getDptOption(FparentId,id,initId){
    $.getJSON('/affairs_sys/dpt_mgr/getDptByFparentId/', {"FparentId": FparentId,"random":Math.random()}, function (responseData) {
        var htmlarry = new StringBuffer();
        $.each(responseData.result, function (index, item) {
            htmlarry.append('<option value="' + item.Fid + '">' + item.Fname + '</option>')
        });
        $(id).html(htmlarry.arrayToString().toString());
        if (initId!="0"){
            $(id).find("option[value='" + initId + "']").attr("selected", true);
        }
    })
}
/************************省部门初始化方法***************************/
function  initDptOption(Fid){
    var FperentId=Fid.substring(0,6);
    getDptOption("101","#Funit",FperentId);
    getDptOption(FperentId,"#Fdpt",Fid)
}
/*****************************绑定民族的方法********************************/
function initNation(domid, selectValue) {
    $.getJSON("/static/json/nation.json", function (data) {
        var htmlbufer = new StringBuffer();
        $.each(data, function (index, item) {
            htmlbufer.append("<option value='" + item.value + "'>" + item.value + "</option>");
        });
        $(domid).html(htmlbufer.arrayToString().toString());
        $(domid).val(selectValue);
    });
}
/**
 * 退出登录
 */
function userLogout() {
    window.location.href = "/affairs_sys/user_mgr/userLogout/";
}

/**
 *修改密码
 */
$("#btn_updatePwd").bind("click", function () {
    $("#form_updPwd").ajaxSubmit({
        //target: '#Tip', //后台将把传递过来的值赋给该元素
        url: "/affairs_sys/user_mgr/editUserPwdById/", //提交给哪个执行
        type: 'POST',
        beforeSubmit: function () {
            if (!/[\@A-Za-z0-9\!\#\$\%\^\&\*\.\~]{6,20}/.test($('#FpwdOld').val())) {
                myAlertTop('密码格式不正确');
                return false;
            }
            if (!/[\@A-Za-z0-9\!\#\$\%\^\&\*\.\~]{6,20}/.test($('#FpwdNew').val())) {
                myAlertTop('新密码格式不正确，请重新输入！');
                return false;
            }
            if ($('#FpwdNew').val() != $('#FpwdNewOk').val()) {
                myAlertTop('两次输入密码不正确，请重新输入！');
                return false;
            }
        },  // pre-submit callback
        success: function (data) {
            myAlertTop(data.msg)
            if (data.istrue === "success") {
                $("#form_updPwd").resetForm();
                $('#modal_updPwd').modal("hide");
            }
        }, //显示操作提示
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            myAlertTop("提交异常" + errorThrown.toString());
        }
    });
});
/****************************************时间格式化***************************************************/
/**
 * Created by 1 on 2016/4/12.
 */
//格式化当前日期
Date.prototype.Format = function (fmt) { //author: meizz
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "H+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}
//格式化当前时间并减去几天
Date.prototype.FormatMinus = function (fmt,mdays) { //author: meizz
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate()+mdays, //日
        "H+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}
//格式化当前时间并减去几个月
Date.prototype.FormatMinusMonth = function (fmt,mMonth) { //author: meizz
    var o = {
        "M+": this.getMonth() + 1 + mMonth, //月份
        "d+": this.getDate(), //日
        "H+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}
function dateFormat(dateString, format) {
    if (dateString!=null){
        return new Date(dateString.replace("T"," ")).Format(format)
    }else {
        return " "
    }

}
