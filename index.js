const express = require('express');
const http = require('http');
const path = require('path');
const socketio = require('socket.io');
const spawn = require("child_process").spawn;
const fs = require('fs');
const app = express();
const fft_frame = 441;

var pcm = require('pcm');

app.use('/', express.static(path.join(__dirname, 'public')));

server = http.createServer(app).listen(8080, function() {
    console.error('Example app listening on port 8080');
})

const io = socketio.listen(server);

io.on('connection', (socket) => {
    let sampleRate = 44100;
    let buffer = [];
    var pythonProcess = spawn('python3',["find_hit.py"]);
    pythonProcess.stdout.setEncoding('utf-8');
    var fft_idx = 0;
    var fname = new Date().getTime();
    var wfs = fs.createWriteStream('template_file', 'utf8');

    socket.on('start', (data) => {
        sampleRate = data.sampleRate;
        fft_idx = 0;
        fname = new Date().getTime();
        var wfs = fs.createWriteStream(String(fname), 'utf8');
    });

    socket.on('send_pcm', (data) => {
        const itr = data.values();
        for (var i = 0; i < data.length; i++) {
            fft_idx += 1;
            wfs.write(String(itr.next().value));
            wfs.write('\n');
            if (fft_idx == fft_frame) {
                wfs.end();
                fft_idx = 0;
                pythonProcess.stdin.write(String(fname)+'\n');
                while (String(fname) == String(new Date().getTime())) {}
                fname = new Date().getTime();
                wfs = fs.createWriteStream(String(fname), 'utf8');
            }
        }
    });

    socket.on('stop', (data, ack) => {
        fft_idx = 0;
        wfs.end();
        // pythonProcess.stdin.write('complete\n');
    });

    socket.on('start_sample', () => {
        // var fname = new Date().getTime();
        fname = 0;
        var wfs = fs.createWriteStream(String(fname), 'utf8');
        var buf = new Float32Array(4096);
        var idx = 0;
        fft_idx = 0;
        pcm.getPcmData('public/sample/sample_fresco.wav', { stereo: false, sampleRate: 44100 },
            function(sample, channel) {
                buf[idx++] = sample;
                fft_idx += 1;
                wfs.write(String(sample));
                wfs.write('\n');
                if (idx == buf.length) {
                    socket.emit('sample_message', buf);
                    buf = new Float32Array(4096);
                    idx = 0;
                }
                if (fft_idx == fft_frame) {
                    fft_idx = 0;
                    wfs.end();
                    pythonProcess.stdin.write(String(fname)+'\n');
                    fname += 1;
                    wfs = fs.createWriteStream(String(fname), 'utf8');
                }
            },
            function() {
                fft_idx = 0;
                wfs.end();
                // pythonProcess.stdin.write('complete\n');
            }
        );
    });
    pythonProcess.stdout.on('data', (data) => {
        var rm_paths = data.split('\n');
        
        for (let rm_path of rm_paths) {
            if (rm_path.match(/OK/)) {
                rm_path = rm_path.replace('OK', '');
                socket.emit('get_result', rm_path);
            }
            
            fs.unlink(rm_path, (err) => {
                //console.error(err);
            });
            
        }
    });
})


// Convert byte array to Float32Array
const toF32Array = (buf) => {
    const buffer = new ArrayBuffer(buf.length);
    const view = new Uint8Array(buffer);
    for (var i = 0; i < buf.length; i++) {
        view[i] = buf[i];
    }
    return new Float32Array(buffer);
}

