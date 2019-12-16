<?php
        $b_name=$_POST["name"];
        $b_pw=$_POST["pw"];
        $b_email=$_POST["email"];
        $b_sub=$_POST["sub"];
        $b_cont=$_POST["cont"];
        $b_tag=$_POST["tag"];

	//$b_cont=str_replace("<script>","",$b_cont);

	//대소문자 구분X : /문자열/i 대소문자 모두 지정
	//$b_cont=preg_replace("/<script>/i","",$b_cont);

	// '<' 만 없애는 방식으로 바뀜
	//$b_cont=str_replace("<","",$b_cont);
	
	// < 를 스크립트 내에서 부등호로 사용하는 경우도 있어서
	//$b_cont=str_replace("<","&lt",$b_cont);

	//모든 문자를 html entity(&lt..)로 변환
	//$b_cont=htmlspecialchars($b_cont);
	
	//$b_cont = strip_tags($b_cont,'<p><a>');
	
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
        {
          echo "<script>alert('해당 확장자를 가진 파일은 업로드 불가합니다.');history.back();</script>";
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
        /*
         echo "file error:".$_FILES['attachFile']['error'];
        ************ 오류 코드 ***************************
         0 : 성공
         1 : php.ini 의 upload_max_filesize 보다 큽니다.
         2 : html 폼에서 지정한  max file size 보다 큽니다.
         3 : 파일이 일부분만 전송되었습니다.
         4 : 파일이 전송되지 않았습니다.
         6 : 임시 폴더가 없습니다.
         7 : 디스크에 파일 쓰기를 실패하였습니다.
         8 : 확장에 의해 파일 업로드가 중지되었습니다.
        *************************************************
        */

        require "../dbconn.php";

        if($f_error==0){
					 $strSQL="insert into board(strName, strPassword, strEmail, strSubject, strContent, htmlTag, writeDate, filename, filesize) values ('$b_name', '$b_pw', '$b_email', '$b_sub', '$b_cont', '$b_tag', GETDATE(), '$f_rename', '$f_size')";
                $f_rs = move_uploaded_file($f_tmp, $f_path);
		}
		else{
		$strSQL="insert into board(strName, strPassword, strEmail, strSubject, strContent, htmlTag, writeDate) values ('$b_name', '$b_pw', '$b_email', '$b_sub', '$b_cont', '$b_tag', GETDATE())";
		}

        $rs = mssql_query($strSQL);
        if($rs){
                echo "<script>alert('글이 성공적으로 등록 되었습니다.');
                        location.replace('board_list.php');</script>";
        }else{
                echo "<script>alert('글을 등록하는데 실패하였습니다.');
                        history.back();</script>";
        }

?>
