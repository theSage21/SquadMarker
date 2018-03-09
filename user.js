// ==UserScript==
// @name         SquadMarker
// @namespace    http://tampermonkey.net/
// @version      0.5
// @description  Mark Questions and Answers on any page from the Internet
// @updateURL    https://raw.githubusercontent.com/theSage21/SquadMarker/master/user.js
// @downloadURL  https://raw.githubusercontent.com/theSage21/SquadMarker/master/user.js
// @author       Arjoonn Sharma
// @match        https://*.wikipedia.org/*
// @grant        none
// @require https://code.jquery.com/jquery-3.2.1.min.js
// @require https://cdn.jsdelivr.net/npm/js-cookie@2/src/js.cookie.min.js

// ==/UserScript==

(function() {
    var backend_url = 'wss://stark-springs-69888.herokuapp.com/mark';


    function makeid() {
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for (var i = 0; i < 100; i++)
            text += possible.charAt(Math.floor(Math.random() * possible.length));

        return text;
    }

    function markAnswer(ws){
        var selection = document.getSelection().toString();
        if (selection === ""){
            alert("You have to select some text as answer first!");
        }
        var question = window.prompt(selection);
        if (question !== null){
            if (question !== ""){
                var payload = {"question": question, "answer": selection};
                ws.send(JSON.stringify(payload));
            }
        }
    }


    var ident = Cookies.get("squadMarkerId");

    console.log(ident);
    if (ident === undefined){
        console.log("no cookie");
        Cookies.set("squadMarkerId", makeid());
    }

    var text = document.body.outerHTML;
    ident = Cookies.get("squadMarkerId");
    var ws = new WebSocket(backend_url);

    ws.onopen = function(evt) {
        var init = {"ident": ident, "url": document.location.href,
                    "text": text};
        ws.send(JSON.stringify(init));
        // ----------------------- ready for work
        var button = document.createElement("button");
        button.innerHTML = "SQUADMARK";
        button.style = "top:0;right:0;position:fixed;z-index: 9999;border: 1px solid; background: #cffb6c; border-radius: 5px;";
        button.onclick = function (){
            markAnswer(ws);
        };
        document.body.appendChild(button);
    };



})();
