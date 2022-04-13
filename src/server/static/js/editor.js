const compileCodeBtn = document.querySelector('.editor__run');
const deployCodeBtn = document.querySelector('.editor__deploy');
const consoleLogList = document.querySelector('.editor__console-logs');


const editor = ace.edit("editor");
const viewer = ace.edit("viewer");

const defaultPyteal = `from pyteal import *

def event(
    init: Expr = Reject(),
    delete: Expr = Reject(),
    update: Expr = Reject(),
    opt_in: Expr = Reject(),
    close_out: Expr = Reject(),
    no_op: Expr = Reject(),
) -> Expr:
    return Cond(
        [Txn.application_id() == Int(0), init],
        [Txn.on_completion() == OnComplete.DeleteApplication, delete],
        [Txn.on_completion() == OnComplete.UpdateApplication, update],
        [Txn.on_completion() == OnComplete.OptIn, opt_in],
        [Txn.on_completion() == OnComplete.CloseOut, close_out],
        [Txn.on_completion() == OnComplete.NoOp, no_op],
    )

def approval():
    return event(init=Seq([
        Approve()
    ]))
`;

const defaultTeal = `#pragma version 6
txn ApplicationID
int 0
==
bnz main_l12
txn OnCompletion
int DeleteApplication
==
bnz main_l11
txn OnCompletion
int UpdateApplication
==
bnz main_l10
txn OnCompletion
int OptIn
==
bnz main_l9
txn OnCompletion
int CloseOut
==
bnz main_l8
txn OnCompletion
int NoOp
==
bnz main_l7
err
main_l7:
int 0
return
main_l8:
int 0
return
main_l9:
int 0
return
main_l10:
int 0
return
main_l11:
int 0
return
main_l12:
int 1
return
`

const consoleMessages = [];

const editorLib = {
    init() {
        editor.getSession().setMode("ace/mode/python");

        //TODO: can we define our own mode? formatting? syntax highlighting?
        viewer.getSession().setMode("ace/mode/python");

        editor.setOptions({
            enableBasicAutocompletion: true,
        });

        viewer.setReadOnly(true);

        editor.setValue(defaultPyteal)
        viewer.setValue(defaultTeal)

        this.outputConsole(`double click to clear the console logs`);
    },

    outputConsole(text) {
        consoleMessages.push({
            text
        });

        const newLog = document.createElement('li');
        const newLogText = document.createElement('pre');

        newLogText.className = "log log--string";
        newLogText.textContent = `> ${consoleMessages[consoleMessages.length-1].text}`;

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

    fetch("/compile", {
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
        }).then(response => response.text())
        .then(response => {
            parsed = JSON.parse(response)
            console.log(parsed)

            viewer.setValue(parsed['teal'])
            editorLib.outputConsole(response)
        }).catch(err => {
            console.log(err.name);
            console.log(err.message);
        });
});

deployCodeBtn.addEventListener('click', () => {
    const userCode = editor.getValue();

    console.log(userCode);

    fetch("/deploy", {
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
    editorLib.clearConsole();
});


editorLib.init();