<?php

if( $_REQUEST["sentence"] ) {
  	$list = array
	();
    
   $fileName = "data/". "unsuitableSentences" . ".csv";
    if (file_exists($fileName) == false){
        array_push($list,"ID,Lause,Õige Vastus,Algvorm,Kääne,Number");
    }
	$sentence = $_REQUEST['sentence'];
	echo sentence;  
	array_push($list,$sentence);
    
    $file = fopen($fileName,"a");
    chmod($file,0777);
    foreach ($list as $line){
        fputcsv($file,explode(',',$line));
}
}
	
$date = date("Y-m-d");
if( $_REQUEST["answerData1"] ) {
	$list = array
	();
    
    $fileName = "data/" . "answersG1_" . $date . ".csv";
    if (file_exists($fileName) == false){
        array_push($list,"ID,VASTUS,ÕIGE/VALE");
    }
	$answerData = $_REQUEST['answerData1'];
	echo $answerData;
	array_push($list,$answerData);
    
    
    $file = fopen($fileName,"a");
    chmod($file,0777);
    foreach ($list as $line){
        fputcsv($file,explode(',',$line));
    }
	

	fclose($file); 
}
if( $_REQUEST["answerData2"] ) {
	$list = array
	();
    
    $fileName = "data/" . "aanswersG2_" . $date . ".csv";
    if (file_exists($fileName) == false){
        array_push($list,"ID,KÄÄNE,ÕIGE/VALE,AINSUS/MITMUS,ÕIGE/VALE");
    }
	$answerData = $_REQUEST['answerData2'];
	echo $answerData;
	array_push($list,$answerData);
    
    
    $file = fopen($fileName,"a");
    chmod($file,0777);
    foreach ($list as $line){
        fputcsv($file,explode(',',$line));
    }
	

	fclose($file); 
}
?>