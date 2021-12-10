






var ws = new WebSocket("ws://127.0.0.1:1299/");


function waitingKeypress() {
    return new Promise((resolve) => {
      document.addEventListener('keydown', onKeyHandler);
      function onKeyHandler(e) {
       
          document.removeEventListener('keydown', onKeyHandler);
          resolve();
        
      }
    });
  }

async function main(start){

    var a = start;

    while(ws.readyState==ws.OPEN){

        console.log("OK")

        if(a){
            await waitingKeypress();
            await delay(10);
            a=false

        }

      

        console.log("Sendoing")

       
    
       document.getElementById("song-pattern").getElementsByClassName("active").forEach(element => {
    
            
           
                send_message(element.innerText)
                
            
           
            
        });
    
    }
}

ws.onmessage = event => print_message(event.data)

ws.onopen = event => {
    console.log(event)
    main(true)


    
};

ws.onclose = event => {
    console.log(event)
   
};

ws.onerror = event => {
    console.log(event)
    
};

function print_message(message)
{
  console.log(message)
}

function send_message(msg)
{
    ws.send(msg);

    return false;
}





