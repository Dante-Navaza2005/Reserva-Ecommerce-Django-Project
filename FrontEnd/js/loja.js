// Script de ordenar
function redirectToPage() {
    var selectElement = document.getElementsByClassName('produtos__select')[0];
    var selectedOption = selectElement.options[selectElement.selectedIndex].value;
    if (selectedOption) {
      window.location.href = selectedOption;
    }
  }

// Scripts do Menu Lateral

var checkboxes = document.querySelectorAll('.menu__tamanho .menu__checkbox');

checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        var adjacentDivs = document.querySelectorAll('.menu__tamanho .menu__tamanho-quadrado');
        
        adjacentDivs.forEach(function(div) {
            div.style.color = ''; // Reset all adjacent div colors
            div.style.borderColor = ''; // Reset all adjacent div colors
        });

        var adjacentDiv = this.previousElementSibling; // Get the previous sibling (the div)
        if (this.checked) {
            adjacentDiv.style.color = '#6495ED'; // Set the color of the currently selected one
            adjacentDiv.style.borderColor = '#6495ED'; // Set the color of the currently selected one
        }
    });
});

var checkboxes = document.querySelectorAll('.menu__categoria .menu__checkbox');

checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        var adjacentDivs = document.querySelectorAll('.menu__categoria .menu__categoria-quadrado');
        
        adjacentDivs.forEach(function(div) {
            div.style.color = ''; // Reset all adjacent div colors
            div.style.backgroundColor = ''; // Reset all adjacent div colors
        });

        var adjacentDiv = this.previousElementSibling.previousElementSibling; // Get the previous sibling (the div)
        if (this.checked) {
            adjacentDiv.style.color = '#6495ED'; // Set the color of the currently selected one
            adjacentDiv.style.backgroundColor = '#6495ED'; // Set the color of the currently selected one
        }
    });
});

var checkboxes = document.querySelectorAll('.menu__tamanho .menu__checkbox');

checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        var adjacentDivs = document.querySelectorAll('.menu__tamanho .menu__tamanho-quadrado');
        
        adjacentDivs.forEach(function(div) {
            div.style.color = ''; // Reset all adjacent div colors
            div.style.borderColor = ''; // Reset all adjacent div colors
        });

        var adjacentDiv = this.previousElementSibling; // Get the previous sibling (the div)
        if (this.checked) {
            adjacentDiv.style.color = '#6495ED'; // Set the color of the currently selected one
            adjacentDiv.style.borderColor = '#6495ED'; // Set the color of the currently selected one
        }
    });
});

var checkboxes = document.querySelectorAll('.menu__categoria .menu__checkbox');

checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        var adjacentDivs = document.querySelectorAll('.menu__categoria .menu__categoria-quadrado');
        
        adjacentDivs.forEach(function(div) {
            div.style.color = ''; // Reset all adjacent div colors
            div.style.backgroundColor = ''; // Reset all adjacent div colors
        });

        var adjacentDiv = this.previousElementSibling.previousElementSibling; // Get the previous sibling (the div)
        if (this.checked) {
            adjacentDiv.style.color = '#6495ED'; // Set the color of the currently selected one
            adjacentDiv.style.backgroundColor = '#6495ED'; // Set the color of the currently selected one
        }
    });
});

var elemsMenuCabecalho = document.querySelectorAll(
  ".menu__expansivel-cabecalho"
);

elemsMenuCabecalho.forEach(function (ele) {
  ele.addEventListener("click", function () {
    ele.parentElement.classList.toggle("menu__expansivel--aberto");
  });
});

// Script para abrir e fechar a tela de filtro
var elemFecharFiltro = document.querySelector(".menu__fechar-filtro");
var elemAbrirFiltro = document.querySelector(".produtos__cabecalho-filtrar");

elemFecharFiltro.addEventListener("click", function () {
  document.body.classList.remove("filtro-aberto");
});

elemAbrirFiltro.addEventListener("click", function () {
  document.body.classList.add("filtro-aberto");
});
