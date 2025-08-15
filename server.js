const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const fs = require('fs');

const app = express();
app.use(bodyParser.json());

// Endpoint to handle code execution
app.post('/run', (req, res) => {
    const { language, code } = req.body;

    // Map language to filename and execution command
    const langMap = {
        python: { ext: 'py', cmd: 'python' },
        javascript: { ext: 'js', cmd: 'node' },
        cpp: { ext: 'cpp', cmd: 'g++' },
        java: { ext: 'java', cmd: 'javac' }
    };

    if (!langMap[language]) {
        return res.status(400).json({ error: 'Unsupported language' });
    }

    const { ext, cmd } = langMap[language];
    const filename = `temp.${ext}`;

    // Write code to file
    fs.writeFile(filename, code, (err) => {
        if (err) {
            return res.status(500).json({ error: 'File write error' });
        }

        let executeCmd;
        if (language === 'cpp') {
            // Compile C++ code and then run the executable
            executeCmd = `${cmd} ${filename} -o temp.out && ./temp.out`;
        } else if (language === 'java') {
            // Compile Java code and then run the .class file
            executeCmd = `${cmd} ${filename} && java temp`;
        } else {
            // Run Python and JavaScript directly
            executeCmd = `${cmd} ${filename}`;
        }

        // Execute the command
        exec(executeCmd, (error, stdout, stderr) => {
            // Clean up temporary files
            fs.unlinkSync(filename);
            if (language === 'cpp') fs.unlinkSync('temp.out');
            if (language === 'java') fs.unlinkSync('temp.class');

            if (error) {
                res.json({ output: stderr || error.message });
            } else {
                res.json({ output: stdout || stderr });
            }
        });
    });
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
