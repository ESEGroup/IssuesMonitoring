//JS para o menu dropdown de cadastrar usuário:

$(document).ready(function(){
    $("#cadastro-usuario").click(function(){
        $("#hidden-register").slideToggle(200);
    });
});

function changeErrMsgParent() {
    var errMsg = $('.error-msg').detach();
    var sucMsg = $('.success-msg').detach();
    $('.page-title').append(errMsg);
    $('.page-title').append(sucMsg);
}
window.onload = changeErrMsgParent;
