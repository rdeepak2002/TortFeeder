$(function () {
	let passwordInput = ''
	let isGuest = false

	setup()

	// Initial method called
	function setup() {
		hideAll()
		setScreenToLogin()
	}

	// Hide all screens and elements
	function hideAll() {
		$('#loginScreen').hide()
		$('#homeScreen').hide()
	}

	// Set screen to home screen
	function setScreenToHome() {
		if(isGuest) {
			$('#feedBtn').hide()
		}
		else {
			$('#feedBtn').show()
		}
		$('#loginScreen').fadeOut('slow', function() {
			$('#homeScreen').fadeIn()
		})
	}

	// Set screen to loginscreen
	function setScreenToLogin() {
		isGuest = false
		$('#homeScreen').fadeOut('slow', function() {
			$('#loginScreen').fadeIn()
		})
	}

	// Password form clicked
	$('#passwordForm').submit(function(e) {
		e.preventDefault()
		passwordInput = $('#passwordInput').val().trim()

		$('#loginScreen').fadeOut('slow', function() {
			$('.loader').fadeIn('slow')

			$.ajax({
				type : 'POST',
				url : '/checkPassword',
				data : {'data':passwordInput}
			})
			.done(function(data) {
				$('.loader').fadeOut('slow', function() {
					if(data.status == 'correct') {
						setScreenToHome()
					}
					if(data.status == 'incorrect') {
						$('#loginScreen').show()
						$('#loginScreen').effect('shake')
					}
				})
			})
		})
	})

	// Continue as guest button
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

	// Sign out button clicked
	$('#signOutBtn').click(function() {
		setScreenToLogin()
	})
})
