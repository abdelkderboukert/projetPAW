/*h = document.getElementById("h").textContent;
m = document.getElementById("m").textContent;
s = document.getElementById("s").textContent;
test(() => {
  let date = new Date(),
    hour = date.getHours(),
    min = date.getMinutes(),
    sec = date.getSeconds();
  if (h + 1 < hour && m < min) {
    print("haha");
  }
}, 1000);*/

let todo = document.querySelectorAll(".container .todo .main .todo_con");
let title1 = document.querySelector(".container .todof .inf h3");
let inf1 = document.getElementById("m1");
let inf2 = document.getElementById("m2");
let inf3 = document.getElementById("m3");
let txt1 = document.getElementById("txt1");
console.log(todo);
for (const el of todo) {
  el.addEventListener("click", function () {
    const title = el.querySelector("h3");
    const txt = el.querySelector("#txt");
    const dat = el.querySelector("#dat");
    const hour = el.querySelector("#hour");
    const datd = el.querySelector("#datd");
    title1.textContent = title.textContent;
    inf1.textContent = dat.textContent;
    inf2.textContent = hour.textContent;
    inf3.textContent = datd.textContent;
    txt1.textContent = txt.textContent;
  });
}
let butt = document.querySelectorAll(".container .todo .main .todo_con .do");
console.log(butt);
for (const el of todo) {
  const id = el.querySelector("#id").textContent;

  el.addEventListener("click", async function () {
    console.log(id);
    const response = await fetch("/todo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: id }),
    });
    console.log(response);
    if (!response.ok) {
      console.error("An error occurred:", response.statusText);
    }
    const data = await response.text();
    console.log(data.message);
    location.reload();
  });
}
