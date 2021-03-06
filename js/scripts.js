$(function(){
	
	answerStr = "";
	idList = [];

	gameTypeSelection();
	
	$(document).keypress(function(e) {
		if(e.which == 13) {
			var nextExists = document.getElementById("next");

			var tryagainExists  = document.getElementById('tryAgainButtonModal');

			var nextModalExists = document.getElementById("nextButtonModal");
			if (tryagainExists !== null && nextExists !== null){
				$('#tryAgainButtonModal').trigger('click');
			}
			if (tryagainExists == null && nextExists !== null ){
				
				$('#next').trigger('click');
			}
			if (nextModalExists !== null){
				$('#nextButtonModal').trigger('click');
			}
		}
});
});

function gameTypeSelection(){
   
	

	$('#question').tooltipster({
            content: $('<span>Esimesena on soovitatav mängida mängu "Pane sõna õigesse käändesse" <br> ning seejärel oma teadmisi kontrollida mänguga "Leia õige kääne".</span>'),
			theme: 'tooltipster-light'
        });
	
	
	
	chooseSentencesAmountRadiobuttons();

	$("#buttonContent").append('<button id = "FindWordButton" class="btn btn-primary chooseCaseButton">Pane sõna õigesse käändesse</button>');
	$("#FindWordButton").click(function(){
		var sentencesAmount = $('input[name=amountRadio]:checked', '#radioButtonFormAmount').val();
		if (typeof sentencesAmount === "undefined"){
			$("#modalButton").empty();
			amountNotification();
		}else{
			$("#buttonContent").empty();
        	caseTypeSelection('findWord', sentencesAmount);
		}
		
		});
	
	$("#buttonContent").append('<button id = "findCase" class="btn btn-primary chooseCaseButton">Leia õige kääne</button>');
	$("#findCase").click(function(){
		var sentencesAmount = $('input[name=amountRadio]:checked', '#radioButtonFormAmount').val();
		if (typeof sentencesAmount === "undefined"){
			$("#modalButton").empty();
			amountNotification();
		}else {
			$("#buttonContent").empty();
        	caseTypeSelection('findCase', sentencesAmount);
			}
		});	
}
function chooseSentencesAmountRadiobuttons(){
	$("#buttonContent").append('<p class="instruction">Vali mängu pikkus ja mängu tüüp.</p>');
	$("#buttonContent").append('<form id="radioButtonFormAmount" class="radioButtonFormAmount"></form>');

	$("#radioButtonFormAmount").append('<div class="radio-inline" ><label><input type="radio"  name="amountRadio" class="radioButtonCase" value = "1">1 lause</label></div>');
	$("#radioButtonFormAmount").append('<div class="radio-inline" ><label><input type="radio"  name="amountRadio" class="radioButtonCase" value = "5">5 lauset</label></div>');
	$("#radioButtonFormAmount").append('<div class="radio-inline" ><label><input type="radio"  name="amountRadio" class="radioButtonCase" value = "10">10 lauset</label></div>');
	$("#radioButtonFormAmount").append('<div class="radio-inline" ><label><input type="radio"  name="amountRadio" class="radioButtonCase" value = "20">20 lauset</label></div>');
}

