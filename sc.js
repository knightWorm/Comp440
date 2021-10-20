
//This sis the number of attemps a user can make 
var attemps = 3;

//Validation function
function validate(){
	var username = document.getElementById("username").value;
	var password = document.getElementById("password").value;

	if(username=="ron1" && password == "123"){

		alert("Login Successful");
		// window.location = "index.html"
		return false;

	}else{
		attemps --;
		alert("Login Faield!\n Attemps left: "+ attemps);

		if(attemps == 0){
			document.getElementById("username").disabled = true;
			document.getElementById("password").disabled = true;
			document.getElementById("submit").disabled = true;
		}
		return false;

	}
}