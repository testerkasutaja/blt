<?php

if( $_REQUEST["sentence"] ) {
  	$list = array
	();
    
   $fileName = "data/unsuitableSentences/". "unsuitableSentences" . ".csv";
    if (file_exists($fileName) == false){
        array_push($list,"id;lause;õige vastus;algvorm;kääne;number");
    }
	$sentence = $_REQUEST['sentence'];
	echo sentence;  
	array_push($list,$sentence);
    
    $file = fopen($fileName,"a");
    chmod($file,0777);
    foreach ($list as $line){
        fputcsv($file,explode(';',$line));
}
}
	
$date = date("Y-m-d");
if( $_REQUEST["answerData1"] ) {
	$list = array
	();
    
    $fileName = "data/word test/" . $date . ".csv";
    if (file_exists($fileName) == false){
        array_push($list,"id;lause;õige sõna;kääne;vastus;õige/vale");
    }
	$answerData = $_REQUEST['answerData1'];
	echo $answerData;
	array_push($list,$answerData);
    
    
    $file = fopen($fileName,"a");
    chmod($file,0777);
    foreach ($list as $line){
        fputcsv($file,explode(';',$line));
    }
	

	fclose($file); 
}
if( $_REQUEST["answerData2"] ) {
	$list = array
	();
    
    $fileName = "data/case test/" . $date . ".csv";
    if (file_exists($fileName) == false){
        array_push($list,"id;lause;õige sõna;kääne;õige/vale;ainsus/mitmus;õige/vale");
    }
	$answerData = $_REQUEST['answerData2'];
	echo $answerData;
	array_push($list,$answerData);
    
    
    $file = fopen($fileName,"a");
    chmod($file,0777);
    foreach ($list as $line){
        fputcsv($file,explode(';',$line));
    }
	

	fclose($file); 
}
?>