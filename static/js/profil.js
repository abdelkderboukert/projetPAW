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
