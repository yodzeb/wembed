const { createApp } = Vue

createApp({
    data() {
	return {
            message: 'Hello Vue!',
	    corpus_list: ['a','b'],
	    base_url:   "/api/"

	}
    },
    methods: {
	async update_corpus() {
	    const url = this.base_url+"/corpus";
	    this.corpus_list = await (await fetch(url)).json();
	},
	greet() {
	    console.log("aaa");
	    alert("bla");
	}
    }
}).mount('#app')
