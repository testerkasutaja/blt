<?php

if( $_REQUEST["sentenceId"] ) {
	//$list = array
	//();
	$sentenceId = $_REQUEST['sentenceId'];
	echo $sentenceId;
	//array_push($list,$name);
    if (file_exists ("vastused/badSentences.csv")){
        $file = fopen("vastused/badSentences.csv","a");
	    chmod($file,0777);
        fputcsv($file,explode(',',$sentenceId));
    }else{
        $file = fopen("vastused/badSentences.csv","w");
	    chmod($file,0777);
        fputcsv($file,explode(',',$sentenceId));
    }
	

	fclose($file); 
}
?>