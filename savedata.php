<?php

if( $_REQUEST["name"] ) {
	$list = array
	(
	"MÄNG,ID,LAUSE,ÕIGE,VALE"
	);


	$name = $_REQUEST['name'];
	echo $name;
	array_push($list,$name);

	$file = fopen("answersData.csv","w");

	foreach ($list as $line)
	  {
	  fputcsv($file,explode(',',$line));
	  }

	fclose($file); 
}
?>