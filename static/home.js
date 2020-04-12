function callFeed() {
	$('.feedBtn').prop('disabled', true);

	$.ajax({
		type : 'POST',
		url : '/feed'
	})
	.done(function(data) {
		$('.feedBtn').prop('disabled', false);
		console.log(data);
	});
}

function checkPassword() {
	passwordInput = $('#passwordInput').val();

	$.ajax({
		type : 'POST',
		url : '/checkPassword',
		data : {'data':sha256(passwordInput)}
	})
	.done(function(data) {
		console.log(data)
	});
}
