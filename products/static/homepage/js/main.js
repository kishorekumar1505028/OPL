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

function update_qty_number(new_val) {
    var prev = parseInt($('#cart_qty').text());
    prev = prev + parseInt(new_val);
    alert(prev);
    $('#cart_qty').text(prev);
}

function isInt(value) {
    return !isNaN(value) && (function (x) {
        return (x | 0) === x;
    })(parseFloat(value))
}

function select_shipping() {
    var types = document.getElementsByName('shipping');
    var type_value = 0;
    var type_id = "";
    for (var i = 0; i < types.length; i++) {
        if (types[i].checked) {
            type_value = types[i].value;
            type_title = types[i].title;
        }
    }
    alert(type_value);
    document.getElementById('shipping_field').innerText = type_title + " \u09F3 " + type_value;
    var tval = document.getElementById('subtotal_price').innerText;
    tval = parseFloat(tval.slice(2, tval.length));
    if (type_value == 40)
        tval += 40;
    alert(tval);
    document.getElementById('total_price').innerText = '\u09F3 ' + tval;
}

function add_to_cart_ajax(id, a, add_or_delete) {
    $.ajax({
        url: '.',
        type: 'POST',
        data: {
            'act': 'add_to_cart',
            'product_id': id,
            'numbers': a,
            'add_or_delete': add_or_delete
        },
        dataType: 'json',
        success: function (data) {
            if (data) {

                if (data['error_msg']) {
                    console.log(data['error_msg']);
                    alert(data['error_msg']);
                } else {
                    alert(data['success_msg']);

                    $('.shopping-cart-list').html(data['html_from_view']);

                    if (data['cart_info_html']) {
                        alert("changing cart info");
                        $('#cart_info').html(data['cart_info_html']);
                    }

                    if (data['wishlist_info_html']) {
                        alert("changing wishlist info");
                        $('#wishlist_info').html(data['wishlist_info_html']);
                    }

                    if (data['checkout_info_html'])
                        $('#checkout_info').html(data['checkout_info_html']);

                    if (data['checkout_total_html']) {
                        $('#checkout_total').html(data['checkout_total_html']);
                        select_shipping();
                    }

                    if (data['cart_total_html']) {
                        $('#cart_total').html(data['cart_total_html']);
                    }
                    document.getElementById("cart_qty").innerText = data['html_cart_size'];
                    alert('cart size');
                    alert(data['html_cart_size']);


                }

            }
        }
    });

}

function add_to_wishlist_ajax(id, add_or_delete) {
    $.ajax({
        url: '.',
        type: 'POST',
        data: {
            'act': 'add_to_wishlist',
            'product_id': id,
            'numbers': 1,
            'add_or_delete': add_or_delete
        },
        dataType: 'json',
        success: function (data) {
            if (data) {
                if (data['error_msg']) {
                    console.log(data['error_msg']);
                    alert(data['error_msg']);
                } else {
                    alert('Product is added to or removed from wishlist');
                    if (data['wishlist_info_html']) {
                        alert("changing wishlist info");
                        $('#wishlist_info').html(data['wishlist_info_html']);
                    }
                }

            }
        }
    });

}

function reload_reviews(id) {
    $.ajax({
        url: '.',
        type: 'POST',
        data: {
            'act': 'reload_review',
            'id': id
        },
        dataType: 'json',
        success: function (data) {
            if (data) {
                if (data['error_msg']) {
                    console.log(data['error_msg']);
                    alert(data['error_msg']);
                } else {
                    alert('Review published');
                    $('.product-reviews').html(data['html_from_view']);
                    $('#review_len').html(data['html2_from_view']);


                }

            }
        }
    });
}

function write_review_ajax(rating, review_content, id) {
    alert("writing review ajax");
    $.ajax({
        url: '.',
        type: 'POST',
        data: {
            'act': 'write_review',
            'rating': rating,
            'id': id,
            'review': review_content
        },
        dataType: 'json',
        success: function (data) {
            if (data) {
                if (data['error_msg']) {
                    console.log(data['error_msg']);
                    alert(data['error_msg']);
                } else {
                    alert('Review published');
                    reload_reviews(id);

                }

            }
        }
    });

}


function handle_add_to_cart(id) {
    alert("js func handle add to cart called")
    add_to_cart_ajax(id, 1, 1);
}

function handle_add_to_wishlist(id, add_or_delete) {

    alert("calling wishlist");
    add_to_wishlist_ajax(id, add_or_delete);
}

function remove_cart_from_wishlist(id) {

    alert("calling remove cart from wishlist");
    add_to_cart_ajax(id, 1, 1);
    add_to_wishlist_ajax(id, 0);
}

function calc_rating(id) {
    var rates = document.getElementsByName('rating');
    var rate_value = 0;
    for (var i = 0; i < rates.length; i++) {
        if (rates[i].checked) {
            rate_value = rates[i].value;
        }
    }
    var review_content = document.getElementById('review_content').value;
    alert(review_content);
    write_review_ajax(parseInt(rate_value), review_content, id)
}


function place_order(id) {
    $.ajax({
        url: '.',
        type: 'POST',
        data: {
            'act': 'place_order',
            'id': id,
        },
        dataType: 'json',
        success: function (data) {
            if (data) {
                if (data['error_msg']) {
                    console.log(data['error_msg']);
                    alert(data['error_msg']);
                } else {
                    alert('Your order has been placed , Thanks for shopping from us!!!');

                }
                if (data['html_from_view'])
                    $('#checkout_info').html(data['html_from_view']);
                document.getElementById("cart_qty").innerText = data['html_cart_size'];
            }
        }
    });
}

function handle_add_to_cart_product_details(id) {
    var a = document.getElementById('dqty').value;
    if (isInt(a) == false)
        alert("Fill up the quantity as integer");
    else {
        a = parseInt(a);
        if (a == 0)
            alert("Insert a nonzero value");
        else if (a < 0)
            alert("Insert a positive value");
        else {
            alert(a);
            add_to_cart_ajax(id, a, 1);
        }

    }


}

function remove_from_cart(id) {
    alert("weird");
    add_to_cart_ajax(id, 0, 0);
}


function change_quantity(id, c) {
    alert(c);
    var a = document.getElementsByClassName("p_qty")[c - 1].value;

    alert(a);
    add_to_cart_ajax(id, a, 1);

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

function show_save_button() {
    document.getElementById("save_btn").style.display = 'block';
}

function hide_save_button() {
    document.getElementById("save_btn").style.display = 'none';
}

function change_storage(id,change_or_remove,quantity,price) {
    $.ajax({
        url: '.',
        type: 'POST',
        data: {
            'act': 'change',
            'quantity': quantity,
            'price': price,
            'id': id,
            'change_or_remove': change_or_remove,
        },
        dataType: 'json',
        success: function (data) {
            if (data) {
                if (data['error_msg']) {
                    console.log(data['error_msg']);
                    alert(data['error_msg']);
                }
                if (data['vendor_storage'])
                    $('#storage_info').html(data['vendor_storage']);

            }
        }

    });
}

function remove_from_storage(id) {
    change_storage(id,0 ,0 , 0);
}
function update_product(id , c) {
    var quantity = document.getElementsByClassName("storage_qty")[c - 1].value;
    var price = document.getElementsByClassName("storage_price")[c - 1].value;
    change_storage(id,1, quantity, price);
    hide_save_button();
}