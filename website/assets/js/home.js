$(document).ready(function () {
  $(".hover-title-info").hover(function () {
    var item = $(this).data("item");
    $(".item-1").addClass("hidden");
    $(".item-2").addClass("hidden");
    $(".item-3").addClass("hidden");
    $(".item-4").addClass("hidden");
    $(".item-5").addClass("hidden");
    $(".item-6").addClass("hidden");
    $("." + item).removeClass("hidden");
  });
});
