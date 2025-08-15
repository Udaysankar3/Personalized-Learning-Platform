function compileCode() {
    const code = editor.getValue();
    fetch('https://api.jdoodle.com/v1/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            script: code,
            language: 'python3', // or the language of your choice
            versionIndex: '3', // specify the version index based on JDoodle docs
            clientId: '9a8842421ed3a3550828de38f212c7e9',
            clientSecret: '4958b2f632d4d1ed0413f0fa1d3d6ff252fdbe1ae139e763c87b066a2964758'
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').innerText = data.output || data.error;
    })
    .catch(error => {
        document.getElementById('output').innerText = 'Error: ' + error.message;
    });
}
