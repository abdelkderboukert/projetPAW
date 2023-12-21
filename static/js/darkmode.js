document.addEventListener("DOMContentLoaded", function () {
  var section = document.querySelector("section");
  var button = document.querySelector("#drk");
  var text = document.querySelector("#drk");
  var isOriginalText = true;
  var ds = document.querySelector("#drk");

  button.addEventListener("click", function () {
    if (isOriginalText) {
      text.textContent = "light mode";
    } else {
      text.textContent = "dark mode";
    }
    isOriginalText = !isOriginalText;

    // Save the current mode to localStorage
    localStorage.setItem("currentMode", isOriginalText ? "light" : "dark");
  });

  ds.onclick = () => {
    section.classList.toggle("dark");
    localStorage.setItem(
      "currentMode",
      section.classList.contains("dark") ? "dark" : "light"
    );
  };

  // Whenever you load a new page, check the value of 'currentMode' in localStorage and set the corresponding mode for the current page
  var currentMode = localStorage.getItem("currentMode");
  if (currentMode === "dark") {
    section.classList.add("dark");
  } else {
    section.classList.remove("dark");
  }
});
