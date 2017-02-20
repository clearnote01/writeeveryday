function bodyLoad() {
  console.log('Body loaded');
  setTimeout(loadIt, 1500);
}

function loadIt() {
  document.getElementById('myLoader').style.display = "none";
  document.getElementById('thePage').style.display = "block";
}
