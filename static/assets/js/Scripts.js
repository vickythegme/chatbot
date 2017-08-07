/*eslint-env jquery, browser*/
$(function(){
	console.log("inside js function");
	document.getElementsByClassName('time')[0].innerHTML = new Date().toLocaleString();
	var sentHead = "<div class='row' style='margin: 5px 0px;'> <div class='col-sm-offset-4 col-sm-8 text-right' '> <div class='sent text-left' >";
	var receivedHead = "<div class='row' style='margin: 5px 0px;'> <div class='col-sm-8 text-left' '> <div class='received text-left' >";
	var receivedHeadError = "<div class='row' style='margin: 5px 0px;'> <div class='col-sm-8 text-left' '> <div class='received text-left' id='yellow' >";
	var tail = "</div> </div></div>";

	function send() {
		console.log("inside js send function");
		var data = {
			"message" : $("#message").val()
//			"context" : $("#context").val()
};
$(sentHead+data.message+"<div class='time'>"+ new Date().toLocaleString()+"</div>"+tail).hide().appendTo(".chatdiv").show("puff", {times : 3}, 200);
$(".chatdiv").animate({ scrollTop: $(".chatdiv").prop("scrollHeight")}, 1000);
$("#message").val("");

$.post("/",data,function(res,err){

	console.log("inside js post function");
	console.log(data);
	if (err !== "success"){
		console.log("error occured"+err);
		$(receivedHeadError+"Can you please say that again"+"<div class='time'>"+ new Date().toLocaleString()+"</div>"+tail).hide().appendTo(".chatdiv").show("puff", {times : 3}, 200);
				//console.log("inside post2")
				$(".chatdiv").animate({ scrollTop: $(".chatdiv").prop("scrollHeight")}, 1000);
			} else { 
			//console.log("inside post1")
			// console.log(err);
			var spl = res.split('I might need');
			// console.log(spl);
			if(spl.length > 1) {
				$(receivedHeadError+res+"<div class='time'>"+ new Date().toLocaleString()+"</div>"+tail).hide().appendTo(".chatdiv").show("puff", {times : 3}, 200);

			} else {
				$(receivedHead+res+"<div class='time'>"+ new Date().toLocaleString()+"</div>"+tail).hide().appendTo(".chatdiv").show("puff", {times : 3}, 200);
				
			}
			console.log("inside post2")
			$(".chatdiv").animate({ scrollTop: $(".chatdiv").prop("scrollHeight")}, 1000);
		}
			//console.log("inside post3")
		});

}



$("#message").keypress(function(event) {
	if (event.which === 13) {
		event.preventDefault();

		if( $("#message").val() !== "")
			send();
	}
});

$("#send").click(function(event){
		//console.log("send")
		if( $("#message").val() !== "")
			send()
	})

function setInput(text) {
	$("#message").val(text);
		//send()
	}
	
});



