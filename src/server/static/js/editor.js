const compileCodeBtn = document.querySelector('.editor__run');
const deployCodeBtn = document.querySelector('.editor__deploy');
const consoleLogList = document.querySelector('.editor__console-logs');


const editor = ace.edit("editor");
const defaultCode = `from pyteal import *

def approval():
    return Approve()
`;
const consoleMessages = [];

const editorLib = {
    init() {
        editor.session.setMode("ace/mode/python");

        editor.setOptions({
            enableBasicAutocompletion: true,
        });

        editor.setValue(defaultCode)
    },

    outputConsole(text) {
        consoleMessages.push({
            text
        })

        const newLog = document.createElement('li');
        const newLogText = document.createElement('pre');

        newLogText.className = "log log--string";
        newLogText.textContent = `> ${consoleMessages[0].text}`;

        newLog.appendChild(newLogText);
        consoleLogList.appendChild(newLog);
    },

    clearConsole() {
        consoleMessages.length = 0;

        // Remove all elements in the log list
        while (consoleLogList.firstChild) {
            consoleLogList.removeChild(consoleLogList.firstChild);
        }
    },
};


compileCodeBtn.addEventListener('click', () => {
    const userCode = editor.getValue();

    console.log(userCode);

    fetch("http://127.0.0.1:5000/compile", {
            body: JSON.stringify({
                "body": userCode,
            }),
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Accept": "application/json",
            },
            method: "POST",
            // mode: 'no-cors',
        }).then(response => response.text())
        .then(response => {
            console.log(response)
            editorLib.outputConsole(response)
        }).catch(err => {
            console.log(err.name);
            console.log(err.message);
        });
});

consoleLogList.addEventListener('dblclick', () => {
    // Clear the logs if double clicked
    console.log("Clear");
    editorLib.clearConsole();
});


editorLib.init();