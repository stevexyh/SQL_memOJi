$(document).ready(function () {
    $(".datatable").DataTable({
        columns: [
            { orderable: false },
            { orderable: true},
            { orderable: true},
            { orderable: false },
            { orderable: true},
            { orderable: true},
            { orderable: true},
            { orderable: false },
        ],
        order: [[1, "asc"]],
        language: {
            paginate: {
                previous: "<i class='mdi mdi-chevron-left'>",
                next: "<i class='mdi mdi-chevron-right'>",
            },
        },
        drawCallback: function () {
            $(".dataTables_paginate > .pagination").addClass(
                "pagination-rounded"
            );
        },
    });
});
