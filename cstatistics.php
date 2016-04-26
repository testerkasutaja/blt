<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Käänded</title>
	<meta name="description" content=" kaanded">
  	<meta name="author" content="Anneliis Halling">
	
	<link rel="stylesheet" href="css/bootstrap.min.css">
  	<link rel="stylesheet" href="css/custom.css">
	<link href="//maxcdn.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css" rel="stylesheet">
	<script src="js/jquery-2.1.3.min.js"></script>
  	<script src="js/bootstrap.min.js"></script>
	<script src="js/datascripts.js"></script>
	
</head>

<body>
	
	<div class="container">
		<h2>Testi "Leia õige kääne" statistika</h2>

<?php
$cases = array(
        'nimetav' => 0,
        'omastav' => 0,
        'osastav' => 0,
        'sisseütlev' => 0,
        'seesütlev' => 0,
        'seestütlev' => 0,
        'alaleütlev' => 0,
        'alalütlev' => 0,
        'alaltütlev' => 0,
        'saav' => 0,
        'rajav' => 0,
        'olev' => 0,
        'ilmaütlev' => 0,
        'kaasaütlev' => 0,
    );
$casesSum = array(
        'nimetav' => 0,
        'omastav' => 0,
        'osastav' => 0,
        'sisseütlev' => 0,
        'seesütlev' => 0,
        'seestütlev' => 0,
        'alaleütlev' => 0,
        'alalütlev' => 0,
        'alaltütlev' => 0,
        'saav' => 0,
        'rajav' => 0,
        'olev' => 0,
        'ilmaütlev' => 0,
        'kaasaütlev' => 0,
    );

$allFiles = scandir('data/case test',-1);
$files = array_diff($allFiles, array('.', '..'));
foreach($files as $file) {
    $filePath = "data/case test/" . $file;
	
	$f = fopen($filePath, "r");
	if (($line = fgetcsv($f)) !== false) {
        echo "";
	}
	while (($line = fgetcsv($f)) !== false) {
        $case = $line[3];
		$value = $line[6];
        //echo $case . " ".$value . " "; 
        $casesSum[$case] = ++$casesSum[$case];
        if (strcmp($value, 'true') == 0) {
            $cases[$case] = ++$cases[$case];
        }
    }
    fclose($f);
}
echo '<table class="table">';
echo '<thead><tr><th>Kääne</th><th>Kokku lahendatud</th><th>Kokku õigeid</th><th>Õigete vastuste osakaal</th></tr></thead>';
foreach ($casesSum as $kSum => $vSum) {
    foreach ($cases as $k => $v) {
        if (strcmp($kSum, $k) == 0){
            $pr = 0;
            if ($v != 0){
               $pr = $v*100/$vSum; 
            }
            echo '<tr><th>'.$k . "</th><th>" .$vSum . "</th><th>" . $v . "</th><th>" . round($pr)."%";
        }
    }
}


?>
		</div>
	</div>
</body>
</html>