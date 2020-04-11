var Main = {
    data() {
        const generateData = _ => {
            var data = [];
            const params = {};
            //获取权限
            $.ajaxSettings.async = false;
            $.get("/ops/get_all_privs", params, function (ret) {
                data = ret;
            });
            $.ajaxSettings.async = true;
            return data;
        };
        const existData = _ => {
            var data = [];
            const params = {
                'grant_obj_id': $('#grantObjId').val(),
                'grant_obj_type': $('#grantObjType').val()
            };
            //获取已拥有的权限
            $.ajaxSettings.async = false;
            $.get("/ops/get_exist_privs", params, function (ret) {
                data = ret;
            });
            $.ajaxSettings.async = true;
            return data;
        };
        return {
            data: generateData(),
            value: existData(),
            filterMethod(query, item) {
                return item.label.indexOf(query) > -1 | item.pingyin.indexOf(query) > -1;
            }
        };
    },
    methods: {
        savePrivs: function (event) {
            var params = {
                'priv_ids': this.value,//选择的权限
                'grant_obj_id': $('#grantObjId').val(),
                'grant_obj_type': $('#grantObjType').val(),
                'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']")[0].value
            };
            $.post("/ops/save_grant/", params, function (ret) {
                if (ret.status == 1) {
                    window.location.href = ret.url;
                } else {
                    Vue.prototype.$message.error(ret.msg);
                }
            });

        }
    }
};
var Ctor = Vue.extend(Main);
new Ctor().$mount('#app');

