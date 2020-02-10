function c1()
    {
        var t=document.getElementById("txt");
        const es = document.getElementsByTagName('tr');
        var tableId = document.getElementById("table"); 
        for (const key in es) {
            es[key].onclick = function() {
                let number = parseInt(key);
                t.value = tableId.rows[number].cells[0].innerHTML
            }
        }    
    }