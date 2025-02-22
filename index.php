<!DOCTYPE html>
<html>

	<!--Metadata-->
	<head>
  
		<!--Title-->
		<title>Linksure | Your path to an insured life.</title>
		
	<!--CSS-->
		
		<!--Bootstrap Stylesheet-->
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
		<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
		
		<!--Custon Stylesheet-->
		<link rel="stylesheet" type="text/css" href="css/index.css" />
  
	</head>
	
	<!--Webpage Body-->
	<body>
	
		<!--Navigation Bar-->
		<?php include("navigation_bar.php");?>
		
		
		<!--Main Jumbotron-->
		<div id="jumbotron" class="p-5 bg-primary text-white">
		
			<!--Title-->
			<h1 class="font-weight-bolder">Linksure</h1>
					
			<!--Search Bar-->
			<div class="mb-3">
						
				<!--Button-->
				<button id="search-btn" class="btn btn-primary mt-3">Try our Insurance Plan Matcher</button>
						
		</div>

		<!--JavaScript-->
		<script>
		 
			//Check if Search Button is Clicked
			document.getElementById("search-btn").addEventListener("click", function () {
					
				//Go to the Insurance Matcher
				window.location.href = "insurance_matcher_form.php";
		
			});

		</script>

	
	
	</body>
  
</html>
