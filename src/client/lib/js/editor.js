const compileCodeBtn = document.querySelector('.editor__run');
const deployCodeBtn = document.querySelector('.editor__deploy');

const editor = ace.edit("editor");
const defaultCode = `from pyteal import *

def approval():
    return Approve()
`;
const editorLib = {
    init() {
        editor.session.setMode("ace/mode/python");

        editor.setOptions({
            enableBasicAutocompletion: true,
        });

        editor.setValue(defaultCode)
    }
};


compileCodeBtn.addEventListener('click', () => {
    const userCode = editor.getValue();

    console.log(userCode);
});


editorLib.init();