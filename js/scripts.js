$(function(){	
	idList = [];
    $("#question").click(function(){
        $("#questiontext").toggle(1000);
    });
	gameTypeSelection();
});

function gameTypeSelection(){
	$("#buttonContent").append('<p>Vali mängu pikkus ja mängu tüüp.</p>');
	
	chooseSentencesAmountRadiobuttons();

	$("#buttonContent").append('<button id = "FindWordButton" class="btn btn-primary chooseCaseButton">Pane sõnasobivasse käändesse</button>');
	$("#FindWordButton").click(function(){
		var sentencesAmount = $('input[name=amountRadio]:checked', '#radioButtonFormAmount').val();
		if (typeof sentencesAmount === "undefined"){
			amountNotification();
		}else{
			$("#buttonContent").empty();
        	caseTypeSelection('findWord', sentencesAmount);
		}
		
		});
	
	$("#buttonContent").append('<button id = "findCase" class="btn btn-primary chooseCaseButton">Leia kääne</button>');
	$("#findCase").click(function(){
		var sentencesAmount = $('input[name=amountRadio]:checked', '#radioButtonFormAmount').val();
		if (typeof sentencesAmount === "undefined"){
			amountNotification()
		}else {
			$("#buttonContent").empty();
        	caseTypeSelection('findCase', sentencesAmount);
			}
		});	
}
function chooseSentencesAmountRadiobuttons(){
	$("#buttonContent").append('<form id="radioButtonFormAmount"></form>');
	$("#radioButtonFormAmount").append('<div class="radio-inline" ><label><input type="radio"  name="amountRadio" class="radioButtonCase" value = "5">5 lauset</label></div>');
	$("#radioButtonFormAmount").append('<div class="radio-inline" ><label><input type="radio"  name="amountRadio" class="radioButtonCase" value = "10">10 lauset</label></div>');
	
}

function amountNotification(){
	$("#answerModal").modal({backdrop: "static"});
	var text = "Mängu pikkus valimata! Palun vali mängu pikkus!";
	document.getElementById("rightOrWrong").innerHTML = text;
	$("#modalButton").append('<button id = "noAmount" class="btn btn-info">OK</button>')
	$('#noAmount').click(function(){
		$("#answerModal").modal("hide");
		$("#modalButton").empty();
	});
}

function caseTypeSelection(gameType, sentencesAmount){
	var sum = 0;
    var right = 0;
	if (gameType === "findWord"){
		$("#buttonContent").append('<button id = "placeCase" class="btn btn-primary chooseCaseButton">Kohakäänded</button>');
		$("#placeCase").click(function(){
			$("#buttonContent").empty();
			loadDoc("place",gameType,sum,right, sentencesAmount);
		});

		$("#buttonContent").append('<button id = "pCase" class="btn btn-primary chooseCaseButton">Osastav kääne</button>');
		$("#pCase").click(function(){
			$("#buttonContent").empty();
			loadDoc("p",gameType,sum,right, sentencesAmount);
		});

		$("#buttonContent").append('<button id = "gesCase" class="btn btn-primary chooseCaseButton">Omastav ja olev kääne</button>');
		$("#gesCase").click(function(){
			$("#buttonContent").empty();
			loadDoc("ges",gameType,sum,right, sentencesAmount);
		});

		$("#buttonContent").append('<button id = "otherCase" class="btn btn-primary chooseCaseButton">Saav, rajav, ilmaütlev ja kaasaütlev kääne</button>');
		$("#otherCase").click(function(){
			$("#buttonContent").empty();
			loadDoc("other",gameType,sum,right, sentencesAmount);
		});
	
		$("#buttonContent").append('<button id = "allCase" class="btn btn-primary chooseCaseButton">Kõik käänded</button>');
		$("#allCase").click(function(){
			$("#buttonContent").empty();
			loadDoc("all",gameType,sum,right, sentencesAmount);
		});
	}else{
		loadDoc("all",gameType,sum,right, sentencesAmount);
	}
}



function loadDoc(caseType, gameType,sum,right, sentencesAmount) {
    caseType = caseType;
	gameType = gameType;
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			getSentenceWithInfo(xhttp, caseType, gameType,sum,right, sentencesAmount);
		}
	};
    if(caseType == "place"){
		xhttp.open("GET", "./laused/kohakäänded.xml", true);
	}
    if(caseType == "p"){
        xhttp.open("GET", "./laused/osastav.xml", true);
  } 
	if(caseType == "ges"){
        xhttp.open("GET", "./laused/omastav_olev.xml", true);
  }
	if(caseType == "other"){
        xhttp.open("GET", "./laused/saav_rajav_ilma_kaasa.xml", true);
  } 
    if(caseType == "all"){
        xhttp.open("GET", "./laused/koik_laused.xml", true);
  } 
    xhttp.send();
}