function amountNotification(){
	$("#answerModal").modal({backdrop: "static"});
	var text = "Mängu pikkus valimata.<br> Palun valige mängu pikkus.";
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
		$('#question').tooltipster('content', 'Vali, milliseid käändeid soovid harjutada.');
        $("#buttonContent").append('<button id = "gesCase" class="btn btn-primary chooseCaseButton">Nimeta, omastav ja olev kääne</button>');
		$("#gesCase").click(function(){
			$('#question').tooltipster('content', 'Sisesta sõna etteantud käändes ning vajuta noolega rohelisele nupule.')
			$("#buttonContent").empty();
			loadDoc("ges",gameType,sum,right, sentencesAmount);
		});
		$("#buttonContent").append('<button id = "placeCase" class="btn btn-primary chooseCaseButton">Kohakäänded</button>');
		$("#placeCase").click(function(){
			$('#question').tooltipster('content', 'Sisesta sõna etteantud käändes ning vajuta noolega rohelisele nupule.');

			$("#buttonContent").empty();
			loadDoc("place",gameType,sum,right, sentencesAmount);
		});

		$("#buttonContent").append('<button id = "pCase" class="btn btn-primary chooseCaseButton">Osastav kääne</button>');
		$("#pCase").click(function(){
			$('#question').tooltipster('content', 'Sisesta sõna etteantud käändes ning vajuta noolega rohelisele nupule.');
			$("#buttonContent").empty();
			loadDoc("p",gameType,sum,right, sentencesAmount);
		});

		$("#buttonContent").append('<button id = "otherCase" class="btn btn-primary chooseCaseButton">Saav, rajav, ilmaütlev ja kaasaütlev kääne</button>');
		$("#otherCase").click(function(){
			$('#question').tooltipster('content', 'Sisesta sõna etteantud käändes ning vajuta noolega rohelisele nupule.');
			$("#buttonContent").empty();
			loadDoc("other",gameType,sum,right, sentencesAmount);
		});
	
		$("#buttonContent").append('<button id = "allCase" class="btn btn-primary chooseCaseButton">Kõik käänded</button>');
		$("#allCase").click(function(){
			$('#question').tooltipster('content', 'Sisesta sõna etteantud käändes ning vajuta noolega rohelisele nupule.');
           
			$("#buttonContent").empty();
			loadDoc("all",gameType,sum,right, sentencesAmount);
		});
	}else{
		$('#question').tooltipster('content', 'Vasta küsimustele ning vajuta rohelist noolega nuppu.');
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
        xhttp.open("GET", "./laused/nimetav_omastav_olev.xml", true);
  }
	if(caseType == "other"){
        xhttp.open("GET", "./laused/saav_rajav_ilma_kaasa.xml", true);
  } 
    if(caseType == "all"){
        xhttp.open("GET", "./laused/koik_laused.xml", true);
  } 
    xhttp.send();
}

function addGeneralGameContent(){
    
    	$("#counterDiv").append('<div id="counter" class="pull-left counter" ></div>');
    	$("#nextButton").append('<button id="next" type="button" class="nextButton btn btn-success btn-circle btn-xl pull-right" ></button>');
	$("#next").append('<span class="glyphicon glyphicon-menu-right"></span>');
    
}

function getSentenceWithInfo(xml,caseType,gameType,sum,right, sentencesAmount) {

    addGeneralGameContent(); 
 	score = calculateScore(sum,right);
    if (isNaN(score)){
        document.getElementById("counter").innerHTML = "Skoor: " + "0"+"%"+ "<br> Laused: "+(sum+1) + " / " + sentencesAmount ;
    }else{
        document.getElementById("counter").innerHTML = "Skoor: " + score+"%"+  "<br> Laused: "+(sum+1) + " / "+ sentencesAmount  ;
    } 
    
	var xmlDoc = xml.responseXML;
	var countInfo = xmlDoc.getElementsByTagName("info").length;
	
	var randomNr;
	var continueLoop = true;
	while(continueLoop){
		randomNr = Math.floor((Math.random() * countInfo) + 0);
		var index = $.inArray(randomNr,idList);
		if(index == -1){
			continueLoop = false;
		}
	}
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
	
	sentenceId = xmlDoc.getElementsByTagName("info")[randomNr].getAttribute('id');

	
	var nr = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("nr")[0].childNodes[0].nodeValue;
    var title = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("title")[0].childNodes[0].nodeValue;
	var caseName = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("case")[0].childNodes[0].nodeValue;
	var nominative = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("n")[0].childNodes[0].nodeValue;
	//kontroll kas on mitu vastust
	var countAnswers = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("answer").length;
	var answers = [];
	var word = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("word")[0].childNodes[0].nodeValue;
	console.log(sentenceId)
	answerStr = sentenceId + ';' + sentence + ';' + word + ';'+ caseName+';'+nr+';';
	var nrCaseName = "<b>"+ nr + "e " + caseName+ "</b>";
	var cliticCount = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("clitic").length;
	var badSentenceStr = sentenceId + '; '+ sentence +'; '+ word +'; '+ nominative + '; ' + caseName + '; '+ nr;
	if (gameType ==="findWord"){
		word = word.toLowerCase();
		answers.push(word);
		if (countAnswers > 0 ){
			for(i = 0; i < countAnswers; i++){
				var a = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("answer")[i].childNodes[0].nodeValue.toLowerCase()
				answers.push(a);
			}	
		}
		if (cliticCount > 0 ){
			var clitic = xmlDoc.getElementsByTagName("info")[randomNr].getElementsByTagName("clitic")[0].childNodes[0].nodeValue;
			nrCaseName = "<b>" + nrCaseName + "</b><br> Rõhuliide: " +"<b>-" + clitic +"</b>" ;
		}
		addGameContentForFindWord(nrCaseName,nominative,sentenceFront,sentenceBack,answers,caseType,gameType,sum,right, sentencesAmount,title, badSentenceStr);
	}else{
	 addGameContentForFindCase(sentenceFront,sentenceBack,nr,caseName,word,caseType,gameType,sum,right, sentencesAmount,title, badSentenceStr);
	}	
}

