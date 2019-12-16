<!doctype html>
<html>
	<!-- head 부분 -->
	<head> 
		<!-- 상단 title -->
		<title>G77 Company</title>
		<!-- CSS Style 지정 -->
		<link rel="stylesheet" href="style_contents.css" type="text/css">
	</head>
	<body>
		<!-- 화면 상단 header 부분 -->
			<iframe src="head.php" id="bodyFrame" name="body" width="100%" height="220px" frameborder="0"></iframe>
		<!-- 화면 하단 body 부분 -->
		<div id="main_contents" class="contents">
			<h1>
			<?php 
				session_start();
				if($_SESSION[nickname])
					echo $_SESSION[nickname]."님 ";
			?>도움이 필요하신가요?<br>빠르고 정확하게 해결해 드리겠습니다</h1>
			<font color="#323232" size="4px">
			<br><strong>G77</strong> 고객센터는 IT 비즈니스 전문가들로만 운영되고 있습니다. <br>
			전문가와 상담해 문제를 쉽게 해결하세요.<br>
			질문 게시판를 통해 문의하여 주시기 바랍니다.<br><br><br>
			<strong>대표번호     :     1577-1577 <br><br>
			상담시간     :     평일  09:00 ~ 18:00 </strong>		
			</font>
		</div>
	</body>
</html>
