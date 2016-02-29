<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Käänded</title>
	<meta name="description" content=" kaanded">
  <meta name="author" content="Anneliis Halling">
	
	<link rel="stylesheet" href="css/bootstrap.min.css">
  <link rel="stylesheet" href="css/custom.css">
	<link href="//maxcdn.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css" rel="stylesheet">
<link href="//code.ionicframework.com/ionicons/1.5.2/css/ionicons.min.css" rel="stylesheet">
	
	<script src="js/jquery-2.1.3.min.js"></script>
  <script src="js/bootstrap.min.js"></script>
	<script src="js/scripts.js"></script>
	
</head>

<body>
	<div class="container">
		<div class="question">
            <button id="question" type="button" class="btn btn-info btn-circle btn-xl pull-right"><span class="glyphicon glyphicon-question-sign"></span></button>
            <p id="questiontext" class="questiontext pull-right"> 
          Sisesta sõna õiges käändes ning vajuta rohelisele noolele.
            </p>   
		</div>
		<div id="counter" class="pull-left counter">
		</div>
        <div id="content" class="well task">
			<div id="buttonContent"></div>
            <div id= "sentenceContent" class = "sentenceContent"></div>         
        </div>
		<div id = "nextButton"></div>
            
            <!-- Modal -->
            <div class="modal fade" id="answerModal" role="dialog">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-body">
                      <p id="rightOrWrong" class = "modalText"></p>
                    </div>
                    <div id = "modalButton" class="modal-footer modalButtons">
                    </div>
                  </div>
                </div>
            </div>
            <div class="modal fade" id="gameOverModal" role="dialog">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-body">
                      <p id="gameOverText" class = "modalText"></p>
                    </div>
                    <div id = "modalButtonOver" class="modal-footer modalButtons">
                    </div>
                  </div>
                </div>
            </div>
    </div>
</body>

</html>


