<?php

if( $_REQUEST["name"] ) {
	$list = array
	();
    $fileName = date("Y-m-d");
    $fileName = "vastused/". "answersData" . $fileName . ".csv";
    if (file_exists($fileName) == false){
        array_push($list,"ID,VASTUS,ÕIGE/VALE");
    }
	$name = $_REQUEST['name'];
	echo $name;
	array_push($list,$name);
    
    
    $file = fopen($fileName,"a");
    chmod($file,0777);
    foreach ($list as $line){
        fputcsv($file,explode(',',$line));
    }
	

	fclose($file); 
}
?>