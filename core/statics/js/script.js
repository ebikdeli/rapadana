function display() {
  var y = document.getElementById("final");
  if (document.getElementById("control_01").checked) {
    y.style.display = "block";
  } else if (document.getElementById("control_02").checked) {
    y.style.display = "block";
  } else if (document.getElementById("control_03").checked) {
    y.style.display = "block";
  }
}

////profile
$(document).ready(function () {
  $(".main div").hide();

  $(".slidebar li:first").attr("id", "active");

  $(".main div:first").fadeIn();

  $(".slidebar a").click(function (e) {
    e.preventDefault();
    if ($(this).closest("li").attr("id") == "active") {
      return;
    } else {
      $(".main div").hide();

      $(".slidebar li").attr("id", "");

      $(this).parent().attr("id", "active");
      // active le parent du li selectionner

      $("#" + $(this).attr("name")).fadeIn();
      // Montre le texte
    }
  });
});
