const socket = io.connect();
let processor = null;
let localstream = null;
var context = new (window.AudioContext || window.webkitAudioContext)({
    sampleRate: 44100
  });
var initial_delay_sec = 0;
var scheduled_time = 0;

function startRecording() {
    console.log('start recording');
    socket.emit('start', { 'sampleRate': context.sampleRate });

    navigator.mediaDevices.getUserMedia({ audio: true, video: false }).then((stream) => {
        localstream = stream;
        const input = this.context.createMediaStreamSource(stream);
        processor = context.createScriptProcessor(256, 1, 1);

        input.connect(processor);
        processor.connect(context.destination);

        processor.onaudioprocess = (e) => {
            const voice = e.inputBuffer.getChannelData(0);
            socket.emit('send_pcm', voice.buffer);
        }
    }).catch((e) => {
        // "DOMException: Rrequested device not found" will be caught if no mic is available
        console.log(e);
    })
}

function stopRecording() {
    console.log('stop recording');
    processor.disconnect();
    processor.onaudioprocess = null;
    processor = null;
    localstream.getTracks().forEach((track) => {
        track.stop();
    })
    socket.emit('stop', '', (res) => {
        console.log(`Audio data is saved as ${res.filename}`);
    })
}

function startSample() {
    socket.emit('start_sample');
}

socket.on('sample_message', (evt) => {
    data = Object.entries(evt).map(([key, value]) => value);
    playAudioStream(data);
});

socket.on('get_result', (msg) => {
    $('#messages').append($('<li>').text(msg));
});

function playChunk(audio_src, scheduled_time) {
    if (audio_src.start) {
        audio_src.start(scheduled_time);
    } else {
        audio_src.noteOn(scheduled_time);
    }
}

function playAudioStream(audio_f32) {
    var audio_buf = context.createBuffer(1, audio_f32.length, 44100);
    var audio_src = context.createBufferSource();
    var current_time = context.currentTime;

    audio_buf.getChannelData(0).set(audio_f32);

    audio_src.buffer = audio_buf;
    audio_src.connect(context.destination);

    if (current_time < scheduled_time) {
        playChunk(audio_src, scheduled_time);
        scheduled_time += audio_buf.duration;
    } else {
        playChunk(audio_src, current_time);
        scheduled_time = current_time + audio_buf.duration + initial_delay_sec;
    }
}

function touchStart() {
    
}