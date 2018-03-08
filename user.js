// ==UserScript==
// @name         SquadMarker
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://en.wikipedia.org/*
// @grant        none
// @require https://code.jquery.com/jquery-3.2.1.min.js
// @require https://cdn.jsdelivr.net/npm/js-cookie@2/src/js.cookie.min.js

// ==/UserScript==

(function() {
    var backend_url = "https://stark-springs-69888.herokuapp.com/mark";
    function makeid() {
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for (var i = 0; i < 100; i++)
            text += possible.charAt(Math.floor(Math.random() * possible.length));

        return text;
    }

    function markAnswer(){
        var selection = document.getSelection().toString();
        if (selection === ""){
            alert("You have to select some text as answer first!");
        }
        var question = window.prompt(selection + "\n\n\nEnter a question");
        var html = document.body.outerHTML;
        var ident = Cookies.get("squadMarkerId");
        if (question !== null){
            if (question !== ""){
                var payload = {"question": question, "answer": selection,
                               "html": html, "ident": ident};
                $.ajax({url: backend_url,
                    type: "post", contentType: "application/json",
                    data: JSON.stringify(payload),
                    success: function (){
                        console.log('reported');
                }});

                               
                console.log(question);
                console.log(selection);
                console.log(html);
                console.log(ident);
            }
        }
    }

    var button = document.createElement("button");
    button.innerHTML = "SQUADMARK";
    button.style = "top:0;right:0;position:fixed;z-index: 9999";

    var ident = Cookies.get("squadMarkerId");
    console.log(ident);
    if (ident === undefined){
        console.log("no cookie");
        Cookies.set("squadMarkerId", makeid());
    }
    document.body.appendChild(button);
    button.onclick = markAnswer;
})();
