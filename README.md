//TODO

This is a helper for virtualpiano.net it reads the active keys on the site and shows them on your Logitech keyboard.

How to make it work
```
git clone https://github.com/TheLukaDragar/logiPiano
``` 
install the python requirements- im to lazy to add req.txt

open a song
https://virtualpiano.net/?song-post-10847

run the program
```python logiPiano.py```


open the  web console in the browser (crtl+shift+i) and paste this in hit enter then
paste.txt
```
var ws=new WebSocket("ws://127.0.0.1:1299/");function waitingKeypress(){return new Promise(e=>{document.addEventListener("keydown",function n(o){document.removeEventListener("keydown",n);e()})})}async function main(e){for(var n=e;ws.readyState==ws.OPEN;)console.log("OK"),0==n?await waitingKeypress():n=!1,console.log("Sendoing"),document.getElementById("song-pattern").getElementsByClassName("active").forEach(e=>{send_message(e.innerText)})}function print_message(e){console.log(e)}function send_message(e){return ws.send(e),!1}ws.onmessage=(e=>print_message(e.data)),ws.onopen=(e=>{console.log(e),main(!0)}),ws.onclose=(e=>{console.log(e)}),ws.onerror=(e=>{console.log(e)});
```

start the song and the keys should light up :)