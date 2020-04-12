function callFeed() {
	console.log("calling feed...")

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
	console.log("checking password...")

	$.ajax({
		data : {
			passIn : "test"
		},
		type : 'POST',
		url : '/checkPassword'
	})
	.done(function(data) {
		alert(data)
	});
}
