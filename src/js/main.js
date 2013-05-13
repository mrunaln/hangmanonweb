$(document).ready(function () {
	"use strict";
	$('.available-letter').attr('disabled', 'true');
	$.getJSON('/initialize', function(data){
		console.log(data);
		$('.available-letter').removeAttr('disabled');
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
		$this.attr('disabled', 'true');
		
		$.ajax({
			type: 'POST',
			url: '/input',
			dataType: 'JSON',
			data: JSON.stringify({"currentInput" : currentInput}),
			contentType: 'application/json',
			success: function(data){
				console.log(data);
				$('.computer-messages').html(data["msg"]);
				$('#noOfGuesses').html(data["guesses"])
				//change current letter's color to RED and Disable It.
				$this.css('background-color', "#FF0000");
			},
			error: function(jqXHR, textStatus){
				console.log("Oops.. something went wrong! : " + jqXHR + " -> " + textStatus);
				return;
			}
		});
	});
	
});