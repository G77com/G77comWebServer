<!doctype html>
<html>
	<!-- head 부분 -->
	<head> 
		<!-- 상단 title -->
		<title>G77 Company</title>

		<!-- CSS Style 지정 -->
		<link rel="stylesheet" href="style_head.css" type="text/css">
	</head>
	<body>
		<?php	session_start();	?>
		<!-- 화면 상단 header 부분 -->
		<div id="area_header">
			<h1>G77 Company</h1>
		</div>
		<!-- 화면 중간 메뉴 부분 -->
		<div id="area_menu">
		<font size = "5px">
			<a href="index_admin.php" target="_parent">   홈</a> 
	<?php	if(!$_SESSION[user_id]): ?>
			| <a href="member/member_login.php" target="_parent">로그인</a> 
			| <a href="member/member_register.php" target="_parent">회원가입</a>  
	<?php	else: ?>
			| <a href="member/member_info_admin.php" target="_parent"><?php echo $_SESSION[nickname]?>님 정보</a>
			| <a href="member/member_logout.php" target="_parent">로그아웃</a> 
			| <a href="member/member_admin.php" target="_parent">관리자페이지</a>
	<?php endif; ?>			
		</div>
	</body>
</html>
