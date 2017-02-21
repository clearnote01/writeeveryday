// Subject to change
var toWriteNo = 500

var textarea = document.getElementById('textarea')
var wordsarea = document.getElementById('noOfWords')

var regex = /\w+[\s.,]/g;

let words = []
let words_l = 0

console.log('This is new post page')

textarea.addEventListener("keyup", function() {
    console.log('some change');
    console.log(textarea.value);
    words = textarea.value.match(regex);
    console.log(words)
    if(words === null) {
      words_l = 0
    }
    else {
      words_l = words.length;
    }
    wordsarea.innerText = words_l + " words";
    checkIfFull(words_l);
});

function checkIfFull(words_l) {
  if (words_l > toWriteNo) {
    wordsarea.style.color = "green";
  }
  else {
    wordsarea.style.color = "white";
  }
}
