function callFeed() {
	console.log("Calling feed!")

	$.ajax({
		data : {
				test : "test"
			},
				type : 'POST',
				url : '/feed'
	})
	.done(function(data) {
		console.log("Done!")
		console.log(data);
	});
}
