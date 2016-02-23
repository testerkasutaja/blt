$(function(){
    sum = 0;
    right = 0;
    wrong = 0;
    $("#question").click(function(){
        $("#questiontext").toggle(1000);
    });
    
    //$("#inputAnswer").keyup(function(event){
      //  if(event.keyCode == 13){
        //    $("#next").click();
        //}
    //});
    
    var placeCase = document.createElement('input');
    placeCase.type = "button"
    placeCase.value = "Kohakäänded";
    placeCase.className = "btn btn-primary chooseCaseButton";
    placeCase.addEventListener('click', function(){
        document.getElementById("content").removeChild(pCase);
        document.getElementById("content").removeChild(placeCase);
        document.getElementById("content").removeChild(gesCase);
        document.getElementById("content").removeChild(otherCase);
        document.getElementById("content").removeChild(allCases);
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
        document.getElementById("content").removeChild(allCases);
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
        document.getElementById("content").removeChild(allCases);
		loadDoc("ges");
    });

    document.getElementById("content").appendChild(gesCase);
    var otherCase = document.createElement('input');
    otherCase.type = "button";
    otherCase.value = "Saav, rajav, ilmaütlev ja kaasaütlev kääne";
    otherCase.className = "btn btn-primary chooseCaseButton";
    otherCase.addEventListener('click', function(){
        document.getElementById("content").removeChild(pCase);
		document.getElementById("content").removeChild(placeCase);
		document.getElementById("content").removeChild(gesCase);
		document.getElementById("content").removeChild(otherCase);
        document.getElementById("content").removeChild(allCases);
		loadDoc("other");
    });

    document.getElementById("content").appendChild(otherCase);
    
    
    
    var allCases = document.createElement('input');
    allCases.type = "button";
    allCases.value = "Kõik käänded";
    allCases.className = "btn btn-primary chooseCaseButton";
    allCases.addEventListener('click', function(){
        document.getElementById("content").removeChild(pCase);
		document.getElementById("content").removeChild(placeCase);
		document.getElementById("content").removeChild(gesCase);
		document.getElementById("content").removeChild(otherCase);
        document.getElementById("content").removeChild(allCases);
		loadDoc("other");
    });

    document.getElementById("content").appendChild(allCases);  
    

});


function loadDoc(type) {
    gameType = type;
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
    if(type == "all"){
        xhttp.open("GET", "./laused/koik_laused.xml", true);
  } 
    xhttp.send();
}


function getSentence(xml) {
    score = calculateScore();
    console.log(score);
    if (isNaN(score)){
        document.getElementById("counter").innerHTML = "0"+"%";
    }else{
        document.getElementById("counter").innerHTML = score+"%";
    }
    document.getElementById("sentenceConten").style.visibility = "visible"; 
    document.getElementById("next").style.visibility = "visible";
    document.getElementById("inputAnswer").value = "";
    
	var xmlDoc = xml.responseXML;
	var countInfo = xmlDoc.getElementsByTagName("info").length;
    var randomNr = Math.floor((Math.random() * countInfo) + 0);
	//var list = [];
	//for(i = 0; i<10; i++) {
	//	var randomNr = Math.floor((Math.random() * countInfo) + 0);
	//	var inf = xmlDoc.getElementsByTagName("info")[randomNr];
	//	list.push(inf);
	//}
 	
	var sentence = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("s")[0].childNodes[0].nodeValue;
    
	var splittedSentence = sentence.split("%%%");
    if (splittedSentence.length==2){
        sentenceFront = splittedSentence[0]
        sentenceBack = splittedSentence[1]
    }else{
        sentenceFront=""
        sentenceBack=splittedSentence[0]
    }
    
	//var caseTag = document.createElement("div");
    //caseTag.className = "case";
    //caseTag.id = "case";
    
    //var wordTag = document.createElement("div");
    //wordTag.className = "wordInNominative";
    //wordTag.id = "word";
    
  //  var firstSenTag = document.createElement("div");
 //   firstSenTag.className = "pull-left";
 //   firstSenTag.id = "sentenceFront";
    
   // var lastSenTag = document.createElement("div");
//    lastSenTag.className = "pull-right";
  //  lastSenTag.id = "sentenceback";
    
    //var answerInputTag = document.createElement("input");
    //answerInputTag.id = "inputAnswer";
//    answerInputTag.type = "text"
    
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

    //document.getElementById("sentenceConten").appendChild(caseTag);
    document.getElementById("case").innerHTML = nrCaseName;
    
    //document.getElementById("sentenceConten").appendChild(wordTag);
	document.getElementById("word").innerHTML = nominative;
    
   // document.getElementById("sentenceConten").appendChild(firstSenTag);
	document.getElementById("sentenceFront").innerHTML = sentenceFront;
    
  // document.getElementById("sentenceConten").appendChild(answerInputTag);
    
    //document.getElementById("sentenceConten").appendChild(lastSenTag);
    document.getElementById("sentenceBack").innerHTML = sentenceBack;
}



