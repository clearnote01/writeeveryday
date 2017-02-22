// Subject to change
var toWriteNo = 500

var textarea = document.getElementById('textarea')
var wordsarea = document.getElementById('noOfWords')
var saveButton = document.getElementById('saveButton')
let daySpan = document.getElementById('noOfDay');
let leftDayButton = document.getElementById('leftDay')
let rightDayButton = document.getElementById('rightDay')

var regex = /\w+[\s.,]/g;

let words = []
let words_l = 0

console.log('This is new post page')

// Ajax load page content
//
let day = daySpan.innerText;
day = day.trim()
function loadDayPost(day, callback) {
  xreq = new XMLHttpRequest();
  xreq.open('GET', '/post/'+day, true);
  xreq.onreadystatechange = function() {
    if (xreq.readyState == XMLHttpRequest.DONE) {
      if (xreq.status == 200) {
        console.log(this.responseText);
        textarea.value = this.responseText
        noOfDay.innerText = day;
      }
      else {
        alert('Prolly got some error');
      }
    }
  }
  xreq.send()
}
if (day!==undefined) {
  loadDayPost(day);
}

// Button click left or right
leftDayButton.addEventListener('click', function() {
  day = day - 1;
  loadDayPost(day);
});
rightDayButton.addEventListener('click', function() {
  day = day + 1;
  loadDayPost(day);
});


// Ajax save functionality
postObject = {}
saveButton.addEventListener('click', function() {
  saveButton.style.backgroundColor = "red";
  saveButton.innerText = "saving...";
  postText = textarea.value;
  // Full JSON 
  postObject.words = words_l;
  postObject.text = postText;
  postObject.completed = 0;
  postObject.day = day;
  function savingAction() {
    saveButton.style.backgroundColor = "green";
    saveButton.innerText = "save";
  }
  console.log('Save button clicked');
  httpRequest = new XMLHttpRequest();
  httpRequest.open('POST','/savepost', true);
  httpRequest.setRequestHeader('Content-Type', 'text/plain');
  httpRequest.onreadystatechange = function() {
    if (httpRequest.readyState == XMLHttpRequest.DONE) {
      //saveButton.style.backgroundColor = "green";
      setTimeout(savingAction, 2000);
    }
  }
  //httpRequest.setRequestHeader('Content-Type', 'application/json')
  console.log('Sending data'+postObject);
  httpRequest.send(JSON.stringify(postObject));
});

textarea.addEventListener("keyup", function() {
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
