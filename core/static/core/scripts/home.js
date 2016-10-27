function Slider(container) {
    this.container = container
}

Slider.prototype.init = function () {
    this.container.unslider({
        infinite: true,
        nav: false
    })
}

var jumpToArticle = function (num) {
    switch (num) {
        case 1:
            window.location.href = '/museum/part/guide/8'
            break
        case 2:
            window.location.href = '/museum//part/guide/9'
            break
        case 3:
            window.location.href = '/museum/part/guide/10'
            break
    }
}

$(document).ready(function () {
    var page = 0
    // var slider = new Slider($('#slider'))
    // var newsSlider = new Slider($('#news-slider'))
    $('a').smoothScroll({
        easing: 'swing',
        speed: 400,
        offset: -190
    });
    $('.bxslider').bxSlider({
        adaptiveHeight: true,
        mode: 'fade',
        captions: true
    });
    // slider.init()
    // newsSlider.init()
    $('#load-more').click(function () {
        $.ajax({
            url: '/museum/' + page,
            success: function (res) {
                res.map(function (news) {
                    var url = '/museum/static/media/' + news.fields.thumbnail.substr(2)
                    $('#news_content').append(
                        '<li>' +
                            '<a style="color: #333; text-decoration: blink" href="/museum/part/exhibition/' + news.pk + '">' +
                                '<div class="image">' +
                                    '<img src="' + url + '" alt=""/>' +
                                '</div>' +
                                '<div class="info">' +
                                    '<h4>' + news.fields.title + '</h4>' +
                                '</div>'+
                            '</a>' +
                        '</li>'
                    )
                });
                ++page
            }
        })
    })
});