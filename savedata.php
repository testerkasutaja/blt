<?php

if( $_REQUEST["data"] ) {
	$list = array
	();
    $fileName = date("Y-m-d");
    $fileName = "data/". "answersData_" . $fileName . ".csv";
    if (file_exists($fileName) == false){
        array_push($list,"ID,VASTUS,ÕIGE/VALE");
    }
	$data = $_REQUEST['data'];
	echo $data;
	array_push($list,$data);
    
    
    $file = fopen($fileName,"a");
    chmod($file,0777);
    foreach ($list as $line){
        fputcsv($file,explode(',',$line));
    }
	

	fclose($file); 
}
?>