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
            
            $files = glob('Eesti_ilukirjandus_1990/*');
            $filePath = $files[rand(0, count($files) - 1)];
            //echo $filePath;
            
            //$xml=simplexml_load_file("Eesti_ilukirjandus_1990/proov.xml");
            
            
            $xmldata = simplexml_load_file('Eesti_ilukirjandus_1990/ilu_ahasveerus.tasak.xml');
            $random = array_rand($xmldata->xpath('s'), 1);
            echo count($random);      
            foreach ($random as $key) {
            $div = $xmldata->p[$key];
            echo $div->s[0] ;
                    }
        
        
          
            //$random = array_rand($xml->xpath("s"), 1);
            //echo count($random);
            //$s = $xml->s[random[0]];
            //echo $s;
            
            /*foreach ($random as $key) 
            $item = $xmldata->item[$key];
            echo '<li class="col4 item ' . $item->category . '">';
            
            $sentence = $xml->teiCorpus->TEI->text->body->div1->p[0]->s[0];
            echo $sentence;*/
            
            
            
            
            
            

            
            
            /*         
					
                        
            $mystring = file_get_contents('proov.txt', true);
            
            $mylist = preg_split('/(?<=[!?.])./',$mystring);
            $mylist = preg_replace('/%/', '', $mylist);
            $mylist[0] = str_replace('lauale','%',$mylist[0]);
            $sentence = preg_split('/%/',$mylist[0]);
            echo $sentence[0];
            echo '<input type="text" >';
            echo $sentence[1];*/
            ?> 
		</div>
		
		<button id="next" type="button" class="btn btn-success btn-circle btn-xl pull-right"><span class="glyphicon glyphicon-menu-right"></span></button>
	</div>
</body>