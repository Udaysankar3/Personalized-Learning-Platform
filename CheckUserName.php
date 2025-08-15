<?php
$servername = "localhost";
$username = "root";  // Update if necessary
$password = "";  // Update if necessary
$dbname = "personalized_learning_platform";  // Replace with your database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get the username from the POST request
$inputUsername = $_POST['user'] ?? '';

// Prepare and execute the SQL query
$sql = "SELECT * FROM register WHERE user = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param('s', $inputUsername);
$stmt->execute();
$result = $stmt->get_result();

// Return a JSON response indicating whether the username exists
header('Content-Type: application/json');
if ($result->num_rows > 0) {
    echo json_encode(['exists' => true]);  // Username exists
} else {
    echo json_encode(['exists' => false]);  // Username does not exist
}

// Close connection
$stmt->close();
$conn->close();
?>
