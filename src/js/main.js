$(document).ready(function () {
	"use strict";
	$.getJSON('/initialize', function(data){
		console.log(data);
		$('.brand').html(data.msg);
		$('#noOfGuesses').html(data.guesses);
		
		var secretWord = "";
		for(var i = 0; i < data.secretWordLength; i++){
			secretWord += 	"<div class=\"btn-group \">" + 
								"<button class=\"btn-large secret-letter\" disabled>_</button>" +
							"</div>";
		}
		$('#secretWord').html(secretWord);
		//Welcome To Hangman
		//Guesses
		//Word Length.
	});
	
	
	$('.available-letter').click(function(){
		var $this = $(this);
		var currentInput = $this.html();
		$.ajax({
			type: 'POST',
			url: '/input',
			dataType: 'JSON',
			data: JSON.stringify({"currentInput" : currentInput}),
			contentType: 'application/json',
			success: function(data){
				console.log(data);
				//change current letter's color to RED and Disable It.
			},
			error: function(jqXHR, textStatus){
				console.log("Oops.. something went wrong! : " + jqXHR + " -> " + textStatus);
				return;
			}
		});
	});
	
});