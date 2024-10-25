$(document).ready(function(){
  var windowHeight = $(window).height();
  var windowBottom = (windowHeight * -1)/2 + 50;

$(".post_wrapper").find('img').addClass("post_image");

// Contact Modal
  if (window.matchMedia("(min-width: 993px)").matches) {
    $(".modal_content").css('top', '0');
    $("#contact_button").click(function(){
      $(".modal").fadeIn(150);
      $(".modal_content").animate({ top: ($(".modal_content").height() - windowHeight) / 8 }, 300);
    });

    $(".modal_close").click(function(){
      $(".modal").fadeOut(150);
      $(".modal_content").animate({top: '0'}, 300);
    });
} else {
  $(".modal_content").css('top', windowHeight);
  $("#contact_button").click(function(){
    $(".modal").fadeIn(150);
    $(".modal_content").animate({ top: windowHeight - $(".modal_content").height() - 100 }, 300);
  });

  $(".modal_close").click(function(){
    $(".modal").fadeOut(150);
    $(".modal_content").animate({top: windowHeight}, 300);
  });
}
  window.addEventListener("scroll", () => {document.body.style.setProperty("--scroll", window.pageYOffset / (document.body.offsetHeight - window.innerHeight));},false);
});

// Lightbox
$(document).on('click', '.post_image', function() {
    var postImageURL = $(this).attr('src');
    var lightBoxImage = $('<img>').attr({
      src: postImageURL,
      class: "lightbox_image"
    });

    $('.lightbox_image__container').empty();
    $('.lightbox_image__container').append(lightBoxImage);
    $('.lightbox').fadeIn(150);
    $('.lightbox_content').animate({ top: '0' }, 300);
});

$(document).on('click', '.lightbox', function() {
    $(".lightbox").fadeOut(150);
    $(".lightbox_content").animate({ top: '100px' }, 300, function() {
        $(".lightbox_content").css('top', '100px');
    });
});