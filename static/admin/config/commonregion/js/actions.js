var Main = {
    data() {
        return {
            dialogFormVisible: false,
            form: {
                name: '',
                region: '',
                date1: '',
                date2: '',
                delivery: false,
                type: [],
                resource: '',
                desc: ''
            },
            formLabelWidth: '120px'
        };
    },
    methods: {
        // loadJsonFromFile: function(file, fileList) {
        //     this.uploadFilename = file.name;
        //     this.uploadFiles = fileList
        // },
        // loadJsonFromFileConfirmed:function() {
        //     console.log(this.uploadFiles);
        //     if (this.uploadFiles) {
        //         for (let i = 0; i < this.uploadFiles.length; i++) {
        //             let file = this.uploadFiles[i];
        //             console.log(file.raw);
        //             if (!file) continue;
        //             let reader = new FileReader();
        //             reader.onload = async (e) => {
        //                 try {
        //                     let document = JSON.parse(e.target.result);
        //                     console.log(document)
        //                 } catch (err) {
        //                     console.log(`load JSON document from file error: ${err.message}`);
        //                     this.showSnackbar(`Load JSON document from file error: ${err.message}`, 4000)
        //                 }
        //             };
        //             reader.readAsText(file.raw)
        //         }
        //     }
        //     dialogFormVisible = false
        // }
    }
}
var Ctor = Vue.extend(Main);
new Ctor().$mount('#app');