function idListCheck(randomNr,countInfo){
	var index = $.inArray(randomNr,idList);
	console.log(index);
	if (!(index==-1)){
		var newRandomNr = Math.floor((Math.random() * countInfo) + 0);
		idListCheck(randomNr,countInfo);
	}
	return randomNr;
}

function getSentenceWithInfo(xml,caseType,gameType,sum,right, sentencesAmount) {
	
    score = calculateScore(sum,right);
    if (isNaN(score)){
        document.getElementById("counter").innerHTML = "0"+"%";
    }else{
        document.getElementById("counter").innerHTML = score+"%";
    }
    
	var xmlDoc = xml.responseXML;
	var countInfo = xmlDoc.getElementsByTagName("info").length;
    var randomNr = Math.floor((Math.random() * countInfo) + 0);
	console.log('enne '+randomNr)
	randomNr = idListCheck(randomNr,countInfo);
	console.log('pärast '+randomNr)
	idList.push(randomNr);

	var sentence = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("s")[0].childNodes[0].nodeValue;
	sentence = modifySentence(sentence);
	var splittedSentence = sentence.split("%%%");
    if (splittedSentence.length==2){
        sentenceFront = splittedSentence[0]
        sentenceBack = splittedSentence[1]
    }else{
        sentenceFront=""
        sentenceBack=splittedSentence[0]
    }
	var nr = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("nr")[0].childNodes[0].nodeValue;
	var caseName = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("case")[0].childNodes[0].nodeValue;
	var nominative = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("n")[0].childNodes[0].nodeValue;
	//kontroll kas on mitu vastust
	var countAnswers = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("answer").length;
	var answers = [];
	var word = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("word")[0].childNodes[0].nodeValue;
	if (gameType ==="findWord"){
		word = word.toLowerCase();
		answers.push(word);
		if (countAnswers > 0 ){
			for(i = 0; i < countAnswers; i++){
				var a = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("answer")[i].childNodes[0].nodeValue.toLowerCase()
				answers.push(a);
			}	
		}
	}
	var nrCaseName = nr + "e " + caseName;
	if(gameType=='findWord'){
		addGameContentForFindWord(nrCaseName,nominative,sentenceFront,sentenceBack,answers,caseType,gameType,sum,right, sentencesAmount);
	}
	else{	addGameContentForFindCase(nominative,sentenceFront,sentenceBack,nr,caseName,word,caseType,gameType,sum,right, sentencesAmount);
	}	
}

function modifySentence(sentence){
	sentence = sentence.replace(" ,",",");
	sentence = sentence.replace(" .",".");
	sentence = sentence.replace(" ?","?");
	sentence = sentence.replace(" !","!");
	return sentence;
}

function addGameContentForFindWord(nrCaseName,nominative,sentenceFront,sentenceBack,answers,caseType,gameType,sum,right, sentencesAmount){
	$("#sentenceContent").append('<div class= "case" id="case"></div>');
	$("#sentenceContent").append('<div id="word" class= "wordInNominative"></div>');
	$("#sentenceContent").append('<div id="sentenceDiv" class="sentence row"></div>');
	$("#sentenceDiv").append('<p id="sentenceFront" class="sentenceFront" ></p>');
	$("#sentenceDiv").append('<input id="inputAnswer" class = "inputAnswer"type="text">');
	$("#sentenceDiv").append('<p id="sentenceBack" class="sentenceBack"></p>');
    document.getElementById("case").innerHTML = nrCaseName;
	document.getElementById("word").innerHTML = nominative;
	document.getElementById("sentenceFront").innerHTML = sentenceFront;
    document.getElementById("sentenceBack").innerHTML = sentenceBack;
	
	$("#nextButton").append('<button id="next" type="button" class="nextButton btn btn-success btn-circle btn-xl pull-right" ></button>');
	$("#next").append('<span class="glyphicon glyphicon-menu-right"></span>');
	$("#next").click(function(){
		controlAnswerFindWord(answers,caseType,gameType,sum,right, sentencesAmount);
	});
	$("#inputAnswer").keyup(function(event){
		if(event.keyCode == 13){
            $("#next").click();
        }
    });
	
}

