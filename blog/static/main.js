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
    const logo = $('.logo_link');
    let opaque = false;

    // Large desktop: nav sits clear of the content, so it stays transparent
    // (the .expanded class still gives it a background when the menu is open)
    if (!window.matchMedia("(min-width: 1740px)").matches) {
      // Go opaque once the bottom of the fixed nav/logo reaches the headline
      const target = $('.page_title h1')[0] || $('.work')[0];
      if (target) {
        const navBottom = Math.max(
          ...$('.nav:visible, .logo_link:visible').map(function() {
            return this.getBoundingClientRect().bottom;
          }).get(),
          0
        );
        opaque = target.getBoundingClientRect().top <= navBottom;
      }
    }

    menu.toggleClass('opaque', opaque);
    logo.toggleClass('opaque', opaque);
  }

  $(window).on('scroll resize', handleScroll);
  $(document).ready(handleScroll);

});