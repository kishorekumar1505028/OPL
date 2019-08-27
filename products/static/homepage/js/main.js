(function ($) {
    "use strict";

    // NAVIGATION
    var minMaxcontent;
    var slider;
    var minMax;
    var showNumber;
    var sortBy;
    var productMinval;
    var productMaxval;
    var productMinvalstr;
    var productMaxvalstr;
    var reverseList = false;

    var responsiveNav = $('#responsive-nav'),
        catToggle = $('#responsive-nav .category-nav .category-header'),
        catList = $('#responsive-nav .category-nav .category-list'),
        menuToggle = $('#responsive-nav .menu-nav .menu-header'),
        menuList = $('#responsive-nav .menu-nav .menu-list');
    var sliderMaxval;
    var sliderMinval;
    var sliderVals;

    console.log(typeof (responsiveNav));
    console.log(typeof (catToggle));
    console.log(typeof (catList));
    console.log(typeof (menuToggle));
    console.log(typeof (menuList));
    catToggle.on('click', function () {
        menuList.removeClass('open');
        catList.toggleClass('open');
    });

    menuToggle.on('click', function () {
        catList.removeClass('open');
        menuList.toggleClass('open');
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
    function get_product_slick_settings() {
        return {
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
        }
    }

    $('#product-slick-1').slick(get_product_slick_settings());

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


    //price slider
    slider = document.getElementById('price-slider');

    //min price and max_price
    minMaxcontent = document.getElementById('min_max_val')
    if (minMaxcontent)
        minMax = minMaxcontent.textContent;

    //sort_option
    if ($('#sort_by option:selected'))
        sortBy = $('#sort_by option:selected').text();

    if ($('#show_number option:selected'))
        showNumber = $('#show_number option:selected').text();


    if (slider) {
        productMaxvalstr = minMax.slice(1, minMax.search(","));
        productMinvalstr = minMax.slice(minMax.search(",") + 2, minMax.length - 1);
        productMaxval = parseInt(productMaxvalstr);
        productMinval = parseInt(productMinvalstr);
        sliderMinval = productMinval
        sliderMaxval = productMaxval

        noUiSlider.create(slider, {
            start: [productMinvalstr, productMaxvalstr],
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
                'min': productMinval,
                'max': productMaxval
            }
        });
        //extracting min and max val from slider
        slider.noUiSlider.on('change', function () {
            sliderVals = slider.noUiSlider.get();
            sliderMinval = Number(sliderVals[0].slice(0, sliderVals[0].length - 1));
            sliderMaxval = Number(sliderVals[1].slice(0, sliderVals[1].length - 1));


        });

    }

    $('#show_number').on('change', function () {
        showNumber = $('#show_number option:selected').text();
    });

    $('#sort_by').on('change', function () {
        sortBy = $('#sort_by option:selected').text();
    });


    function do_ajax(doreverse) {
        $.ajax({
            url: 'ajax/price_filter/',
            type: 'POST',
            data: {
                'minval': sliderMinval,
                'maxval': sliderMaxval,
                'sortby': sortBy,
                'shownumber': showNumber,
                'reverselist': doreverse

            },
            dataType: 'json',
            success: function (data) {
                if (data) {
                    console.log(data['html_from_view']);
                    $('#ajax_filter').html(data['html_from_view']);

                }
            }
        });

    }

    $('#submit_btn').on('click', function () {
        reverseList = false
        do_ajax(reverseList);
    });

    $('#sort-btn').on('click', function () {
        reverseList = !reverseList
        alert(reverseList)
        do_ajax(reverseList);
    });


})(jQuery);

"use strict";

function add_to_cart_ajax(id) {
    $.ajax({
        url: '.',
        type: 'POST',
        data: {
            'act':'add_to_cart',
            'product_id': id
        },
        dataType: 'json',
        success: function (data) {
            if (data) {
                if (data['error_msg']) {
                    console.log(data['error_msg']);
                    alert(data['error_msg']);
                }
                else
                {
                    $('.shopping-cart-list').html(data['html_from_view']);
                }

            }
        }
    });

}

function update_qty_number(do_add) {

    var qty = Number($('.qty').text());
    if (do_add == true)
        qty++;
    else {
        qty--;
        qty = Math.max(0,qty);
    }

    $('.qty').text(qty);
}

function handle_add_to_cart(id) {
    update_qty_number(true);
    add_to_cart_ajax(id);
}

var elements = document.getElementsByClassName("dummy");
var elements2 = document.getElementsByClassName("dummy2");

console.log("elements of row" + elements);
// Declare a loop variable
var i;

// List View
function listView() {
    if (elements) {

        console.log("elements of row in list view" + elements.length);
        for (i = 0; i < elements.length; i++) {
            console.log(elements[i]);
            elements[i].className = elements[i].className.replace(" grid-view", " list-view");

        }
        for (i = 0; i < elements2.length; i++) {
            //console.log(elements2[i]);
            //elements2[i].className = elements2[i].className.replace(" col-md-4", " fook");

        }
    }
}


// Grid View

function gridView() {
    if (elements) {

        console.log("elements of row in grid view" + elements);
        for (i = 0; i < elements.length; i++) {
            elements[i].className = elements[i].className.replace(" list-view", " grid-view");
        }
        for (i = 0; i < elements2.length; i++) {
            //console.log(elements2[i]);
            //elements2[i].className = elements2[i].className.replace(" fook", " col-md-4");

        }
    }
}

/* Optional: Add active class to the current button (highlight it) */
var btns = document.getElementsByClassName("view-button");

if (btns) {
    for (var i = 0; i < btns.length; i++) {
        btns[i].addEventListener("click", function () {
            var current = document.getElementsByClassName("view-active");
            console.log(current);
            current[0].className = current[0].className.replace(" view-active", "");
            this.className += " view-active";
        });
    }
}



