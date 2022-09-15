const { createApp } = Vue



createApp({
    data() {
	return {
	    corpus_list: [],
	    epoch: 20,
	    window: 8,
	    base_url:   "/api/",
	    new_corpus_name : "NewCorpus",
	    current_corpus_name : "",
	    corpus_details : {},
	    to_upload_file : "",
	    loading : false,
	    keyword : "",
	    rand : 1
	}
    },
    beforeMount(){
	this.update_corpus();
    },
    computed: {
	get_image_url: function () {
	    console.log("img url");
	    return this.base_url+"/corpus/"+this.current_corpus_name+"/picture";
	}
    },
    methods: {
	async upload_file(e) {
	    this.loading = true;
	    console.log ("aaa");
	    this.to_upload_file = e.target.files || e.dataTransfer.files;
	    this.to_upload_file = this.to_upload_file[0];
	    console.log ("aaa");
	    console.log(this.to_upload_file);
	    this.loading = false;
	},
	async submit_file() {
	    this.loading = true;
	    let formData = new FormData();
	    console.log (this.to_upload_file);
	    formData.append('file', this.to_upload_file);
	    //formData.append('filename', this.to_upload_file.name);
	    console.log (formData);
	    res=await (await fetch (this.base_url+"/corpus/"+this.current_corpus_name, 
				    { method: "POST", 
				      headers: {
					  'Accept': 'application/json',
				      },
				      body: formData
				    }
				   ));
	    this.get_corpus_details(this.current_corpus_name);
	    this.loading = false;
	},
	async delete_file(file) {
	    var url = this.base_url+"/corpus/"+this.current_corpus_name+"/"+file;
	    var myInit = { method: 'DELETE'};
	    await (fetch(url, myInit));
	    this.get_corpus_details(this.current_corpus_name);
	},
	async update_corpus() {
	    const url = this.base_url+"/corpus";
	    this.corpus_list = await (await fetch(url)).json();
	},
	async create_corpus() {
	    url = this.base_url+"/corpus";
	    var myHeaders = new Headers();
	    myHeaders.append("Content-Type", "application/json");
	    var myInit = { method: 'POST',
			   headers: myHeaders,
			   mode: 'cors',
			   body: JSON.stringify({ "name": this.new_corpus_name }),
			   cache: 'default' };
	    await (fetch(url, myInit));
	    this.update_corpus();
	},
	async get_corpus_details(corpus_name) {
	    this.current_corpus_name = corpus_name;
	    url = this.base_url+"/corpus/"+corpus_name;
	    this.corpus_details = await(await fetch(url)).json();
	},
	async delete_corpus(corpus_name) {
	    url = this.base_url+"/corpus/"+corpus_name;
	    var myInit = { method: 'DELETE' };
	    await (fetch (url, myInit));
	    this.update_corpus();
	},
	async update_dict() {
	    this.loading = true;
	    url = this.base_url+"/corpus/"+this.current_corpus_name+"/dict";
	    var myHeaders = new Headers();
	    myHeaders.append("Content-Type", "application/json");
	    var myInit = { method: 'PUT',
			   headers: myHeaders,
			   body: JSON.stringify({
			       "epoch": this.epoch,
			       "window": this.window
			   })
			 };
	    await (fetch (url, myInit));
	    this.loading = false;
	},
	async update_image(corpus_name) {
	    this.loading = true;
	    url = this.base_url + "/corpus/"+this.current_corpus_name+"/picture/"+this.keyword;
	    var myInit = { method: 'PUT' };
            await (fetch (url, myInit));
	    this.rand = this.rand+1;
	    this.loading = false;
	}
    }
}).mount('#app')
