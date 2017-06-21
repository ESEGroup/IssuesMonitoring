var express = require('express');
var bodyParser = require('body-parser');
var app = express();
app.use(bodyParser.urlencoded({ extended: false }));

app.get('/', function (req, res) {
  var data = "";
  res.on('data', function(chunk){
    data = chunk;
  });
  console.log(req.body);
  res.send('Hello World!');
});

app.post('/', function(req,res){
  var data = "";
  res.on('data', function(chunk){
    data = chunk;
  });
  console.log(req.body);
  res.send('Teste');
})

app.listen(8080, function () {
  console.log('Example app listening on port 8080!');
});
