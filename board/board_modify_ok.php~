<?php
	$r_num = $_GET[num];
	$r_pass = $_POST[b_pass];
	$b_name=$_POST["name"];	
	$b_email=$_POST["email"];
	$b_sub=$_POST["sub"];
	$b_cont=$_POST["cont"];
	$b_tag=$_POST["tag"];

	// html 사용안하는 게시글은 html encoding 처리
	if($b_tag == "F"){
			$b_cont = htmlspecialchars($b_cont);
	}

	// file 정보 받기
	// $_FILES : form 에서 file type으로 넘어오면 여러가지 정보가 넘어오는데 이런 정보를 받아주는 슈퍼글로벌 변수
	$f_error=$_FILES["att_file"]["error"];
	if($f_error==0){
			$f_name=$_FILES["att_file"]["name"];

	//$f_name 의 확장자가 .php 또는 .html .html인경우 업로드 불가
	//if(eregi(".php|.html|.htm"),$f_name)
	if(preg_match("/(.php|.html|.htm)/i",$f_name))
	{  echo "<script>alert('해당 확장자를 가진 파일은 업로드 불가합니다.');history.back();</script>";
	  exit;
	}

			$f_path="upload/".$f_name;
			$f_tmp=$_FILES["att_file"]["tmp_name"];
			$f_size=$_FILES["att_file"]["size"];

			// 같은 이름의 파일이 있을 경우 이름 뒤에 숫자 붙이기
			$f_rename=$f_name;
			for($i=1; is_file($f_path); $i++){
			$f_rename=$f_name."(".$i.")";
			$f_path="./upload/".$f_rename;
			}
	}else if($f_error!=4){
			echo "<script>alert('파일 업로드 실패($f_error)');
					history.back();</script>";
					exit;
	}

	require("../dbconn.php");
	
	$strSQL="select strNumber,strPassword,filename from board where strNumber=$r_num ";
	//echo $strSQL;
	$rs = mssql_query($strSQL);
	$rs_arr = mssql_fetch_array($rs);

	if($rs_arr){
		if(is_file("upload/$rs_arr[filename]")){		
			unlink("upload/$rs_arr[filename]");
		}
		$strSQL="update board set strName='$b_name', strEmail='$b_email', strSubject='$b_sub', htmlTag='$b_tag', strContent='$b_cont' ";
		if($f_error==0)
        {
                $strSQL.=", filename='$f_rename', filesize='$f_size'";
                $f_rs = move_uploaded_file($f_tmp, $f_path);
		}
		$strSQL.=" where strNumber=$r_num ";
		$rs = mssql_query($strSQL);
		if($rs){
			echo "<script>alert('게시물이 수정 되었습니다.');
			location.replace('board_list.php');</script>";
		}
	}else{
		echo "<script>alert('게시물을 수정 할 수 없습니다.');
			history.back();</script>";
	}
?>
