$('#setting').on('click', function () {
    $("#popup1").fadeIn();
});

$('#close1').on('click', function () {
    $('#popup1').fadeOut();
});

$('#help').on('click', function () {
    $("#popup2").fadeIn();
});

$('#close2').on('click', function () {
    $('#popup2').fadeOut();
});

$('#pp').on('click', function () {
    $('#popup2').fadeOut();
    $('#popup3').fadeIn();

});

$('#close3').on('click', function () {
    $('#popup3').fadeOut();
});

$('#le').on('click', function () {
    $('#popup2').fadeOut();
    $("#popup4").fadeIn()
});

$('#close4').on('click', function () {
    $('#popup4').fadeOut();
});

$('#search_text').on('click', function () {
    $("#popup5").fadeIn()
});

$('#close5').on('click', function () {
    $('#popup5').fadeOut();
});

$(function() {
    const h = $(window).height(); // ブラウザウィンドウの高さを取得する
    $('#contents').css('display','none'); // コンテンツを非表示にする
    $('#loader-bg ,#loader').height(h).css('display','block');//ローディング画像を表示
});