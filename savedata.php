<p id = "string"></p>

<?php
$list = array
(
"MÄNG,ID,LAUSE,ÕIGE,VALE"
);

$answersStr = $_POST['variable'];

array_push($list,$answersStr);


$file = fopen("answersData.csv","w");

foreach ($list as $line)
  {
  fputcsv($file,explode(',',$line));
  }

fclose($file); ?>