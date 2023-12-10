/*let section = document.querySelector("section"),
  icons = document.querySelector("#drk");

icons.onclick = () => {
  section.classList.toggle("dark");
};*/
document.addEventListener("DOMContentLoaded", function () {
  var section = document.querySelector("section");
  var button = document.querySelector("#drk");
  var isOriginalText = true;
  var ds = document.querySelector("#drk");

  button.addEventListener("click", function () {
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
// creating a function and calling it in every seconds
setInterval(() => {
  let date = new Date(),
    hour = date.getHours(),
    min = date.getMinutes(),
    sec = date.getSeconds();

  let d;
  d = hour < 12 ? "AM" : "PM"; //if hour is smaller than 12, than its value will be AM else its value will be pm
  hour = hour > 12 ? hour - 12 : hour; //if hour value is greater than 12 than 12 will subtracted ( by doing this we will get value till 12 not 13,14 or 24 )
  hour = hour == 0 ? (hour = 12) : hour; // if hour value is  0 than it value will be 12

  // adding 0 to the front of all the value if they will less than 10
  hour = hour < 10 ? "0" + hour : hour;
  min = min < 10 ? "0" + min : min;
  sec = sec < 10 ? "0" + sec : sec;

  document.querySelector(".hour_num").innerText = hour;
  document.querySelector(".min_num").innerText = min;
  document.querySelector(".sec_num").innerText = sec;
  document.querySelector(".am_pm").innerText = d;
}, 1000); // 1000 milliseconds = 1s
