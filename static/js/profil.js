let section = document.querySelector("section"),
  ds = document.querySelector(".ds");
 

ds.onclick = () => {
  section.classList.toggle("dark");
};

  button = document.querySelector(".main .ds");
  text = document.querySelector(" .main .ds");
  isOriginalText = true;
button.addEventListener("click", function() {
    if (isOriginalText) {
        text.textContent = "light mode";
    } else {
        text.textContent = "dark mode";
    }
    isOriginalText = !isOriginalText;
});