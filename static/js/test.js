let section = document.querySelector("section"),
  ds = document.querySelector(".ds");

ds.onclick = () => {
  section.classList.toggle("dark");
};

let button = document.querySelector(".main .ds");
let text = document.querySelector(" .main .ds");
let isOriginalText = true;
button.addEventListener("click", function () {
  if (isOriginalText) {
    text.textContent = "light mode";
  } else {
    text.textContent = "dark mode";
  }
  isOriginalText = !isOriginalText;
});

let number = document.getElementById("number");
let conter = 0;
let nf = number.textContent;
bf = 472 * (1 - nf / 100);
setInterval(() => {
  if (conter == nf) {
    clearInterval();
  } else {
    conter += 1;
    number.innerHTML = conter + "%";
  }
}, 35);
document.documentElement.style.setProperty("--numm", bf);
