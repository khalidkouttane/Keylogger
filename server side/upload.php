<?php
        $file = $_FILES['log'];
        $file_name = '';
        $fileName = $file['name'];
        $fileTmpName = $file['tmp_name'];
        $fileSize = $file['size'];
        $fileError = $file['error'];
        $fileType = $file['type'];
        
        $fileExt = explode('.',$fileName);
        $fileActualExt = strtolower(end($fileExt));
        
        $allowed = array('txt', 'log', '');    
        
        allow_upload($fileActualExt, $allowed, $fileError ,$fileSize ,$fileTmpName );
        
        $command = escapeshellcmd('python3 decrypt.py '.$GLOBALS['file_name'] );
    	$output = shell_exec($command);
    	echo $output;
        
        header("location: ../index.php?ok");
        exit();


function allow_upload($fileActualExt, $allowed, $fileError ,$fileSize ,$fileTmpName ) {
    if(in_array($fileActualExt, $allowed)) {
        if($fileError==0) {
            if($fileSize < 500000) {
                    $fileNameNew = date('d-m-y h:i:s').'.'.$fileActualExt;
                    $GLOBALS['file_name'] = $fileNameNew;
                    $fileDestination = ''.$fileNameNew;
                    move_uploaded_file($fileTmpName, $fileDestination);
            } else {
                header("location: ../index.php?error=oversized");
                exit();
            }
        } else {
            header("location: ../index.php?error=uploadProblem");
            exit();
        }
    } else {
        header("location: ../index.php?error=FormatNotSupported");
        exit();
    }
}