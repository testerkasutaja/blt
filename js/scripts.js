$(document).ready(function(){
    $("#question").click(function(){
        $("#questiontext").toggle(1000);
    });
});

$( document ).ready(function() {
      $("#inputAnswer").keyup(function(event){
      if(event.keyCode == 13){
          $("#next").click();
      }
  });
})
function loadDoc() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
    getSentenceFormAllCases(xhttp);
    }
  };
  xhttp.open("GET", "./laused.xml", true);
  xhttp.send();
}

function getSentenceFormAllCases(xml) {
    document.getElementById("allCases").style.visibility = "hidden"; 
    document.getElementById("sentenceConten").style.visibility = "visible"; 
    document.getElementById("next").style.visibility = "visible";
    document.getElementById("tryAgainButtonModal").style.visibility = "hidden";
    document.getElementById("nextButtonModal").style.visibility = "hidden"; 
    document.getElementById("inputAnswer").value = "";
    var xmlDoc = xml.responseXML;
	var countInfo = xmlDoc.getElementsByTagName("info").length;
 	var randomNr = Math.floor((Math.random() * countInfo) + 0);
	var sentence = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("s")[0].childNodes[0].nodeValue;
	var splittedSentence= sentence.split("%%%");
    if (splittedSentence.length==2){
        sentenceFront=splittedSentence[0]
        sentenceBack=splittedSentence[1]
    }else{
        sentenceFront=""
        sentenceBack=splittedSentence[0]
    }
	
	//window.alert(splittedSentence[0])
	var nr = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("nr")[0].childNodes[0].nodeValue;
	var caseName = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("case")[0].childNodes[0].nodeValue;
	var nominative = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("n")[0].childNodes[0].nodeValue;
	//kontroll kas on mitu vastust
	var countAnswers = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("answer").length;
	answers = [];
	for(i = 0; i < countAnswers; i++){
        var a = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("answer")[i].childNodes[0].nodeValue.toLowerCase()
		answers.push(a);
	}	
	var nrCaseName = nr + "e " + caseName;
	
	document.getElementById("sentenceFront").innerHTML = sentenceFront;
    document.getElementById("sentenceBack").innerHTML = sentenceBack;
	document.getElementById("case").innerHTML = nrCaseName;
	document.getElementById("word").innerHTML = nominative;
}

function controlAnswer(xml) {
	var inputText = document.getElementById("inputAnswer").value.toLowerCase();
	var isAnswer = false;
	console.log(answers);
    if (inputText=== ""){
        text = "Palun sisesta vastus!";
        document.getElementById("rightOrWrong").innerHTML = text;
        document.getElementById("tryAgainButtonModal").style.visibility = "visible"; 
    }else{
        for (a in answers){
            if (inputText == answers[a]){
                isAnswer = true;
                break;
            }
        }
        if(isAnswer) {
            text = "Õige vastus!";
            document.getElementById("rightOrWrong").innerHTML = text;
            document.getElementById("nextButtonModal").style.visibility = "visible"; 

        }
        else {
            text = "See vastus on kahjuks vale! Õige vastus on: " + answers[0];
            document.getElementById("rightOrWrong").innerHTML = text;
            document.getElementById("nextButtonModal").style.visibility = "visible"; 
        }
    }
	
}
	
function tryagain(){
    document.getElementById("tryAgainButtonModal").style.visibility = "hidden";    
}
