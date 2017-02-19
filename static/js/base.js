function bodyLoad() {
  setTimeout(loadIt, 1500);
}

function loadIt() {
  document.getElementById('thePage').style.display = "block";
  document.getElementById('myLoader').style.display = "none";
}