function addGameContentForFindCase(nominative,sentenceFront,sentenceBack,nr,caseName,word,caseType,gameType,sum,right, sentencesAmount){
	
	var sentence = sentenceFront + " <b>" + word + " </b>" + sentenceBack ;
	$("#sentenceContent").append('<p id = "fullSentence" class = "fullSentence"></p>');
	$("#fullSentence").html(sentence);
	$("#sentenceContent").append('<p id = "textForCase"></p>');
	$("#textForCase").html("Mis käändes on sõna: <b>" + word+'</b>?');
	$("#sentenceContent").append('<form id="radioButtonFormCase"></form>');
	$("#radioButtonFormCase").append('<div class="radio-inline" ><label><input type="radio"  name="caseRadio" class="radioButtonCase" value = "omastav">Omastav</label></div>');
	$("#radioButtonFormCase").append('<div class="radio-inline"><label><input type="radio" id = "radioButtonCase" name="caseRadio" class="radioButtonCase" value = "osastav">Osastav</label></div>');
	$("#radioButtonFormCase").append('<div class="radio-inline" ><label><input type="radio"  name="caseRadio" class="radioButtonCase" value = "sisseütlev">Sisseütlev</label></div>');
	$("#radioButtonFormCase").append('<div class="radio-inline"><label><input type="radio" id = "radioButtonCase" name="caseRadio" class="radioButtonCase" value = "seesütlev">Seesütlev</label></div>');
	$("#radioButtonFormCase").append('<div class="radio-inline" ><label><input type="radio"  name="caseRadio" class="radioButtonCase" value = "seestütlev">Seestütlev</label></div>');
	$("#radioButtonFormCase").append('<div class="radio-inline"><label><input type="radio" id = "radioButtonCase" name="caseRadio" class="radioButtonCase" value = "alaleütlev">Alaleütlev</label></div>');
	$("#radioButtonFormCase").append('<div class="radio-inline" ><label><input type="radio"  name="caseRadio" class="radioButtonCase" value = "alalütlev">Alalütlev</label></div>');
	$("#radioButtonFormCase").append('<div class="radio-inline"><label><input type="radio" id = "radioButtonCase" name="caseRadio" class="radioButtonCase" value = "alaltütlev">Alaltütlev</label></div>');
	$("#radioButtonFormCase").append('<div class="radio-inline" ><label><input type="radio"  name="caseRadio" class="radioButtonCase" value = "saav">Saav</label></div>');
	$("#radioButtonFormCase").append('<div class="radio-inline"><label><input type="radio" id = "radioButtonCase" name="caseRadio" class="radioButtonCase" value = "rajav">Rajav</label></div>');
	$("#radioButtonFormCase").append('<div class="radio-inline" ><label><input type="radio"  name="caseRadio" class="radioButtonCase" value = "olev">Olev</label></div>');
	$("#radioButtonFormCase").append('<div class="radio-inline"><label><input type="radio" id = "radioButtonCase" name="caseRadio" class="radioButtonCase" value = "ilmaütlev">Ilmaütlev</label></div>');
	$("#radioButtonFormCase").append('<div class="radio-inline" ><label><input type="radio"  name="caseRadio" class="radioButtonCase" value = "kaasaütlev">Kaasaütlev</label></div>');
	$("#sentenceContent").append('<p id = "textForNr"></p>');
	$("#textForNr").html("Kas sõna <b>" + word + "</b> on ainsuses või mitmuses?");
	$("#sentenceContent").append('<form id="radioButtonFormNr"></form>');
	$("#radioButtonFormNr").append('<div class="radio-inline" id = "radioButtonNr"><label><input type="radio" id = "radioButtonSg" name="nrRadio" class="radioButtonNr" value = "ainsus">Ainsus</label></div><div class="radio-inline"><label><input type="radio" id = "radioButtonPl" name="nrRadio" class="radioButtonNr" value = "mitmus">Mitmus</label></div>');
	$("#nextButton").append('<button id="next" type="button" class="nextButton btn btn-success btn-circle btn-xl pull-right" ></button>');
	$("#next").append('<span class="glyphicon glyphicon-menu-right"></span>');
	$("#next").click(function(){
		controlAnswerFindCase(nr,caseName,caseType,gameType,sum,right, sentencesAmount);
	});
	
}

