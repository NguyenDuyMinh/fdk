$(document).ready(function() {
    $("#btnSubmit").click(function(){
        // Check browser support
		if (typeof(Storage) !== "undefined") {
		  // Store
		  var proId = $("input[name=pro_id]").val();
		  var d = new Date();
		  var exdays = 2;
		  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
		  var expires = "expires="+d.toUTCString();
		  document.cookie = proId + "=" + proId + ";" + expires + ";path=/";
		  $("#favorites").addClass("fa fa-heart");
		} else {
		  console.log("Sorry, your browser does not support Web Storage...");
		}
    });
});
//$("input[name=pro_id]").val();
// function getCookie(cname) {
//   var name = cname + "=";
//   var ca = document.cookie.split(';');
//   for(var i = 0; i < ca.length; i++) {
//     var c = ca[i];
//     while (c.charAt(0) == ' ') {
//       c = c.substring(1);
//     }
//     if (c.indexOf(name) == 0) {
//       return c.substring(name.length, c.length);
//     }
//   }
//   return "";
// }
// var d = new Date();
// var exdays = 2;
// d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
// var expires = "expires="+d.toUTCString();
// document.cookie = proId + "=" + proId + ";" + expires + ";path=/";
// if (sessionStorage.getItem(proId)) {
// 	sessionStorage.removeItem(proId);
// 	$("#favorites").removeClass("fa fa-heart");
// } else {
// 	sessionStorage.setItem(proId, proId);
// 	$("#favorites").addClass("fa fa-heart");
// }
		  
