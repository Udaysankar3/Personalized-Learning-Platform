<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Database connection settings
$servername = "localhost";
$username = "root"; // Update if necessary
$password = ""; // Update if necessary
$dbname = "personalized_learning_platform"; // Replace with your database name

// Create a connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    header('Content-Type: application/json');
    echo json_encode(['status' => 'error', 'message' => 'Database connection failed: ' . $conn->connect_error]);
    exit;
}

// Get the username and password from the request
$inputUsername = $_POST['user'] ?? '';
$inputPassword = $_POST['pass'] ?? '';

if (empty($inputUsername) || empty($inputPassword)) {
    header('Content-Type: application/json');
    echo json_encode(['status' => 'error', 'message' => 'Username or password is missing']);
    exit;
}

// Prepare and execute the SQL query to validate the credentials
$sql = "SELECT * FROM register WHERE user = ? AND pass = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param('ss', $inputUsername, $inputPassword);
$stmt->execute();
$result = $stmt->get_result();

header('Content-Type: application/json');  // Ensure the response is JSON

if ($result->num_rows > 0) {
    echo json_encode(['status' => 'success', 'message' => 'Login successful!']);
} else {
    echo json_encode(['status' => 'error', 'message' => 'Invalid username or password']);
}

// Close the connection
$stmt->close();
$conn->close();
?>
