$(function () {
	let passwordInput = ''
	let isGuest = false

	setup()

	function setup() {
		hideAll()
		setScreenToLogin()
	}

	function hideAll() {
		$('#loginScreen').hide()
		$('#homeScreen').hide()
	}

	function setScreenToHome() {
		$('#loginScreen').fadeOut('slow', function() {
			$('#homeScreen').fadeIn()
		})
	}

	function setScreenToLogin() {
		isGuest = false
		$('#homeScreen').fadeOut('slow', function() {
			$('#loginScreen').fadeIn()
		})
	}

	// Password form clicked
	$('#passwordForm').submit(function(e) {
		e.preventDefault()
		passwordInput = $('#passwordInput').val()

		$.ajax({
			type : 'POST',
			url : '/checkPassword',
			data : {'data':passwordInput}
		})
		.done(function(data) {
			if(data.status == 'correct') {
				setScreenToHome()
			}
		})
	})

	// Conitnue as guest button
	$('#guestBtn').click(function() {
		isGuest = true
		setScreenToHome()
	})

	// Feed button clicked
	$('#feedBtn').click(function() {
		$('#feedBtn').prop('disabled', true)

		$.ajax({
			type : 'POST',
			url : '/feed',
			data : {'data':passwordInput}
		})
		.done(function(data) {
			$('#feedBtn').prop('disabled', false)
			if(data.status == 'invalid') {
				alert('You must be logged in to feed the tortoise!')
			}
			if(data.status == 'failure') {
				alert('Error connecting to servo!')
			}
		})
	})
})
