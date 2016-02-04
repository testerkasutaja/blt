$(document).ready(function(){
    $("#question").click(function(){
        $("#questiontext").toggle(1000);
    });
});


function loadDoc() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
    myFunction(xhttp);
    }
  };
  xhttp.open("GET", "./laused.xml", true);
  xhttp.send();
}
function myFunction(xml) {
  var xmlDoc = xml.responseXML;
	var countInfo = xmlDoc.getElementsByTagName("info").length;
 	var randomNr = Math.floor((Math.random() * countInfo) + 0);
	var sentence = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("s")[0].childNodes[0].nodeValue;
	var splittedSentence= sentence.split("%%%");
	//sentence1=splittedSentence[0]
	//sentence2=splittedSentence[1]
	//window.alert(splittedSentence[0])
	var nr = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("nr")[0].childNodes[0].nodeValue;
	var caseName = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("case")[0].childNodes[0].nodeValue;
	var nominative = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("n")[0].childNodes[0].nodeValue;
	//kontroll kas on mitu vastust
	var countAnswers = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("answer").length;
	answers = [];
	for(i = 0; i < countAnswers; i++){
		answers.push(xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("answer")[i].childNodes[0].nodeValue);
	}


	
	//answer2 = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("answer")[1].childNodes[0].nodeValue;
	
	nrCaseName = nr + " " + caseName;
	
	document.getElementById("sentence").innerHTML = sentence;
	document.getElementById("case").innerHTML = nrCaseName;
	document.getElementById("word").innerHTML = nominative;
}
function controlAnswer(xml) {
	var inputText = document.getElementById("inputAnswer").value;
	var isAnswer = false;
	console.log(answers);
	for (a in answers){
		if (inputText == answers[a]){
			isAnswer = true;
			break;
		}
	}
	if(isAnswer) {
		text = "Õige vastus";
		window.alert(text);
	}
	else {
     text = "Vale vastus";
			window.alert(text);
    }
}
	