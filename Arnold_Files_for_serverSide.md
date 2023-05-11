HOW TO DOWNLOAD FOLES FROM YOUR WEBSITE THAT HAVE BEEN UPLOADED ONTO YOUR SERVER
<?php
$file = '/path/to/your/file.ext';  // Path to the file on the server
$filename = 'desired_filename.ext'; // Desired filename for the downloaded file

header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename="' . $filename . '"');
header('Content-Length: ' . filesize($file));

readfile($file);
?>

HOW TO ALLOW THEE WEBSITE TO READ FILES THAT WERE UPLOADED ONTO IT
<?php
$file = '/path/to/your/file.ext';  // Path to the file on the server

// Read the file contents
$fileContent = file_get_contents($file);

// Do something with the file content (e.g., display, process, etc.)
echo $fileContent;
?>

HOW TO READ THE FILE PATH FOR AN  UPLOADED FILE
<form action="upload.php" method="POST" enctype="multipart/form-data">
  <input type="file" name="fileToUpload" id="fileToUpload">
  <input type="submit" value="Upload" name="submit">
</form>


<?php
$targetDirectory = "uploads/"; // The directory where uploaded files will be stored
$targetFile = $targetDirectory . basename($_FILES["fileToUpload"]["name"]);

// Move the uploaded file to the target directory
if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $targetFile)) {
    echo "The file " . basename($_FILES["fileToUpload"]["name"]) . " has been uploaded.";
    echo "File path: " . $targetFile;
} else {
    echo "Sorry, there was an error uploading your file.";
}
?>
Handle the file upload on the server: Create a server-side script (e.g., PHP) to handle the file upload. In the example above, the form's action attribute is set to "upload.php", indicating that the form data will be submitted to the upload.php script. Inside the script, you can access the uploaded file's details, including the file path.


In this example, the uploaded file is stored in the "uploads/" directory with its original name (basename($_FILES["fileToUpload"]["name"])). The file path is then echoed to display it.

