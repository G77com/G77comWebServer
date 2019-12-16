<?php
//DB 연결
$file_name = urldecode($_GET['filename']);
$file_name = str_replace("../","",$file_name);

require("../dbconn.php");
$strSQL = "select * from board where filename='{$file_name}'";
$result = mssql_query($strSQL);
$rs_row = mssql_fetch_assoc($result);


$filename = $rs_row['filename'];
$fileDir = "/var/www/html/board/upload";
$fullPath = $fileDir."/".$filename;
$size = filesize($fullPath);
 
header("Content-Type: application/octet-stream");
header("Content-Disposition: attachment; filename=".$filename."");
header("Content-Transfer-Encoding: binary");
header("Content-Length: ".$size);
header("Cache-Control: cache, must-revalidate");
header("Pragma: no-cache");
header("Expires: 0");
 
$fh = fopen($fullPath, "r");
fpassthru($fh); 
fclolse($fh);
 
?>

