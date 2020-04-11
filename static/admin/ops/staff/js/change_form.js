//系统账号由用户名自动转拼音生成
document.getElementById('id_staff_name').onblur = function () {
    const data={'chinese':$("#id_staff_name").val()}
    $.get("/common/pingyin", data, function (ret) {
        $("#id_systemuser-0-sys_user_code").val(ret)
    });
}

var Role = {
    data() {
        const generateData = _ => {
            var data = [];
            const params = {};
            //获取岗位
            $.ajaxSettings.async = false;
            $.get("/ops/get_system_roles", params, function (ret) {
                data = ret;
            });
            $.ajaxSettings.async = true;
            return data;
        };
        const existData = _ => {
            var data = [];
            const params = {'staff_id': $('#staff_id').val()};
            //获取员工当前角色
            $.ajaxSettings.async = false;
            $.get("/ops/get_system_user_roles", params, function (ret) {
                data = ret;
            });
            $.ajaxSettings.async = true;
            return data;
        };
        return {
            systemRoles: generateData(),
            checkedRoles: existData()
        };
    }
};
var Ctor = Vue.extend(Role);
new Ctor().$mount('#roleApp');

/**
 * 初始化设置岗位
 * */
function setUserPost(){
    var data = [];
    const params = {'org_id': $('#id_org').val()};
    //获取岗位
    $.ajaxSettings.async = false;
    $.get("/ops/get_org_post", params, function (ret) {
        data = ret;
        $("#postSelect").empty();
        $('#postSelect').append("<option>请选择</option>")
        for(var i=0;i<data.length;i++){
            $('#postSelect').append("<option value='"+data[i].sys_post_id+"'>"+data[i].sys_post_name+"</option>")
        }
    });
    const params2 = {'staff_id': $('#staff_id').val()};
    //获取用户当前岗位
    $.get("/ops/get_system_user_post", params2, function (ret) {
        $("#postSelect").val(ret);
    });
    $.ajaxSettings.async = true;
}
setUserPost();
$(document).on("change","#id_org",function(){
　 setUserPost();
});
