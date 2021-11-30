$( document ).on( 'click', '.list-group-item', function(event) {
   if (event.target.hasAttribute('href')) {
       var link = event.target.href + 'ajax/';
       var link_array = link.split('/');
       if (link_array[3] == 'products') {
           $.ajax({
               url: link,
               success: function (data) {
                   $('.page_content').html(data.result);
               },
           });

           event.preventDefault();
       }
   }
});