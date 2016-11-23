new Vue({
  delimiters: ['{{!', '}}']
})

var app = new Vue({
  el: '#app',
  data: {
    todos: [
    ],
    message: 'Input your desired Strings'
  },
  methods: {
  	calculation: function(){
  		var ws = new WebSocket("ws://localhost:8200/ws");
      ws.onopen = function() {
         ws.send(app.message);
      };
      ws.onmessage = function (evt) {
         app.todos.push({ text: evt.data })
      };
  	}
  }
})

