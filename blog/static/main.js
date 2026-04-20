$(document).ready(function(){
  var windowHeight = $(window).height();
  var windowBottom = (windowHeight * -1)/2 + 50;
  const menu = $('.nav');
  const work = $('.nav_work');
  const collapsedWidth = menu.width();

  work.show();
  const expandedWidth = menu.outerWidth();
  work.hide();

//  $(".post_body").find('img').addClass("post_image");

  // Highlight selected menu item
  $('.nav_item').click(function() {
    if (!$(this).hasClass("selected")) {
      $('.nav_item').removeClass("selected");
      $(this).addClass("selected");
    }
  });

  // Animate work list

  $('#nav_item__work').click(function() {
    if (work.is(":visible")) {
      work.slideToggle(150);
      menu.delay(200).animate({ width: collapsedWidth }).removeClass("expanded");
    } else {
      menu.animate({ width: 500, duration: expandedWidth }).addClass("expanded");
      work.delay(200).slideToggle();
    }

  });
  $('#nav_item__about').click(function() {
    if (work.is(":visible")) {
      work.slideToggle();
      menu.delay(200).animate({ width: collapsedWidth }).removeClass("expanded");
    }
  });
  $('#nav_item__contact').click(function() {
    if (work.is(":visible")) {
      work.slideToggle();
      menu.delay(200).animate({ width: collapsedWidth }).removeClass("expanded");
    }
  });

  function handleScroll(){
    const scrollTop = $(window).scrollTop();
    const workTop = $('.work').offset();
    const logo = $('.logo_link');

    if (window.matchMedia("(min-width: 993px)").matches) {
      if (workTop && scrollTop >= workTop.top - 128) {
        menu.addClass('opaque');
        logo.addClass('opaque');
      } else {
        menu.removeClass('opaque');
        logo.removeClass('opaque');
      }
    } else {
      if (scrollTop >= 200) {
        menu.addClass('opaque');
        logo.addClass('opaque');
      } else {
        menu.removeClass('opaque');
        logo.removeClass('opaque');
      }
    }
  }

  $(window).on('scroll', handleScroll);
  $(document).ready(handleScroll);

});