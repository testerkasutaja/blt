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
		<div class="pull-left">
		<p class="counter">1/3</p>
		</div>
		<div class="well task">
            <?php	
							//RANDOM FAILI SAAMINE
							function getFile(){
								$files = glob('Eesti_ilukirjandus/ilukirjandus/Eesti_ilukirjandus_1990/*');
            		$filePath = $files[rand(0, count($files) - 1)];
            		echo $filePath;
								$xml_string = file_get_contents($filePath);
								return $xml_string;
							}
							function getSentence($xml_string){
								//namespaceidest ja include vabanemine, et kasutada xpath
								$xml_string = preg_replace('/xmlns[^=]*="[^"]*"/i', '', $xml_string);
								$xml_string = preg_replace('/[a-zA-Z]+:([a-zA-Z]+[=>])/', '$1', $xml_string);
            		$xml_string = preg_replace('/<xi:include +href[^=]*="[^"]*"+ \/>/i','',$xml_string);
								$xml = new SimpleXMLElement($xml_string);
								//RANDOM LAUSE SAAMINE
								$resultS = $xml->xpath('//s');
								$scounter= count($resultS)-1;
								echo 'mitu s-1 on ' . $scounter . '<br>';
								$nrS = rand(0,$scounter);
								echo '         mitmenda  S võtame' . $nrS . '<br>';
								echo $resultS[$nrS];
							}
			
						$xml_string = getFile();
						getSentence($xml_string);
			
						$morf_word = 'poest';
    				$morf_analys = 'pood+st //_S_ sg el, pl p, //';
			
			
						preg_match('/(sg||pl) (n|g|p|ill|in|el|ad|abl|all|tr|ter|es|ab|kom|adt)/i',	$morf_analys, $kaanded);
						preg_match('/_[A-Z]_/i', $morf_analys, $sonaliik);
						print_r($kaanded);
						print_r($sonaliik);
						if(count($kaanded)>1){
							//sõna ei sobi
						}else{
							
						}

            
            ?> 
		</div>
		
		<button id="next" type="button" class="btn btn-success btn-circle btn-xl pull-right"><span class="glyphicon glyphicon-menu-right"></span></button>
	</div>
</body>