function modifySentence(sentence){
	sentence = sentence.replace(" ,",",");
	sentence = sentence.replace(" .",".");
	sentence = sentence.replace(" ?","?");
	sentence = sentence.replace(" !","!");
	return sentence;
}

function addGameContentForFindWord(nrCaseName,nominative,sentenceFront,sentenceBack,answers,caseType,gameType,sum,right, sentencesAmount,title, badSentenceStr){
    //$("#container").append('<div id ="title" class = "title"></div>');
	
	$("#head").append('<div id ="gameName" class = "head1"></div>');
	$("#head").append('<div id ="gameCase" class = "head2"></div>');
   // document.getElementById("title").innerHTML = 'Raamatu pealkiri: "' + title + '"' ;
   // $(".title").css("color", "rgb(30, 108, 132)");
	$("#sentenceContent").append('<div id="word" class= "wordInNominative"></div>');
	$("#sentenceContent").append('<div class= "case" id="case"></div>');
	$("#sentenceContent").append('<div id="sentenceDiv" class="sentence row"></div>');
	$("#sentenceDiv").append('<p id="sentenceFront" class="sentenceFront" ></p>');
	$("#sentenceDiv").append('<input id="inputAnswer" class = "inputAnswer"type="text">');
	document.getElementById("inputAnswer").focus();
	$("#sentenceDiv").append('<p id="sentenceBack" class="sentenceBack"></p>');
	document.getElementById("gameName").innerHTML ="Pane sõna õigesse käändesse";
    document.getElementById("case").innerHTML = "Kääne: "+nrCaseName;
	document.getElementById("word").innerHTML = "Sõna: <b>" + nominative+"</b>";
	document.getElementById("sentenceFront").innerHTML = sentenceFront;
    document.getElementById("sentenceBack").innerHTML = sentenceBack;
    if (caseType ==='p'){
		c = 'Osastav kääne'
	}else if(caseType==='all'){
		c = 'Kõik käänded'
	}else if (caseType ==='ges'){
		c = 'Omastav ja olev kääne'
	}else if (caseType ==="other"){
		c = 'Saav, rajav, ilmaütlev ja kaasaütlev kääne'
	}else{
		c = 'Kohakäänded'
	}
	document.getElementById("gameCase").innerHTML = c;
    $("#next").click(function(){
		controlAnswerFindWord(answers,caseType,gameType,sum,right, sentencesAmount, badSentenceStr);
		document.getElementById("inputAnswer").blur();
	});
}

