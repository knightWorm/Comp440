
//This sis the number of attemps a user can make 
var attemps = 3;

//Validation function
function validate(){
	var username = document.getElementById("username").value;
	var password = document.getElementById("password").value;

	if(username=="ron1" && password == "123"){

		alert("Login Successful");
		// window.location = "index.html"
		return window.location.refresh();
	

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
function refresh(){

	window.location.href = window.location.href;
}

function checkUsername() {
	var username = document.getElementById("createUsername").value;

	if(username.length == 0){
		return false;
	}
	/*else if(username == database value){
		return false;
	}*/
	else{
		return true;
	}
}

function checkEmail() {
	var email = document.getElementById("createEmail").value;

	if(email.length == 0){
		return false;
	}
	/*else if(username == database value){
		return false;
	}*/
	else{
		return true;
	}
}

//take the ID's from html and set to these variables
let createPassword = document.querySelector('#createPassword');
let confirmPassword = document.querySelector('#confirmPassword');
let result = document.querySelector('h3');

//if passwords match say matching, else not matching
//used in validAccount()
function passwordMatch(){
	var pass1 = document.getElementById("createPassword").value;
	var pass2 = document.getElementById("confirmPassword").value;
	result.innerText = createPassword.value == confirmPassword.value ? 'Password Matches' : 'Password Mismatch';

	if(pass1.length == 0 || pass2.length == 0){
		return false;
	}
	else if(result.innerText == 'Password Matches'){
		return true;
	}
	else{
		return false;
	}
}

createPassword.addEventListener('keyup', () => {
	if (confirmPassword.value.length != 0) passwordMatch();
})

confirmPassword.addEventListener('keyup', passwordMatch);


//for create account button, checks fields to see if username or email already exists in database
//checks to see if the password fields match
//if every field is valid it will create an account, add user data to database, then return user to sign in page
function validateAccount(){
	
	if(checkUsername() == false){
		alert("Username not valid");
		return window.location.reload();
	}
	else if(checkEmail() == false){
		alert("Email not valid");
		return window.location.reload();
	}
	else if(passwordMatch() == false){
		alert("Password not valid");
		return window.location.reload();
	}
	else if(checkUsername() == true && checkEmail() == true && passwordMatch() == true){
		alert("Account Created");
		return window.location.replace("index.html");
	}
	else{
		alert("Something not valid");
		return window.location.reload();
	}
	
}