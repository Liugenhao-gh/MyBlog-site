function showLogin(){
    $("#llogin").addClass("active");
    $("#rresign").removeClass("active");
    $("#ffind").removeClass("active");
    $("#login").addClass("active");
    $("#resign").removeClass("active");
    $("#find").removeClass("active");
    $("#mymodal").modal('show');
}

function  showReg() {
    $("#llogin").removeClass("active");
    $("#rresign").addClass("active");
    $("#ffind").removeClass("active");
    $("#login").removeClass("active");
    $("#resign").addClass("active");
    $("#find").removeClass("active");
    $("#mymodal").modal('show')
}

function showReset() {
    $("#llogin").removeClass("active");
    $("#rresign").removeClass("active");
    $("#ffind").addClass("active");
    $("#login").removeClass("active");
    $("#resign").removeClass("active");
    $("#find").addClass("active");
    $("#mymodal").modal("show");
}

function dosendmail(obj) {
    var email = $.trim($("#regname").val());
    if(!email.match(/.+@.+\..+/)){
        window.alert("邮箱格式错误");
        $("#regname").focus()
        return false;
    }
    $.post('/ecode', 'email=' + email, function (data) {
        if(data == 'email-invaild'){
            window.alert("邮箱格式错误");
            $("#regname").focus()
            return false;
        }
        if(data == 'send-pass'){
            window.alert("发送成功，请查收");
            $("#regname").attr('disabled', true);//验证码发送后禁止修改注册邮箱
            $(obj).attr('disabled', true);//发送邮件按钮不可用
            return false;
        }
        else{
            window.alert("发送失败");
        }

    })

}

function doReg(e) {
    if (e != null && e.keyCode != 13){
        return false;
    }
    var regname = $.trim($("#regname").val());
    var regpass = $.trim($("#regpass").val());
    var regcode = $.trim($("#regcode").val());

    if(!regname.match(/.+@.+\..+/) || regpass.length <5){
        window.alert("注册邮箱不正确或密码长度少于5位");
        return false;
    }
    else {
        //构件post请求的正文数据
        param = "username=" + regname;
        param += "&password=" + regpass;
        param += "&code=" + regcode;
        //利用jQuery框架发送post请求，并获取到后台注册接口的响应内容
        $.post('/user', param, function (data) {
            if(data == "ecode-error"){
                window.alert("验证码无效");
                $("#regcode").val('');//清空验证码
                $("#regcode").focus();
            }
            else if (data == "up-invalid"){
                window.alert("用户名和密码格式不正确，密码不能少于5位");
            }
            else if(data == "user-repeated"){
                window.alert("该用户已被注册");
                $("#regname").val('')
                $("#regname").focus();
            }
            else if(data == "reg-pass"){
                window.alert("注册成功");
                //注册成功,刷新当前页面
                setTimeout('location.reload();',1000);

            }
            else if(data == "reg-fail"){
                window.alert("注册失败，请联系管理员");
            }

        })

    }

}
function dologin(e) {
    if (e !=null && e.keyCode != 13){
        return false;
    }
    loginname = $.trim($("#loginname").val());
    loginpass = $.trim($("#loginpass").val());
    logincode = $.trim($("#logincode").val());
    if (loginname.length < 5 || loginpass.length < 5){
        window.alert("用户名或密码少于5位");
        return false;
    }
    else{
        //构建POST请求正文数据
        param = "username=" + loginname;
        param += "&password=" + loginpass;
        param += "&logincode=" + logincode;
        //利用jQuery发送post请求，获取到后台接口响应到的数据
        $.post('/login', param, function (data) {
         if (data == "vcode-error"){
                    window.alert("验证码无效");
                    $("#logincode").val('');
                    $("#logincode").focus();
                }
                else if (data == "login-pass"){
                    window.alert("登录成功");
                    setTimeout('location.reload();', 1000);
                }
                else if (data == "login-fail"){
                    window.alert("登录失败")
                }
        })
    }
}