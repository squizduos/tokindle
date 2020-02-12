$(document).ready(function(){
	$(window).resize(function(){
		$(".welcome .intro").css('margin-top', (parseInt($(".welcome .kindle").css("height")) - parseInt($(".welcome .intro").css("height")))/2);
		$(".welcome").css('margin-top', (parseInt($("html").css("height")) - parseInt($(".welcome").css("height")))/2 );
		$(".subscribe").css('margin-top',(parseInt($("html").css("height")) - parseInt($(".subscribe").css("height")))/2);
		$(".unsubscribe").css('margin-top',(parseInt($("html").css("height")) - parseInt($(".unsubscribe").css("height")))/2);
	});
	
	$(window).resize();

	$('.subscribe-button').click(function(e) {
		$.ajax({type: "POST", url: "/action/", data: $("form.subscribe").serialize(), success: function(msg){ eval(msg); }});
		return false;
	//	$('.reveal-modal').reveal();
	});
	
	$('input, select').styler();

});
function showTopBox(message){
	//$("#note").fadeIn();
	$("#note").html(message).show().animate({"top": "0px", "opacity":1}, 500, function(){
		setTimeout(function(){ $("#note").animate({"top": "-50px", "opacity":0}, 500);}, 4000);
	});
}