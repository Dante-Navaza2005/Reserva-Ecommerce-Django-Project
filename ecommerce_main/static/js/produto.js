// Script para o Carrossel da Página de Produto
var checkboxes = document.querySelectorAll('.menu__tamanho .menu__checkbox');

checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        var adjacentDivs = document.querySelectorAll('.menu__tamanho .s-produto__tamanhos-item');
        
        adjacentDivs.forEach(function(div) {
            div.style.color = ''; // Reset all adjacent div colors
            div.style.backgroundColor = ''; // Reset all adjacent div colors
        });

        var adjacentDiv = this.previousElementSibling; // Get the previous sibling (the div)
        if (this.checked) {
            adjacentDiv.style.color = 'white'; // Set the color of the currently selected one
            adjacentDiv.style.backgroundColor = 'black'; // Set the color of the currently selected one
        }
    });
});

var elemsCarrosselBotao = document.querySelectorAll(
  ".s-produto__carrossel-botao"
);
var elemCarrosselImagens = document.querySelector(
  ".s-produto__carrossel-itens"
);

elemsCarrosselBotao.forEach(function (elem, i) {
  elem.addEventListener("click", function () {
    elemCarrosselImagens.style = "transform: translateX(-" + i * 100 + "%)";

    elemsCarrosselBotao.forEach(function (ele) {
      if (ele != elem) {
        ele.classList.remove("s-produto__carrossel-botao--selecionado");
      } else {
        ele.classList.add("s-produto__carrossel-botao--selecionado");
      }
    });
  });
});
