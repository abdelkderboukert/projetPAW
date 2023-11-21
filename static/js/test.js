h = document.getElementById("h").textContent;
m = document.getElementById("m").textContent;
s = document.getElementById("s").textContent;
test(() =>{
    let date = new Date(),
    hour = date.getHours(),
    min = date.getMinutes(),
    sec = date.getSeconds();
    if (h+1< hour && m< min) {
        print("haha")
    }

}, 1000)