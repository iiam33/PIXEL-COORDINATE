function uploadFile() {
    document.getElementById('upload').click(); //redirect user to the file upload page  
}

function drag(){
    document.getElementById('files').parentNode.className = "dragzone"; //drag function
}

function drop(){
    document.getElementById('files').parentNode.className = 'dragzone'; //drop function
}