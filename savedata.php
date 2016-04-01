<?php


if( $_REQUEST["sentenceId"] ) {
  
    $fileName = "data/". "unsuitableSentences" . ".csv";
	$sentenceId = $_REQUEST['sentenceId'];
	echo sentenceId;  
    
    $file = fopen($fileName,"a");
    chmod($file,0777);

 
    fputcsv($file,explode(',',$sentenceId));
	fclose($file); 
}
$date = date("Y-m-d");
if( $_REQUEST["answerData1"] ) {
	$list = array
	();
    
    $fileName = "data/" . "answersData_game1_" . $date . ".csv";
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
    
    $fileName = "data/" . "answersData_game2_" . $date . ".csv";
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