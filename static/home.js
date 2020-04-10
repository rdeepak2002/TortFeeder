function callFeed() {
	//$('.feedBtn').prop('disabled', true);

	$.ajax({
		data : {
				test : "test"
			},
				type : 'POST',
				url : '/feed'
	})
	.done(function(data) {
		//$('.feedBtn').prop('disabled', false);
		console.log(data);
	});
}
