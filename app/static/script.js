
function change_profile(image_url) {

	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function()
	{
		setTimeout('window.location.replace("/profile")', 1000);
	}
	
	httpRequest.open("POST", "/change_profile", true);
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	var data = "check=" + image_url;
	httpRequest.send(data);
}

function change_group(image_url, group_name) {

	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function()
	{
		setTimeout('window.location.replace("/profile")', 1000);
	}
	
	httpRequest.open("POST", "/change_group", true);
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	var data = "check=" + image_url + "|" + group_name;
	httpRequest.send(data);
}

function change_publicity(group_name, change) {

	var httpRequest = new XMLHttpRequest();
	var password = "";

	if(change) {
		password = prompt("Please enter your group's password", "password");
	}

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function()
	{
		setTimeout(location.reload.bind(window.location), 500); 
	}
	
	httpRequest.open("POST", "/change_publicity", true);
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	var data = "check=" + group_name + "|" + password;
	httpRequest.send(data);
}

function become_member(group_name, priv) {

	var httpRequest = new XMLHttpRequest();
	var password = "";
	var error = document.getElementById("error");

	if(priv == "True") {
		password = prompt("This group is private, please enter the password", "password");
	}

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function()
	{
		error.innerHTML = this.responseText;
	}
	
	httpRequest.open("POST", "/become_member", true);
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	var data = "check=" + group_name + "|" + password;
	httpRequest.send(data);

	setTimeout(location.reload.bind(window.location), 300);
}

function remove_member(group_name, username) {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function()
	{
		setTimeout(location.reload.bind(window.location), 200);
	}

	verification = prompt("Please type confirm if you're sure you'd like to remove this user");

	if(verification.toLowerCase() == "confirm") {
		var temp = 1;
	}
	else {
		return;
	}

	httpRequest.open("POST", "/remove_member", true);
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	var data = "check=" + group_name + "|" + username;
	httpRequest.send(data);

	alert("You have successfully removed: " + username);
}

function leave_group(group_name, username) {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function()
	{
		setTimeout(location.reload.bind(window.location), 200);
	}

	verification = prompt("Please type confirm if you're sure you'd like to leave this group");

	if(verification.toLowerCase() == "confirm") {
		var temp = 1;
	}
	else {
		return;
	}

	httpRequest.open("POST", "/remove_member", true);
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	var data = "check=" + group_name + "|" + username;
	httpRequest.send(data);

	alert('You\'ve successfully left group:' + group_name);
}

function become_spectator(group_name) {

	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function()
	{
		location.reload();
	}
	
	httpRequest.open("POST", "/become_spectator", true);
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	var data = "check=" + group_name;
	httpRequest.send(data);
}

function remove_spectate(group_name) {
	var httpRequest = new XMLHttpRequest();

	if(!httpRequest) {
		alert("Giving up");
		return false;
	}

	httpRequest.onreadystatechange = function () {
		location.reload();
	}

	httpRequest.open("POST", "/remove_spectate", true);
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	var data = "check=" + group_name;
	httpRequest.send(data);

	alert("You have successfully stopped spectating: " + group_name);
}

function remove_post(post_id) {
	var httpRequest = new XMLHttpRequest();

	if(!httpRequest) {
		alert("Giving up");
		return false;
	}

	verification = prompt("Please type confirm if you're sure you'd like to remove this post");

	if(verification.toLowerCase() == "confirm") {
		var temp = 1;
	}
	else {
		return;
	}

	httpRequest.onreadystatechange = function () {
		setTimeout(location.reload.bind(window.location), 300);
	}

	httpRequest.open("POST", "/remove_post", true);
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	var data = "check=" + post_id;
	httpRequest.send(data);
}

function add_pokemon(group_id) {
	var pokemon = document.getElementById("searchbar").value.toLowerCase();
	var httpRequest = new XMLHttpRequest();
	var error = document.getElementById("error");

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function()
	{
		error.innerHTML = this.responseText;
		return false;
	}

	httpRequest.open("POST", "/add_pokemon", false);
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	var data = "check=" + group_id + "|" + pokemon;
	httpRequest.send(data);

	setTimeout(location.reload.bind(window.location), 1000);
}

function remove_pokemon(group_id, pokemon) {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() 
	{
		setTimeout(location.reload.bind(window.location), 500); 
	}
	
	httpRequest.open("POST", "/remove_pokemon", true);
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	var data = "check=" + group_id + "|" + pokemon;
	httpRequest.send(data);
}

function add_comment(comment_id, post_id) {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	var body = document.getElementById(comment_id).value;

	if(!body){
		return;
	}

	httpRequest.onreadystatechange = function() 
	{
		setTimeout(location.reload.bind(window.location), 500); 
	}
	
	httpRequest.open("POST", "/add_comment", true);
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	var data = "check=" + post_id + "|" + body;
	httpRequest.send(data);
}

function add_chat(username, message, group) {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() 
	{
		return;
	}

	httpRequest.open("POST", "/add_chat", true);
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	var data = "check=" + username + "|" + message + "|" + group;
	httpRequest.send(data);
}

function edit_record(link_id) {
	var httpRequest = new XMLHttpRequest();

	wins = prompt("Enter the number of wins for this user", "ex) 3");
	losses = prompt("Enter the number of losses for this user", " ex) 2");

	httpRequest.onreadystatechange = function() 
	{
		if(this.responseText.localeCompare("OK!")){
			setTimeout(location.reload.bind(window.location), 300);
		}
		return;
	}

	httpRequest.open("POST", "/edit_record", true);
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	var data = "check=" + wins + "|" + losses + "|" + link_id;
	httpRequest.send(data);
}

function show_comments(id) {
	var comments = document.getElementById(id);

	if(comments.style.display == 'none'){
		comments.style.display = 'initial';
	}
	else{
		comments.style.display = 'none';
	}
}