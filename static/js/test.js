h = document.getElementById("h").textContent;
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
}, 1000);

let section = document.querySelector("section"),
  ds = document.querySelector(".ds");

ds.onclick = () => {
  section.classList.toggle("dark");
};

let button = document.querySelector(".container .ds");
let text = document.querySelector(".container .ds");
let isOriginalText = true;
button.addEventListener("click", function () {
  if (isOriginalText) {
    text.textContent = "light mode";
  } else {
    text.textContent = "dark mode";
  }
  isOriginalText = !isOriginalText;
});
