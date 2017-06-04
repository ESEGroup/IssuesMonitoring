$(function(){
    $(".aprovar").each(function() {
        $(this).change(function(){
            $.ajax({
                url: this.getAttribute("data-url"),
                method: "POST",
                data: {"aprovar": this.checked}
            });
        });
    });
});
