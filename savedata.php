<?php

if( $_REQUEST["name"] ) {
	$list = array
	();


	$name = $_REQUEST['name'];
	echo $name;
	array_push($list,$name);

	$file = fopen("vastused/answersData.csv","a");
	chmod($file,0777);
	
	foreach ($list as $line)
	  {
	  fputcsv($file,explode(',',$line));
	  }

	fclose($file); 
}
?>