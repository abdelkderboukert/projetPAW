let section = document.querySelector("section"),
  ds = document.querySelector("#drk");

ds.onclick = () => {
  section.classList.toggle("dark");
};

let button = document.querySelector("#drk");
let text = document.querySelector("#drk");
let isOriginalText = true;
button.addEventListener("click", function () {
  if (isOriginalText) {
    text.textContent = "light mode";
  } else {
    text.textContent = "dark mode";
  }
  isOriginalText = !isOriginalText;
});
