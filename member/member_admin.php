<!doctype html>
<html>
	<!-- head 부분 -->
	<head> 
		<!-- 상단 title -->
		<title>G77 Company</title>
		<!-- CSS Style 지정 -->
		<link rel="stylesheet" href="../style_contents.css" type="text/css">
	</head>
	<body>
		<!-- 화면 상단 header 부분 -->
			<iframe src="../head2.php" id="bodyFrame" name="body" width="100%" height="220px" frameborder="0"></iframe>
		<!-- 화면 하단 body 부분 -->
		<div id="main_contents" class="contents">
			<h1> <br>반갑습니다. 
			<?php 
				session_start();
				if($_SESSION[nickname])
					echo $_SESSION[nickname]."님 ";
			?><br><br><strong>관리자 페이지 입니다</strong></h1>
			<font color="#323232" size="4px">
			<br>관리자 외 사용자는 볼 수 없는 페이지입니다.
			</font>
		</div>
	</body>
</html>
