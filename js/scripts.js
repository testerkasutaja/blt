$(function(){
    $("#question").click(function(){
        $("#questiontext").toggle(1000);
    });
    
    $("#inputAnswer").keyup(function(event){
      if(event.keyCode == 13){
          $("#next").click();
      }
    });
    
    var placeCase = document.createElement('input');
    placeCase.type = "button"
    placeCase.value = "Kohakäänded";
    placeCase.className = "btn btn-primary chooseCaseButton";
    placeCase.addEventListener('click', function(){
			document.getElementById("content").removeChild(pCase);
			document.getElementById("content").removeChild(placeCase);
			document.getElementById("content").removeChild(gesCase);
			document.getElementById("content").removeChild(otherCase);
			loadDoc("place");
    });
	
    document.getElementById("content").appendChild(placeCase);
	
		var pCase = document.createElement('input');
    pCase.type = "button"
    pCase.value = "Osastav kääne";
    pCase.className = "btn btn-primary chooseCaseButton";
    pCase.addEventListener('click', function(){
			document.getElementById("content").removeChild(pCase);
			document.getElementById("content").removeChild(placeCase);
			document.getElementById("content").removeChild(gesCase);
			document.getElementById("content").removeChild(otherCase);
			loadDoc("p");
    });

    document.getElementById("content").appendChild(pCase);
	
		var gesCase = document.createElement('input');
    gesCase.type = "button"
    gesCase.value = "Omastav ja olev kääne";
    gesCase.className = "btn btn-primary chooseCaseButton";
    gesCase.addEventListener('click', function(){
			document.getElementById("content").removeChild(pCase);
			document.getElementById("content").removeChild(placeCase);
			document.getElementById("content").removeChild(gesCase);
			document.getElementById("content").removeChild(otherCase);
			loadDoc("ges");
    });

    document.getElementById("content").appendChild(gesCase);
	
		var otherCase = document.createElement('input');
    otherCase.type = "button";
    otherCase.value = "Saav, rajav, ilmaütlev ja kaasaütlev käänded";
    otherCase.className = "btn btn-primary chooseCaseButton";
    otherCase.addEventListener('click', function(){
			document.getElementById("content").removeChild(pCase);
			document.getElementById("content").removeChild(placeCase);
			document.getElementById("content").removeChild(gesCase);
			document.getElementById("content").removeChild(otherCase);
			loadDoc("other");
    });

    document.getElementById("content").appendChild(otherCase);
});


function loadDoc(type) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			getSentence(xhttp);
		}
	};
 	if(type == "place"){
		xhttp.open("GET", "./laused/kohakäänded.xml", true);
	}
  if(type == "p"){
    xhttp.open("GET", "./laused/osastav.xml", true);
  } 
	if(type == "ges"){
    xhttp.open("GET", "./laused/omastav_olev.xml", true);
  }
	if(type == "other"){
    xhttp.open("GET", "./laused/saav_rajav_ilma_kaasa.xml", true);
  } 
	xhttp.send();
}

function getSentence(xml) {
  document.getElementById("sentenceConten").style.visibility = "visible"; 
  document.getElementById("next").style.visibility = "visible";
  document.getElementById("tryAgainButtonModal").style.visibility = "hidden";
  document.getElementById("nextButtonModal").style.visibility = "hidden"; 
  document.getElementById("inputAnswer").value = "";
	
	var xmlDoc = xml.responseXML;
	var countInfo = xmlDoc.getElementsByTagName("info").length;
	
	var list = [];
	for(i = 0; i<10; i++) {
		var randomNr = Math.floor((Math.random() * countInfo) + 0);
		var inf = xmlDoc.getElementsByTagName("info")[randomNr];
		list.push(inf);
	}
 	
	
	var sentence = list[0].getElementsByTagName("s")[0].childNodes[0].nodeValue;
    
	var splittedSentence = sentence.split("%%%");
    if (splittedSentence.length==2){
        sentenceFront = splittedSentence[0]
        sentenceBack = splittedSentence[1]
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
						var nextButtonModal = document.createElement('button');
    				nextButtonModal.type = "button"
    				nextButtonModal.value = "Edasi";
    				nextButtonModal.className = "tn btn-success nextButtonModal";
						document.getElementById("modalButton").appendChild(nextButtonModal);
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