function controlAnswer(xml) {
    
    $("#answerModal").modal({backdrop: "static"});
    var inputText = document.getElementById("inputAnswer").value.toLowerCase();
	var isAnswer = false;
	console.log(answers);
    console.log(sum);
    if (inputText === ""){
        tryagainButton();
    }else{
        for (a in answers){
            if (inputText == answers[a]){
                isAnswer = true;
                break;
            }
        }
        if(isAnswer) {
            sum = sum + 1;
            right = right + 1;
            var text = "Õige vastus!";
            document.getElementById("rightOrWrong").innerHTML = text;
        }
        else {
            sum = sum + 1;
            wrong = wrong + 1;
            var text = "See vastus on kahjuks vale! <br> Õige vastus on: " + "<b>" + answers[0] + "</b>";
            document.getElementById("rightOrWrong").innerHTML = text;
        }
        createNextButtonModal();
    }
    score = calculateScore();
    console.log(score);    
    document.getElementById("counter").innerHTML = score+"%";
	
}
function createNextButtonModal(){
    var nextButtonModal = document.createElement('input');
    nextButtonModal.type = "button";
    nextButtonModal.value = "Edasi";
    nextButtonModal.id = "nextButtonModal"
    nextButtonModal.className = "btn btn-success";
    
    document.getElementById("modalButton").appendChild(nextButtonModal);
    nextButtonModal.addEventListener('click', function(){
        //document.getElementById("sentenceConten").removeChild(caseTag);
        if (sum >= 3){
            gameOver();
            
        }else{
            loadDoc(gameType);            
        }
        document.getElementById("modalButton").removeChild(nextButtonModal);
        $("#answerModal").modal("hide");
        
    });
    
}	
function tryagainButton(){
    var text = "Palun sisesta vastus!";
    document.getElementById("rightOrWrong").innerHTML = text;
    var tryAgainModalButton = document.createElement('input');
    tryAgainModalButton.type = "button";
    tryAgainModalButton.value = "Proovi uuesti";
    tryAgainModalButton.id = "tryAgainButtonModal";
    tryAgainModalButton.className = "btn btn-success";
    document.getElementById("modalButton").appendChild(tryAgainModalButton);
    tryAgainModalButton.addEventListener('click', function(){
        document.getElementById("modalButton").removeChild(tryAgainModalButton);
        $("#answerModal").modal("hide");
    });
}

function calculateScore(){
    score = right * 100 / sum;
	score = Math.round(score);
    return score;
    
}
function gameOver(){
    $("#gameOverModal").modal({backdrop: "static"});
    var text = "Mäng läbi! <br> Õigeid vastuseid oli " + right + " <br> Valesid vastuseid oli " + wrong + "<br> Skoor on " + score + "%";
    document.getElementById("gameOverText").innerHTML = text;
    
    var startAgainModalButton = document.createElement('input');
    startAgainModalButton.type = "button";
    startAgainModalButton.value = "Alusta mängu uuesti";
    startAgainModalButton.id = "tryAgainButtonModal";
    startAgainModalButton.className = "btn btn-success";
    document.getElementById("modalButtonOver").appendChild(startAgainModalButton);

    startAgainModalButton.addEventListener('click', function(){
        location.reload();
		startAgainModalButton.value = "Laeb...";
		      
    });
}
