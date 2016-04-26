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
		<h2>Ebasobivad laused</h2>
		<div class="input-group"> <span class="input-group-addon">Filtreeri</span>
			<input id="filter" type="text" class="form-control" placeholder="Sisesta otsing...">
		</div>
<?php


$allFiles = scandir('data/unsuitableSentences',-1);
$files = array_diff($allFiles, array('.', '..'));
foreach($files as $file) {
	print_r($file);
	displayData($file);
}

function displayData($filePath) {
	$filePath = "data/unsuitableSentences/" . $filePath;
	echo '<table class="table">';
	$f = fopen($filePath, "r");
	if (($line = fgetcsv($f)) !== false) {
		echo '<thead><tr><th>'.implode('</th><th>',$line).'</th></tr></thead>';
	}
	while (($line = fgetcsv($f)) !== false) {
		echo '<tbody class="searchable">';
		echo "<tr>";
        foreach ($line as $cell) {
			echo "<td>" . htmlspecialchars($cell) . "</td>";
        }
        echo "</tr>\n";
		echo "</tbody>";
}
fclose($f);
echo "\n</table>";
	}


?>
		</div>
	</div>
</body>
</html>
