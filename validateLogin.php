<?php
$user = $_POST['username'];
$pass = $_POST['password'];


if($user=="Admin" && $pass =="pass123")
{
  header("Location:scanFace.html");
}

?>