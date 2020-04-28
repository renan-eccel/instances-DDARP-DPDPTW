jQuery(document).ready(function ($) {
    function isImageVault(path) {
        var regexp = new RegExp("\\/ImageVault\\/Images\\/");
        return (path.match(regexp));
    }
    function getImageVaultBigImage(path) {
        var idmatch = path.match(new RegExp("\\/id_(\\d+)\\/"));
        if (idmatch.length > 1) {
            return "/ImageVault/Images/id_" + parseInt(idmatch[1]) + "/scope_0/ImageVaultHandler.aspx";
        }
        else return path;
    }
    $('img').filter('.sintefvideo').each(function () {
        var tag = $(this);
        var regexp = new RegExp("vi/([A-Za-z0-9\\d\\-_]+)/(?:\\w*).jpg");
        var matches = regexp.exec(tag.attr('src'));
        if (matches != null && matches.length == 2 && matches[1] === tag.attr('alt')) {
            var srcUrl = 'https://www.youtube.com/embed/' + tag.attr('alt') + '?modestbranding=1&showinfo=0&iv_load_policy=3&showsearch=0&rel=0&theme=light&wmode=opaque';
            var videoTag = $('<iframe frameborder="0" allowfullscreen/>').attr('src', srcUrl).attr('width', tag.attr('width')).attr('height', tag.attr('height'));
            var newTag = $('<span></span>').css('float', tag.css('float')).css('padding', '0px 5px').html(videoTag);
            tag.replaceWith(newTag);
        }
    });

    $('img.sintefoverlay').wrap(function () {
        var linkurl = $(this).attr("src");
        if (isImageVault(linkurl)) {
            linkurl = getImageVaultBigImage(linkurl);
        }
        return '<a class="sintefoverlaylink" href="' + linkurl + '"></a>';
    });
    $('.sintefoverlaylink').fancybox({ type: 'image' });

    var imageCarouselID = 0;
    $('.carouselwrapper').each(function () {
        var wrapper = $(this);
        var carousel = $('<div class="imageCarousel"></div>');
        var images = JSON.parse($(this).attr('alt').replace(/\¤/g, '"'));
        var span = $('<span />');
        for (var i = 0; i < images.length; i++) {
            var title = images[i].alt;
            var src = images[i].src;
            var imageTag = $('<img />').attr('src', src).attr('alt', title).removeAttr("height").removeAttr("width");
            var aTag = $('<a></a>').attr('class', 'carouselImage').attr('rel', 'carouselGroup' + imageCarouselID).attr('href', src).attr('title', title).append(imageTag);
            span.append(aTag);
        }
        carousel.html(span);
        wrapper.replaceWith(carousel);

        imageCarouselID++;
    });
    $('.carouselImage').fancybox({
        type: 'image',
        prevEffect: 'none',
        nextEffect: 'none',
        helpers: {
            title: {
                type: 'inside'
            },
            thumbs: {
                width: 50,
                height: 50
            }
        }
    });
});