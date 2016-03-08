<?php
$list = array
(
"MÄNG,ID,LAUSE,ÕIGE,VALE"
);
echo $answersStr;
array_push($a,$answersStr);
$file = fopen("answersData.csv","w");

foreach ($list as $line)
  {
  fputcsv($file,explode(',',$line));
  }

fclose($file); ?>