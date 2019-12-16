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
			<a href="index.php" target="_parent">   홈</a> 
			| <a href="board/board_list.php" target="_parent">   제품    </a> 
			| <a href="board/board_list.php" target="_parent">   서비스    </a> 
			| <a href="board/board_list.php" target="_parent">   질문 게시판   </a> 
	<?php	if(!$_SESSION[user_id]): ?>
			| <a href="member/member_login.php" target="_parent">로그인</a> 
			| <a href="member/member_register.php" target="_parent">회원가입</a>  
	<?php	else: ?>
			| <a href="member/member_info.php" target="_parent"><?php echo $_SESSION[nickname]?>님 정보</a>
			| <a href="member/member_nick.php" target="_parent">닉네임수정</a>
			| <a href="member/member_logout.php" target="_parent">로그아웃</a> 
	<?php endif; ?>			
		</div>
	</body>
</html>
