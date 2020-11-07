const spawn = require("child_process").spawn;

var pythonProcess = spawn('python3',["find_hit.py"]);

pythonProcess.stdin.write('aaaa\n');

pythonProcess.stdout.on('data', (data) => {
    console.log('a');
});

pythonProcess.on('error', function (err) {
    console.error(err);
});

pythonProcess.on('exit', function (code) {
    console.log('child process exited.');
});