$(document).ready(function() {
    // Setup - add a text input to each footer cell
    $('#example tfoot th').each(function () {
        //var title = $(this).text();
        $(this).html('<input type="text" placeholder="Search" />');
    });

    var filesTable = $('#example').DataTable({
        fixedHeader: true,
        "lengthMenu": [[10, 20, 50, 100, -1], [10, 20, 50, 100, "All"]],
        "pageLength": 50,
        dom: 'Bfrtip',
        "order": [[0, "asc"]],
        buttons: ['pageLength', 'csv', 'excel', 'pdf', 'print']
    });
    var r = $('#example tfoot tr');
    r.find('th').each(function () {
        $(this).css('padding', '3px');
    });
    $('#example thead').append(r);
    // Apply the filter
    // https://www.jqueryscript.net/demo/DataTables-Jquery-Table-Plugin/examples/api/multi_filter.html
    $("#example thead input").on('keyup change', function () {
        filesTable
            .column($(this).parent().index() + ':visible')
            .search(this.value)
            .draw();
    });
});