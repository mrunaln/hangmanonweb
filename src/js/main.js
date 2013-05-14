$(document).ready(function () {
	"use strict";
	$('.available-letter').attr('disabled', 'true');
	
	$.ajax({
		type: 'GET',
		url: '/initialize',
		dataType: 'JSON',
		contentType: 'application/json',
		success: function(data){
			console.log(data);
			$('.available-letter').removeAttr('disabled');
			$('.brand').html(data.msg);
			$('#noOfGuesses').html(data.guesses);
			
			var secretWord = "";
			for(var i = 0; i < data.secretWordLength; i++){
				secretWord += 	"<div class=\"btn-group \">" + 
									"<button id=\"s" + i + "\" class=\"btn-large secret-letter\" disabled>_</button>" +
								"</div>";
			}
			$('#secretWord').html(secretWord);

		},
		
	});
	/*$.getJSON('/initialize', function(data){
		//Welcome To Hangman
		//Guesses
		//Word Length.
	});
	*/
	
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
				$.each(data.guessedWord, function(idx, value){
					$("#s" + value).html(currentInput);
				});
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