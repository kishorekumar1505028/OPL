(function ($) {
  "use strict"

  // NAVIGATION
  var responsiveNav = $('#responsive-nav'),
    catToggle = $('#responsive-nav .category-nav .category-header'),
    catList = $('#responsive-nav .category-nav .category-list'),
    menuToggle = $('#responsive-nav .menu-nav .menu-header'),
    menuList = $('#responsive-nav .menu-nav .menu-list'),
    primarybtn = $('#kukkuru'),
    priceslider = $('#price-slider');

  catToggle.on('click', function () {
    menuList.removeClass('open');
    catList.toggleClass('open');
  });

  menuToggle.on('click', function () {
    catList.removeClass('open');
    menuList.toggleClass('open');
  });

  primarybtn.on('click', function () {
    alert("hi");
  });

  $(document).click(function (event) {
    if (!$(event.target).closest(responsiveNav).length) {
      if (responsiveNav.hasClass('open')) {
        responsiveNav.removeClass('open');
        $('#navigation').removeClass('shadow');
      } else {
        if ($(event.target).closest('.nav-toggle > button').length) {
          if (!menuList.hasClass('open') && !catList.hasClass('open')) {
            menuList.addClass('open');
          }
          $('#navigation').addClass('shadow');
          responsiveNav.addClass('open');
        }
      }
    }
  });

  // HOME SLICK
  $('#home-slick').slick({
    autoplay: true,
    infinite: true,
    speed: 300,
    arrows: true,
  });

  // PRODUCTS SLICK
  $('#product-slick-1').slick({
    slidesToShow: 3,
    slidesToScroll: 2,
    autoplay: true,
    infinite: true,
    speed: 300,
    dots: true,
    arrows: false,
    appendDots: '.product-slick-dots-1',
    responsive: [{
      breakpoint: 991,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
      }
    },
    {
      breakpoint: 480,
      settings: {
        dots: false,
        arrows: true,
        slidesToShow: 1,
        slidesToScroll: 1,
      }
    },
    ]
  });

  $('#product-slick-2').slick({
    slidesToShow: 3,
    slidesToScroll: 2,
    autoplay: true,
    infinite: true,
    speed: 300,
    dots: true,
    arrows: false,
    appendDots: '.product-slick-dots-2',
    responsive: [{
      breakpoint: 991,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
      }
    },
    {
      breakpoint: 480,
      settings: {
        dots: false,
        arrows: true,
        slidesToShow: 1,
        slidesToScroll: 1,
      }
    },
    ]
  });

  // PRODUCT DETAILS SLICK
  $('#product-main-view').slick({
    infinite: true,
    speed: 300,
    dots: false,
    arrows: true,
    fade: true,
    asNavFor: '#product-view',
  });

  $('#product-view').slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    arrows: true,
    centerMode: true,
    focusOnSelect: true,
    asNavFor: '#product-main-view',
  });

  // PRODUCT ZOOM
  $('#product-main-view .product-view').zoom();

  // PRICE SLIDER
  var slider = document.getElementById('price-slider');
  if (slider) {
    noUiSlider.create(slider, {
      start: [1, 999],
      connect: true,
      tooltips: [true, true],
      format: {
        to: function (value) {
          return value.toFixed(2) + '$';
        },
        from: function (value) {
          return value
        }
      },
      range: {
        'min': 1,
        'max': 999
      }
    });
  }
  //extracting min and max val from slider
  slider.noUiSlider.on('change', function () {
    alert("hi all");
    var vals = slider.noUiSlider.get();
    var minval = Number(vals[0].slice(0, vals[0].length - 1));
    var maxval = Number(vals[1].slice(0, vals[1].length - 1));

    console.log(typeof (minval) + minval + typeof (maxval) + maxval);
  });



})(jQuery);

var elements = document.getElementsByClassName("dummy");
var elements2 = document.getElementsByClassName("dummy2");

console.log("elements of row" + elements);
// Declare a loop variable
var i;

// List View
function listView() {
  console.log("elements of row in listview" + elements.length);
  for (i = 0; i < elements.length; i++) {
    console.log(elements[i]);
    elements[i].className = elements[i].className.replace(" grid-view", " list-view");

  }
  for (i = 0; i < elements2.length; i++) {
    //console.log(elements2[i]);
    //elements2[i].className = elements2[i].className.replace(" col-md-4", " fook");

  }
}

// Grid View
function gridView() {
  console.log("elements of row in gridview" + elements);
  for (i = 0; i < elements.length; i++) {
    elements[i].className = elements[i].className.replace(" list-view", " grid-view");
  }
  for (i = 0; i < elements2.length; i++) {
    //console.log(elements2[i]);
    //elements2[i].className = elements2[i].className.replace(" fook", " col-md-4");

  }
}

/* Optional: Add active class to the current button (highlight it) */
var container = document.getElementById("row-filter");
var btns = document.getElementsByClassName("view-button");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function () {
    var current = document.getElementsByClassName("view-active");
    console.log(current);
    current[0].className = current[0].className.replace(" view-active", "");
    this.className += " view-active";
  });
}


