// JavaScript Document

function getLeaf(url) {
 var splited=url.split('?');// remove all the parameter from url
 url=splited[0];
 return url.substring(url.lastIndexOf("/")+1);// return file name without domain and path
} 
// logo sliding
$(function() {
    var offset = $("#logo").offset();
    var topPadding = 15;
    $(window).scroll(function() {
        if ($(window).scrollTop() > offset.top) {
            $("#logo").stop().animate({
                marginTop: $(window).scrollTop() - offset.top + topPadding
            });
        } else {
            $("#logo").stop().animate({
                marginTop: 0
            });
        };
    });

    
});

// Scrolls to the top
$(function() {
    $('a[href=#top]').click(function(){
        $('html, body').animate({scrollTop:0}, 'slow');
        return false;
    });
});

// menu buttons image change
jQuery.fn.extend({
 enter: function() {//plugins creation
     return this.each(function() {
       var pth = $(this).find("img")[0];
	   //alert($(this).children().attr("href"));
	    if($(this).children().attr("href")==getLeaf(document.location.href)){// check that the link url and document url is same
           $(pth).attr("src",pth.src.replace(/.gif/g, '_active.gif'));
		 } else{
               $(this).hover(function(){
                  $(pth).attr("src",pth.src.replace(/.gif/g, '_active.gif'));// mouse over Image
                  },function(){
                      $(pth).attr("src",pth.src.replace(/_active.gif/g, '.gif'));// mouse out image
                      });
               }
               });
     }
});
$(function(){  // Document is ready
 $("li").enter();// call the function
});