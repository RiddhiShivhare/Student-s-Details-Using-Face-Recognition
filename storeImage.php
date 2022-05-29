
<?php
    $img = $_POST['image'];
    $folderPath = "uploads/";
  
    $image_parts = explode(";base64,", $img);
    $image_type_aux = explode("image/", $image_parts[0]);
    $image_type = $image_type_aux[1];
  
    $image_base64 = base64_decode($image_parts[1]);
    
      $fileName = uniqid() . '.png';  
 
    
    
    $file = $folderPath . $fileName;
    file_put_contents($file, $image_base64);
  
    echo"<b>Image Captured and Stored Successfully !</b>";
     
?>
 <?php
 header("Location: http://localhost:5000");
  exit();
?>