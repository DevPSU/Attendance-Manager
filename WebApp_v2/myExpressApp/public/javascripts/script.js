function populateTable(courseID){
    $(".button-purple").each(function(index){
        $(this).css('background-color', '#FFD000');
    });

    //Make Table secion visisble
    var x = document.getElementById("tableData");
    if (x.style.display === "block") {
      x.style.display = "none";
    } else {
      x.style.display = "block";
    }
}

function toggleLogIn() {
    var x = document.getElementById("signinstuff");
    if (x.style.display === "block") {
      x.style.display = "none";
    } else {
      x.style.display = "block";
    }
}