function addGameContentForFindCase(sentenceFront,sentenceBack,nr,caseName,word,caseType,gameType,sum,right, sentencesAmount,title, badSentenceStr){
    $("#head").append('<div id ="gameName" class = "head1"></div>');
	$("#head").append('<div id ="gameCase" class = "head2"></div>');
	//document.getElementById("title").innerHTML = 'Raamatu pealkiri: "' + title + '"' ;
   // $(".title").css("color", "rgb(30, 108, 132)");
	var sentence = sentenceFront + " <b>" + word + " </b>" + sentenceBack ;
	$("#sentenceContent").append('<p id = "fullSentence" class = "fullSentence"></p>');
	$("#fullSentence").html(sentence);
	$("#sentenceContent").append('<div id = "queastionArea" class = "queastionArea"></div>')
	$("#queastionArea").append('<p id = "textForCase"></p>');
	$("#textForCase").html("Mis käändes on sõna <b>" + word+'</b>?');
	$("#queastionArea").append('<form id="radioButtonFormCase" class ="radioButtonFormCase"></form>');
	$("#radioButtonFormCase").append('<div class="radio-inline" ><label><input type="radio"  name="caseRadio" class="radioButtonCase" value = "nimetav">Nimetav</label></div>');
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
	$("#sentenceContent").append('<form id="radioButtonFormNr" ></form>');
	$("#radioButtonFormNr").append('<div class="radio-inline" id = "radioButtonNr"><label><input type="radio" id = "radioButtonSg" name="nrRadio" class="radioButtonNr" value = "ainsus">Ainsus</label></div><div class="radio-inline"><label><input type="radio" id = "radioButtonPl" name="nrRadio" class="radioButtonNr" value = "mitmus">Mitmus</label></div>');
	document.getElementById("gameName").innerHTML ="Leia õige kääne";
	document.getElementById("gameCase").innerHTML = "Kõik käänded";

    $("#next").click(function(){
		
		controlAnswerFindCase(nr,caseName,caseType,gameType,sum,right, sentencesAmount, badSentenceStr)
	});

}

function controlAnswerFindWord(answers,caseType,gameType,sum,right, sentencesAmount, badSentenceStr) {
    
    $("#answerModal").modal({backdrop: "static"});
    var inputText = document.getElementById("inputAnswer").value.toLowerCase();
	
	
	var isAnswer = false;
	//console.log(answers);
    //console.log(sum);
    if (inputText === ""){
		//$("#nextButton").empty();
        tryagainButton(gameType,badSentenceStr);
    }else{
		answerStr = answerStr + inputText + "; ";
		$("#nextButton").empty();
        $("#badSentence").empty();
        
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
            var text = "See vastus on kahjuks vale. <br> Õige vastus on " + "<b>" + answers[0] + "</b>"+".";
            document.getElementById("rightOrWrong").innerHTML = text;
        }
		
        createNextButtonModal(caseType,gameType,sum,right, sentencesAmount,badSentenceStr);
    	answerStr = answerStr + isAnswer;
		$.post( 
			"savedata.php",
        	{ answerData1: answerStr },
        	function(data) {
				$('#stage').html(data);
			});
	}


	
}
function controlAnswerFindCase(nr,caseName,caseType,gameType,sum,right, sentencesAmount, badSentenceStr){
	$("#answerModal").modal({backdrop: "static"});
	var nrAnswer = $('input[name=nrRadio]:checked', '#radioButtonFormNr').val(); 
	var caseAnswer = $('input[name=caseRadio]:checked', '#radioButtonFormCase').val();
	
	if (caseName === "lühike sisseütlev"){
		caseName = "sisseütlev";
	}
	
	if (typeof caseAnswer === "undefined" || typeof nrAnswer ==="undefined"){
		//$("#nextButton").empty();
		tryagainButton(gameType,badSentenceStr);
	}else {
		$("#nextButton").empty();
        $("#badSentence").empty();
		if (caseAnswer === caseName && nrAnswer === nr ){
            answerStr = answerStr + caseAnswer +';'+true + ';' + nrAnswer + ';' + true ; 
			sum=sum+1;
			right = right +1;
			var text = "Õige vastus!";
            document.getElementById("rightOrWrong").innerHTML = text;		
		}
		if (!(caseAnswer === caseName) && nrAnswer === nr){
            answerStr = answerStr + caseAnswer +';'+ false + ';' + nrAnswer + ';' + true ; 
			sum=sum+1;
			right = right +0.5;
			if(nr ==="mitmus"){
				var text = "Mitmus on õige, kuid kääne kahjuks vale. <br> Õige kääne on  " + caseName + ".";
			}else{
				var text = "Ainsus on õige, kuid kääne kahjuks vale. <br> Õige kääne on  " + caseName+".";
			}
			
            document.getElementById("rightOrWrong").innerHTML = text;
		}
		if (caseAnswer === caseName && !(nrAnswer === nr)){
            answerStr = answerStr + caseAnswer +';'+true + ';' + nrAnswer + ';' + false ; 
			sum=sum+1;
			right = right +0.5;
			var text =  "Kääne on õige, kuid sõna on " + nr + "es" + ".";
            document.getElementById("rightOrWrong").innerHTML = text;
		}
		if(!(caseAnswer === caseName) && !(nrAnswer === nr)){
            answerStr = answerStr + caseAnswer +';'+false + ';' + nrAnswer + ';' + false ; 
			sum = sum +1 ;
			var text = "Mõlemad vastused on kahjuks valed.<br>" + "Õige vastus on " + nr + "e " + caseName + ".";
			document.getElementById("rightOrWrong").innerHTML = text;
		}
		createNextButtonModal(caseType,gameType,sum,right, sentencesAmount,badSentenceStr);
		$.post(
			"savedata.php",
			{ answerData2: answerStr },
			function(data) {
				$('#stage').html(data);
			});
	}
	
}

