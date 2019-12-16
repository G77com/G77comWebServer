<?php
	$server = '200.200.200.19:1433';
	// Connect to MSSQL
	$conn = mssql_connect($server, 'sa', 'P@ssw0rd');
	$connDB=mssql_select_db('WebTest', $conn);
	if (!$connDB) {
		die('Something went wrong while connecting to MSSQL');
	}
	else {
		print($connDB);
		print('connect sucess');
	}
?>
