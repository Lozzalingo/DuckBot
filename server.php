<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $input = escapeshellarg($_POST["input"]); // Sanitize user input
    $command = "python3 backend.py " . $input; // Call Python script
    $output = shell_exec($command);
    echo $output ? $output : "Error processing request.";
}
?>
