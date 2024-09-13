var elemBotaoEntrega = document.querySelector(".checkout__botao--entrega");
var elemCheckoutEndereco = document.querySelector(".checkout__endereco");

elemBotaoEntrega.addEventListener("click", function () {
  elemCheckoutEndereco.classList.toggle("checkout__endereco--visivel");
});
