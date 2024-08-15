$(document).ready(function() {
    function handleAutocomplete(campo, lista, categoria) {
        campo.on('input', function() {
            var termo = $(this).val();
            if (termo.length > 0) {
                $.ajax({
                    url: '/sugestoes',
                    type: 'GET',
                    data: { termo: termo, categoria: categoria },
                    success: function(sugestoes) {
                        lista.empty();
                        sugestoes.forEach(function(sugestao) {
                            lista.append('<li>' + sugestao + '</li>');
                        });
                    }
                });
            } else {
                lista.empty();
            }
        });

        lista.on('click', 'li', function() {
            campo.val($(this).text());
            lista.empty();
        });
    }

    handleAutocomplete($('#campo_nome'), $('#lista_sugestoes_nome'), 'nome');
    handleAutocomplete($('#campo_risco'), $('#lista_sugestoes_risco'), 'risco');

    $('#autocomplete-form').on('submit', function(event) {
        event.preventDefault();

        var palavraNome = $('#campo_nome').val();
        var palavraRisco = $('#campo_risco').val();

        if (palavraNome) {
            $.ajax({
                url: '/inserir_palavra',
                type: 'POST',
                data: { palavra: palavraNome, categoria: 'nome' },
                success: function(response) {
                    alert(response);
                }
            });
            $('#campo_nome').val('');
        }

        if (palavraRisco) {
            $.ajax({
                url: '/inserir_palavra',
                type: 'POST',
                data: { palavra: palavraRisco, categoria: 'risco' },
                success: function(response) {
                    alert(response);
                }
            });
            $('#campo_risco').val('');
        }
    });
});



