//JS para o menu dropdown de cadastrar usuário:

$(document).ready(function(){
    changeErrMsgParent();
    $("#cadastro-usuario").click(function(){
        $("#hidden-register").slideToggle(200);
    });
});

function changeErrMsgParent() {
    var errMsg = $('.error-msg').detach();
    errMsg.removeClass('hidden');
    var sucMsg = $('.success-msg').detach();
    sucMsg.removeClass('hidden');
    $('.page-title').append(errMsg);
    $('.page-title').append(sucMsg);
}
