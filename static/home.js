$(function () {
	let passwordInput = ''
	let isGuest = false

	setup()

	// Initial method called
	function setup() {
		hideAll()

		$('#videoFeed').on('load', function() {
			$('.loader').fadeOut('slow', function() {
				let passwordCookie = getCookie('password')
				if(passwordCookie) {
					// Check if password cookie is correct
					$.ajax({
						type : 'POST',
						url : '/checkPassword',
						data : {'data':passwordCookie}
					})
					.done(function(data) {
						$('.loader').fadeOut('slow', function() {
							if(data.status == 'correct') {
								setCookie('password', passwordCookie, 360)
								setScreenToHome()
							}
							if(data.status == 'incorrect') {
								eraseCookie('password')
								$('#loginScreen').show()
								$('#loginScreen').effect('shake')
								setScreenToLogin()
							}
						})
					})
				}
				else {
					setScreenToLogin()
				}
			})
		})
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
						setCookie('password', passwordInput, 360)
						setScreenToHome()
					}
					if(data.status == 'incorrect') {
						eraseCookie('password')
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
		eraseCookie('password')
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
		eraseCookie('password')
		setScreenToLogin()
	})

	// Methods to manage password cookie
	function setCookie(name,value,days) {
		var expires = ''
		if (days) {
			var date = new Date()
			date.setTime(date.getTime() + (days*24*60*60*1000))
			expires = '; expires=' + date.toUTCString()
		}
		document.cookie = name + '=' + (value || '')  + expires + '; path=/'
	}

	function getCookie(name) {
		var nameEQ = name + '='
		var ca = document.cookie.split(';')
		for(var i=0;i < ca.length;i++) {
			var c = ca[i]
			while (c.charAt(0)==' ') c = c.substring(1,c.length)
			if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length)
		}
		return null
	}

	function eraseCookie(name) {
		document.cookie = name+'=; Max-Age=-99999999;'
	}
})
