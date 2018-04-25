/**
 * Created by 1 on 2016/6/26.
 */

/**
 * 定义全局变量，是否提交
 */
var ValidateHelper = function () {
    var isSubmit = true;
    this.setIsSubmit = function (value) {
        isSubmit = value;
    }
    this.getIsSubmit = function () {
        return isSubmit;
    }
}
var myValidate = new ValidateHelper();
/**
 * 页面加载时，开启验证
 * @param form
 */
function initValidate(form) {
    $.each(form.find("input"), function (index, item) {
        $(item).off("blur").blur(function () {
            validate(item);
        })
    });
}

/**
 * 提交时，验证
 * @param form
 */
function validateSubmit(form) {
    myValidate.setIsSubmit(true);
    $.each(form.find("input"), function (index, item) {
        validate(item);
        if (validateRequire(item) != 2) {
            myValidate.setIsSubmit(false)
        } else if (validatePhone(item) != 2) {
            myValidate.setIsSubmit(false)
        } else if (validateCard(item) != 2) {
            myValidate.setIsSubmit(false)
        } else if (validateInt(item) != 2) {
            myValidate.setIsSubmit(false)
        }
    });
    console.info(myValidate.getIsSubmit())
    return myValidate.getIsSubmit();
}

/**
 * 验证方法
 * @param item
 */
function validate(item) {
    $(item).prev("span,.span-validate").remove();
    $(item).next("span,.span-validate").remove();
    if (validateRequire(item) == 0) {
        $(item).before('<span class="span-validate" style="color:red;"><img style="width: 20px;height: 20px;" src="/static/img/error.png" />必填</span>');
    } else if (validateRequire(item) == 1) {
        $(item).after('<span class="span-validate" style="color:red;"><img style="width: 20px;height: 20px;" src="/static/img/error.png" />必填</span>');
    } else if (validatePhone(item) == 0) {
        $(item).before('<span class="span-validate" style="color:red;"><img style="width: 20px;height: 20px;" src="/static/img/error.png" />格式错误</span>');
    } else if (validatePhone(item) == 1) {
        $(item).after('<span class="span-validate" style="color:red;"><img style="width: 20px;height: 20px;" src="/static/img/error.png" />格式错误</span>');
    } else if (validateCard(item) == 0) {
        $(item).before('<span class="span-validate" style="color:red;"><img style="width: 20px;height: 20px;" src="/static/img/error.png" />格式错误</span>');
    } else if (validateCard(item) == 1) {
        $(item).after('<span class="span-validate" style="color:red;"><img style="width: 20px;height: 20px;" src="/static/img/error.png" />格式错误</span>');
    } else if (validateInt(item) == 0) {
        $(item).before('<span class="span-validate" style="color:red;"><img style="width: 20px;height: 20px;" src="/static/img/error.png" />必须为整数</span>');
    } else if (validateInt(item) == 1) {
        $(item).after('<span class="span-validate" style="color:red;"><img style="width: 20px;height: 20px;" src="/static/img/error.png" />必须为整数</span>');
    }
}

/**
 * 验证非空
 * @param item
 * @returns {number}
 */
function validateRequire(item) {
    if ($(item).hasClass("validate_require") && $(item).val() === "") {
        return 0;
    } else if ($(item).hasClass("validate_require_after") && $(item).val() === "") {
        return 1;
    }
    return 2;
}

/**
 * 验证身份证
 * @param item
 * @returns {number}
 */
function validateCard(item) {
    if ($(item).hasClass("validate_card") && $(item).val() != "" && !isCard($(item).val())) {
        return 0;
    } else if ($(item).hasClass("validate_card_after") && $(item).val() != "" && !isCard($(item).val())) {
        return 1;
    }
    return 2;
}

/**
 * 验证电话
 * @param item
 * @returns {number}
 */
function validatePhone(item) {
    if ($(item).hasClass("validate_phone") && $(item).val() != "" && !isMobilePhone($(item).val())) {
        return 0;
    } else if ($(item).hasClass("validate_phone_after") && $(item).val() != "" && !isMobilePhone($(item).val())) {
        return 1;
    }
    return 2;
}

/**
 * 验证电话
 * @param item
 * @returns {number}
 */
function validateInt(item) {
    if ($(item).hasClass("validate_int") && $(item).val() != "" && !isInt($(item).val())) {
        return 0;
    } else if ($(item).hasClass("validate_int_after") && $(item).val() != "" && !isInt($(item).val())) {
        return 1;
    }
    return 2;
}

var regMobilePhone = /^1\d{10}$/;
var regTelPhone = /^((0\d{2,3})-)?(\d{7,8})(-(\d{3,}))?$/;
var regCard = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
var regInt = /^-?[1-9]\d*$/;


//检查是否整数
function isInt(str) {
    if (regInt.test(str)) {
        return true;
    }
    return false;
}
function isMobilePhone(str) {
    if (regMobilePhone.test(str)) {
        return true;
    }
    return false;
}

function isPhone(str) {
    if (regMobilePhone.test(str) || regTelPhone.test(str)) {
        return true;
    }
    return false;
}

function isCard(str) {
    if (regCard.test(str)) {
        return true;
    }
    return false;
}