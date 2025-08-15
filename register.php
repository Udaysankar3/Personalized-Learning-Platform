<?php
$servername = "localhost";
$username = "root"; 
$password = ""; 
$dbname = "Personalized_Learning_Platform"; 


$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}


$user = $_POST['username'];
$pass = $_POST['password'];
$gender = $_POST['gender'];
$dob = $_POST['dob'];
$mobile = $_POST['mobile'];
$degree = $_POST['degree'];
$interests = $_POST['interests'];


$sql = "INSERT INTO register (user, pass, gender, dob, mobile, degree, interests)
VALUES ('$user', '$pass', '$gender', '$dob', '$mobile', '$degree', '$interests')";

if ($conn->query($sql) === TRUE) {
  echo "Registration successful!";
} else {
  echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
