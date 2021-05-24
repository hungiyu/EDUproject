let express = require('express');
let app = express();
let router = express.Router();
let exec = require('child_process').exec;
let port = 9000;

app.use(express.static(__dirname + '/public'));

router.get('/', function (req, res, next) {
    //預設頁面
});
router.get('/start', function (req, res, next) {
    
    exec('python ~/mycar/manage.py drive --model ~/mycar/models/mypilot0308_base.h5', 
    function (err, stdout, stderr) {
        
        res.sendFile(__dirname+'/public/index.html');

    });

//res.sendFile(__dirname+'/public/index.html');

});

app.use('/', router);
var server = app.listen(port, function () {
    console.log('Node server is running..');
});