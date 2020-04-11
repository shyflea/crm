var Main = {
    data() {
        const generateData = _ => {
            var data = [];
            const params = {};
            //获取岗位
            $.ajaxSettings.async = false;
            $.get("/ops/get_all_post", params, function (ret) {
                data = ret;
            });
            $.ajaxSettings.async = true;
            return data;
        };
        const existData = _ => {
            var data = [];
            const params = {'org_id': document.getElementById("org_id").value};
            //获取自身配置的岗位
            $.ajaxSettings.async = false;
            $.get("/ops/get_org_post_self", params, function (ret) {
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
    methods:{
    }
};
var Ctor = Vue.extend(Main);
new Ctor().$mount('#app');
