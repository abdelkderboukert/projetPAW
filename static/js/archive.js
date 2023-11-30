let section = document.querySelector("section"),
  ds = document.querySelector(".drk");

ds.onclick = () => {
  section.classList.toggle("dark");
};

let button = document.querySelector(".container .drk");
let text = document.querySelector(".container .drk");
let isOriginalText = true;
button.addEventListener("click", function () {
  if (isOriginalText) {
    text.textContent = "light mode";
  } else {
    text.textContent = "dark mode";
  }
  isOriginalText = !isOriginalText;
});
/*0770396410 aymn familt 3mr*/
let todo = document.querySelectorAll(".container .todo .main .todo_con");
let title1 = document.querySelector(".container .todof .inf h3");
let inf1 = document.querySelector("#inf1");
let inf2 = document.querySelector("#inf2");
let inf3 = document.querySelector("#inf3");
console.log(todo);
for (const el of todo) {
  el.addEventListener("click", function () {
    const title = el.querySelector("h3");
    title1.textContent = title.textContent;
  });
}
