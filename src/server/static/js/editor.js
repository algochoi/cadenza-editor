const compileCodeBtn = document.querySelector(".editor__run");
const deployCodeBtn = document.querySelector(".editor__deploy");
const consoleLogList = document.querySelector(".editor__console-logs");

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
`;

const consoleMessages = [];

const editorLib = {
  init() {
    editor.getSession().setMode("ace/mode/python");

    //TODO: can we define our own mode? formatting? syntax highlighting?
    let TealMode = ace.require("ace/mode/algorand_teal").Mode
    viewer.getSession().setMode(new TealMode());

    editor.setOptions({
      enableBasicAutocompletion: true,
    });

    viewer.setReadOnly(true);

    editor.setValue(defaultPyteal);
    viewer.setValue(defaultTeal);

    this.outputConsole(`double click to clear the console logs`);
  },

  outputConsole(text) {
    consoleMessages.push({
      text,
    });

    const newLog = document.createElement("li");
    const newLogText = document.createElement("pre");

    newLogText.className = "log log--string";
    newLogText.textContent = `> ${
      consoleMessages[consoleMessages.length - 1].text
    }`;

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

compileCodeBtn.addEventListener("click", () => {
  const userCode = editor.getValue();


  fetch("/compile", {
    body: JSON.stringify({
      body: userCode,
    }),
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type",
      Accept: "application/json",
    },
    method: "POST",
  })
    .then((response) => response.text())
    .then((response) => {
      parsed = JSON.parse(response);
      viewer.setValue(parsed["teal"]);
      editorLib.outputConsole(response);
    })
    .catch((err) => {
      console.error(err.name);
      console.error(err.message);
    });
});

deployCodeBtn.addEventListener("click", () => {
  const userCode = editor.getValue();

  console.log(userCode);

  fetch("/deploy", {
    body: JSON.stringify({
      body: userCode,
    }),
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type",
      Accept: "application/json",
    },
    method: "POST",
  })
    .then((response) => response.text())
    .then((response) => {
      editorLib.outputConsole(response);
    })
    .catch((err) => {
      console.error(err.name);
      console.error(err.message);
    });
});

consoleLogList.addEventListener("dblclick", () => {
  // Clear the logs if double clicked
  editorLib.clearConsole();
});

(function(){

ace.define(
  "ace/mode/algorand_teal_highlight_rules",
  [
    "require",
    "exports",
    "module",
    "ace/lib/oop",
    "ace/mode/text_highlight_rules",
  ],
  function (require, exports, module) {
    "use strict";

    var oop = require("../lib/oop");
    var TextHighlightRules =
      require("./text_highlight_rules").TextHighlightRules;

    var AlgorandTEALHighlightRules = function () {
      // regexp must not have capturing parentheses. Use (?:) instead.
      // regexps are ordered -> the first match is used

      this.$rules = {
        start: [
          {
            token: "comment.line.teal",
            regex: /\/\/.*?$/,
          },
          {
            include: "#keywords",
          },
          {
            include: "#branch",
          },
          {
            include: "#branch-target",
          },
          {
            include: "#addr",
          },
          {
            include: "#base32",
          },
          {
            include: "#base64",
          },
          {
            include: "#address-string",
          },
        ],
        "#keywords": [
          {
            token: "keyword.function.teal",
            regex:
              /\b(?:int|byte|intcblock|intc|intc_0|intc_1|intc_2|intc_3|bytecblock|bytec|bytec_0|bytec_1|bytec_2|bytec_3|arg|arg_0|arg_1|arg_2|arg_3|txn|txna|gtxn|gtxna|global)\b/,
          },
          {
            token: "entity.name.function.teal",
            regex:
              /\b(?:sha256|keccak256|sha512_256|ed25519verify|len|itob|btoi|mulw)\b/,
          },
          {
            token: "entity.name.function.teal",
            regex:
              /\b(?:Sender|Fee|FirstValid|FirstValidTime|LastValid|Note|Lease|Receiver|Amount|CloseRemainderTo|VotePK|VoteFirst|VoteLast|VoteKeyDilution|Type|TypeEnum|XferAsset|AssetAmount|AssetSender|AssetReceiver|AssetCloseTo|GroupIndex|TxID|ApplicationID|OnCompletion|ApplicationArgs|NumAppArgs|Accounts|NumAccounts|ApprovalProgram|ClearStateProgram|RekeyTo|ConfigAsset|ConfigAssetTotal|ConfigAssetDecimals|ConfigAssetDefaultFrozen|ConfigAssetUnitName|ConfigAssetName|ConfigAssetURL|ConfigAssetMetadataHash|ConfigAssetManager|ConfigAssetReserve|ConfigAssetFreeze|ConfigAssetClawback|FreezeAsset|FreezeAssetAccount|FreezeAssetFrozen)\b/,
          },
          {
            token: "entity.name.function.teal",
            regex:
              /\b(?:MinTxnFee|MinBalance|MaxTxnLife|ZeroAddress|GroupSize|LogicSigVersion|Round|LatestTimestamp|CurrentApplicationID)\b/,
          },
          {
            token: "support.function.teal",
            regex: /\b(?:load|store|pop|dup)\b/,
          },
          {
            token: "keyword.control.teal",
            regex: /\berr\b/,
          },
          {
            token: "constant.numeric.teal",
            regex: /\b(?:0|[1-9][0-9]*)\b/,
          },
          {
            token: "keyword.operator.teal",
            regex: /\+|\-|\*|\/|<=|>=|<|>|&&|\|\||==|!=|!|%|\||&|\^|~/,
          },
        ],
        "#branch": [
          {
            token: "keyword.control.teal",
            regex: /bnz\s+/,
            push: [
              {
                token: "text",
                regex: /$/,
                next: "pop",
              },
              {
                token: "variable.parameter",
                regex: /[a-zA-Z_][a-zA-Z0-9_]*/,
              },
            ],
          },
        ],
        "#branch-target": [
          {
            token: "variable.parameter",
            regex: /[a-zA-Z_][a-zA-Z0-9_]*:/,
          },
        ],
        "#addr": [
          {
            token: "entity.name.type.teal",
            regex: /addr\s+/,
            push: [
              {
                token: "text",
                regex: /$/,
                next: "pop",
              },
              {
                include: "#address-string",
              },
            ],
          },
        ],
        "#address-string": [
          {
            token: "string.addr.teal",
            regex: /[0-9A-Z]{58}/,
          },
        ],
        "#base32": [
          {
            token: "entity.name.type.teal",
            regex: /(?:base32|bs32)(?:\s+|\()/,
            push: [
              {
                token: "text",
                regex: /$/,
                next: "pop",
              },
              {
                include: "#base32-string",
              },
            ],
          },
        ],
        "#base32-string": [
          {
            token: "string.base32.teal",
            regex: /[A-Z2-7]*/,
          },
        ],
        "#base64": [
          {
            token: "entity.name.type.teal",
            regex: /(?:base64|bs64)(?:\s+|\()/,
            push: [
              {
                token: "text",
                regex: /$/,
                next: "pop",
              },
              {
                include: "#base64-string",
              },
            ],
          },
        ],
        "#base64-string": [
          {
            token: "string.base64.teal",
            regex: /[a-zA-Z0-9\/\+]*={0,2}/,
          },
        ],
      };

      this.normalizeRules();
    };

    AlgorandTEALHighlightRules.metaData = {
      $schema:
        "https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json",
      name: "Algorand TEAL",
      scopeName: "source.teal",
    };

    oop.inherits(AlgorandTEALHighlightRules, TextHighlightRules);

    exports.AlgorandTEALHighlightRules = AlgorandTEALHighlightRules;
  }
);

ace.define(
  "ace/mode/algorand_teal",
  [
    "require",
    "exports",
    "module",
    "ace/lib/oop",
    "ace/mode/text_highlight_rules",
  ],
  function (require, exports, module) {
    "use strict";

    var oop = require("../lib/oop");
    var TextMode = require("./text").Mode;
    var AlgorandTEALHighlightRules =
      require("./algorand_teal_highlight_rules").AlgorandTEALHighlightRules;

    var Mode = function () {
      this.HighlightRules = AlgorandTEALHighlightRules;
    };
    oop.inherits(Mode, TextMode);

    (function () {
      // this.lineCommentStart = ""\\/\\/.*?$"";
      // this.blockComment = {start: ""/*"", end: ""*/""};
      // Extra logic goes here.
      this.$id = "ace/mode/algorand_teal";
    }.call(Mode.prototype));

    exports.Mode = Mode;
  }
);

editorLib.init();

})()