function createBadSentenceButton(badSentenceStr){
	$("#modalButton").append('<button id="inappropriateSentence" type="button" class="btn btn-warning btn-md inappropriateSentence" >Teata ebasobivast lausest</button>');
	$("#inappropriateSentence").click(function(){
		 $(this).prop('disabled', true);
		 $('#inappropriateSentence').html('Teatatud!');
		
		 $.post( 
                  "savedata.php",
             	  { sentence: badSentenceStr },
			      function(data) {
					  $('#stage').html(data);
				  }
               );
	  });
}

function createNextButtonModal(caseType,gameType,sum,right, sentencesAmount,badSentenceStr){
	createBadSentenceButton(badSentenceStr);
	$("#modalButton").append('<button type="button" id ="nextButtonModal" class="btn btn-success nextModalButton">Edasi</button>')
    $('#nextButtonModal').click(function(){
		$("#answerModal").modal("hide");
		$("#modalButton").empty();
		$("#sentenceContent").empty();

		
		if (sum >= sentencesAmount){
            gameOver(sum,right,gameType);
            
        }else{
            loadDoc(caseType,gameType,sum,right,sentencesAmount);
            $("#counterDiv").empty();
        }
        });
	
    
}	
function tryagainButton(gameType,badSentenceStr){
    var text = "Palun sisesta vastus.";
    document.getElementById("rightOrWrong").innerHTML = text;
	$("#modalButton").empty();
	createBadSentenceButton(badSentenceStr);
	$("#modalButton").append('<button type="button" id="tryAgainButtonModal" class="btn btn-success tryAgainButton">Proovi uuesti</button>');
	$("#tryAgainButtonModal").click(function(){
		if (gameType === "findWord"){
			document.getElementById("inputAnswer").focus();
			}
		$("#answerModal").modal("hide");
		$("#modalButton").empty();

		});
}

function calculateScore(sum,right){
    score = right * 100 / sum;
	score = Math.round(score);
    return score;
}
function gameOver(sum,right,gameType){
	score = calculateScore(sum,right);
    if (isNaN(score)){
        document.getElementById("counter").innerHTML = "Skoor: " + "0"+"%";
    }else{
        document.getElementById("counter").innerHTML = "Skoor: " + score+"%";
    } 
    $("#gameOverModal").modal({backdrop: "static"});
	if (gameType=="findCase"){
		sum = sum*2;
		right = right*2;
	}
	wrong = sum - right;
	score = calculateScore(sum,right)
    var text = "Mäng läbi! <br> Õigeid vastuseid oli " + right + "<br> Valesid vastuseid oli "+ wrong+ "<br> Skoor on " + score + "%";
    document.getElementById("gameOverText").innerHTML = text;
    
	$("#modalButtonOver").append('<button id = "overButton" class="btn btn-success">Vali uus test</button>');
	$('#overButton').click(function(){
		//$.get("savedata.php");
		location.reload();
		$("#overButton").html('Laeb...');
        $("#counterDiv").empty();
	});
}
