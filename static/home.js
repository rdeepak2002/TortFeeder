function callFeed() {
	$.ajax({
		data : {
				test : "test"
			},
				type : 'POST',
				url : '/feed'
	})
	.done(function(data) {
		console.log(data);
	});
}
