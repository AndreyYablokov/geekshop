window.onload = function () {
    $('.basket_list').on('click', 'input[type="number"]', function () {
        var t_href = event.target;

        $.ajax({
            url: '/baskets/edit/' + t_href.name + '/' + t_href.value + '/',
            success: function (data) {
                $('.basket_list').html(data.result)
            },
        });
    });

    $('.card-footer').on('click', function () {
        var t_href = event.target;

        if (t_href.classList.contains('btn-outline-success')) {
            $.ajax({
                url: '/baskets/add/' + t_href.name + '/',
                success: function () {
                    t_href.classList.remove('btn-outline-success');
                    t_href.classList.add('btn-outline-danger');
                    t_href.innerHTML = 'Удалить из корзины'
                },
            });
        } else {
            $.ajax({
                url: '/baskets/remove_ajax/' + t_href.name + '/',
                success: function () {
                    t_href.classList.remove('btn-outline-danger');
                    t_href.classList.add('btn-outline-success');
                    t_href.innerHTML = 'Добавить в корзину'
                },
            });
        }
    });
}