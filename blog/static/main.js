$(document).ready(function(){
  var windowHeight = $(window).height();
  var windowBottom = (windowHeight * -1)/2 + 50;

  if (window.matchMedia("(min-width: 993px)").matches) {
    $(".modal_content").css('top', '0');
    $("#contact_button").click(function(){
      $(".modal").fadeIn(150);
      $(".modal_content").animate({ top: ($(".modal_content").height() - windowHeight) / 8 }, 300);
    });

    $(".close").click(function(){
      $(".modal").fadeOut(150);
      $(".modal_content").animate({top: '0'}, 300);
    });
} else {
  $(".modal_content").css('top', windowHeight);
  $("#contact_button").click(function(){
    $(".modal").fadeIn(150);
    $(".modal_content").animate({ top: windowHeight - $(".modal_content").height() - 100 }, 300);
  });

  $(".close").click(function(){
    $(".modal").fadeOut(150);
    $(".modal_content").animate({top: windowHeight}, 300);
  });
}
  window.addEventListener("scroll", () => {document.body.style.setProperty("--scroll", window.pageYOffset / (document.body.offsetHeight - window.innerHeight));},false);
});