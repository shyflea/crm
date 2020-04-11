new Vue({
    el: '#app',
    data() {
        return {
            searchInput: ''
        }
    },
    methods: {
        //删除缓存
        clearCache: function (cacheName) {
            $('#cacheName').val(cacheName);
            document.getElementById('cacheForm').submit();
        },
        //查询缓存
        searchCache: function (event) {
            document.getElementById('searchForm').submit();
        }
    }
});

