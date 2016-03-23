<?php
if( $_REQUEST["sentenceId"] ) {
	$list = array
	();
    $fileName = date("Y-m-d");
    $fileName = "data/". "unsuitableSentences_" . $fileName . ".csv";
    if (file_exists($fileName) == false){
        array_push($list,"ID");
    }
	$sentenceId = $_REQUEST['sentenceId'];
	echo sentenceId;
	array_push($list,$sentenceId);
    
    
    $file = fopen($fileName,"a");
    chmod($file,0777);
    foreach ($list as $line){
        fputcsv($file,explode(',',$line));
    }

	fclose($file); 
}
?>