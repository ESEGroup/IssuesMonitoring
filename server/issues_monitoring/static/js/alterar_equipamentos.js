$(function() {
    var alt = document.getElementsByClassName("alter-btn")
    console.log(alt.length);
    for(var i = 0; i<alt.length; ++i){
        alt[i].addEventListener("click", function(ev){
            var mac = ev.target.getAttribute("data-mac"),
                url = ev.target.getAttribute("data-url");
            ajax_get(url);

        });
    }
});
