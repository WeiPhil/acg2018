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

$(function() {
    $('a[href*=#]').click(function(){
        $('html, body').animate({
            scrollTop: $(this.hash).offset().top
        }, 'quick');
        return false;
    });
});