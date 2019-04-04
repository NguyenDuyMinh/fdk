$(document).ready(function() {
    $("#btnSubmit").click(function(){
    	//$('#navbar').load('layout.html');
    	function getCookie(cname) {
		  var name = cname + "=";
		  var decodedCookie = decodeURIComponent(document.cookie);
		  var ca = decodedCookie.split(';');
		  for(var i = 0; i < ca.length; i++) {
		    var c = ca[i];
		    while (c.charAt(0) == ' ') {
		      c = c.substring(1);
		    }
		    if (c.indexOf(name) == 0) {
		      return c.substring(name.length, c.length);
		    }
		  }
		  return "";
		}
        // Check browser support
		if (typeof(Storage) !== "undefined") {
			var cookieId = 'favs_pro';
			var cookieStr = $("input[name=pro_id]").val();
			var d = new Date();
		  	var exdays = 2;
		  	d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
		  	var expireTime = "expires="+d.toUTCString();
		  	var cookieCurrent = getCookie(cookieId);
		  	var cookieArray = cookieCurrent.split(",");
		  	if (cookieCurrent) {
		  		for(i = 0; i <= cookieArray.length; i++) {
			  		if (cookieArray[i] === cookieStr){
			  			cookieArray.splice(i, 1);
			  			var flag = true; 
			  		}
			  	}
			  	if(flag != true){
			  		cookieArray.push(cookieStr);
			  	}
			  	document.cookie = cookieId+'='+cookieArray+';expires='+expireTime+';path=/';
		  	} else {
		  		//document.cookie = cookieId+'='+cookieStr+';expires='+cookieStr+';domain='+document.domain;
		  		document.cookie = cookieId+'='+cookieStr+';expires='+cookieStr+';path=/';
		  		$("#favorites").addClass("fa fa-heart");
		  	}
		} else {
		  console.log("Sorry, your browser does not support Web Storage...");
		}
    });
});
		  