function controlAnswerFindWord(answers,caseType,gameType,sum,right, sentencesAmount) {
    
    $("#answerModal").modal({backdrop: "static"});
    var inputText = document.getElementById("inputAnswer").value.toLowerCase();
	var isAnswer = false;
	//console.log(answers);
    //console.log(sum);
    if (inputText === ""){
        tryagainButton();
    }else{
		$("#nextButton").empty();
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
            var text = "See vastus on kahjuks vale! <br> Õige vastus on: " + "<b>" + answers[0] + "</b>";
            document.getElementById("rightOrWrong").innerHTML = text;
        }
        createNextButtonModal(caseType,gameType,sum,right, sentencesAmount);
    }
    score = calculateScore(sum,right);
    //console.log(score);    
    document.getElementById("counter").innerHTML = score+"%";
	
}
function controlAnswerFindCase(nr,caseName,caseType,gameType,sum,right, sentencesAmount){
	$("#answerModal").modal({backdrop: "static"});
	var nrAnswer = $('input[name=nrRadio]:checked', '#radioButtonFormNr').val(); 
	var caseAnswer = $('input[name=caseRadio]:checked', '#radioButtonFormCase').val();
	
	if (caseName === "lühike sisseütlev"){
		caseName = "sisseütlev";
	}
	
	if (typeof caseAnswer === "undefined" ||typeof nrAnswer ==="undefined"){
		tryagainButton();
	}else {
		$("#nextButton").empty();
		if (caseAnswer === caseName && nrAnswer === nr ){
			sum=sum+1;
			right = right +1;
			var text = "Õige vastus";
            document.getElementById("rightOrWrong").innerHTML = text;		
		}
		if (!(caseAnswer === caseName) && nrAnswer === nr){
			sum=sum+1;
			right = right +0.5;
			var text = nr + " on õige, kuid kääne kahjuks vale. <br> Õige kääne on : " + caseName;
            document.getElementById("rightOrWrong").innerHTML = text;
		}
		if (caseAnswer === caseName && !(nrAnswer === nr)){
			sum=sum+1;
			right = right +0.5;
			var text =  "Kääne on õige, kuid sõna on " + nr + "es";
            document.getElementById("rightOrWrong").innerHTML = text;
		}
		if(!(caseAnswer === caseName) && !(nrAnswer === nr)){
			sum = sum +1 ;
			var text = "Mõlemad vastused on kahjuks valed.<br>" + "Õige vastus on " + nr + "e " + caseName;
			document.getElementById("rightOrWrong").innerHTML = text;
		}
		createNextButtonModal(caseType,gameType,sum,right, sentencesAmount);
	}
	score = calculateScore(sum,right);
	document.getElementById("counter").innerHTML = score+"%";
}
function createNextButtonModal(caseType,gameType,sum,right, sentencesAmount){
	$("#modalButton").append('<button type="button" id ="nextButtonModal" class="btn btn-success">Edasi</button>')
    $('#nextButtonModal').click(function(){
		$("#answerModal").modal("hide");
		$("#modalButton").empty();
		$("#sentenceContent").empty();
		if (sum >= sentencesAmount){
            gameOver(sum,right);
            
        }else{
            loadDoc(caseType,gameType,sum,right,sentencesAmount);            
        }
        });	
    
}	
function tryagainButton(){
    var text = "Palun sisesta vastus!";
    document.getElementById("rightOrWrong").innerHTML = text;
	$("#modalButton").append('<button id = "tryAgainButtonModal" class="btn btn-success">Proovi uuest</button>');
	$("#tryAgainButtonModal").click(function(){
		$("#answerModal").modal("hide");
		$("#modalButton").empty();
		});
}

function calculateScore(sum,right){
    score = right * 100 / sum;
	score = Math.round(score);
    return score;
}
function gameOver(sum,right){
    $("#gameOverModal").modal({backdrop: "static"});
	wrong = sum - right;
    var text = "Mäng läbi! <br> Õigeid vastuseid oli " + right + "<br> Valesid vastuseid oli "+ wrong+ "<br> Skoor on " + score + "%";
    document.getElementById("gameOverText").innerHTML = text;
    
	$("#modalButtonOver").append('<button id = "overButton" class="btn btn-success">Alusta mängu uuesti</button>')
	$('#overButton').click(function(){
		location.reload();
		$("#overButton").html('Laeb...');
	});
}
