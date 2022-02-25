
$(document).ready(
    function(){
                var final_report_datatable = $("#final_report_table").DataTable({
                        "dom": "Bfrtip",
                        "responsive": true,
                        "destroy": true,
                        "createdRow": function( row, data) {
                                if (true ) {        
                                        $(row).css('color','black');
                                }
                       },
                       "buttons":[
                        {
                            extend: 'copyHtml5',
                            text:      '<i class="fa fa-files-o"> Copy</i>',
                        //     exportOptions: {
                        //         columns: [ 0, 1, 2, 3, 4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
                        //     },
                        },
                        {
                            extend: 'excelHtml5',
                            text:      '<i class="fa fa-download"> Download</i>',
                        //     exportOptions: {
                        //         columns: [ 0, 1, 2, 3, 4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
                        //     },
                            title: 'CDC Database'


                        },
                        
                       
                    ]
                        
                });
            $.ajax({
                url: "get_final_report",
                type: 'POST',
                data: {
                       
                },
                dataType: 'json',
                success: function (data) {
                        
                        console.log(data)
                        final_report_datatable.clear().draw();
                        final_report_datatable.search("").draw()
                        var fetchedData = data.clients
                        
                        for (const [key, value] of Object.entries(fetchedData)) {
                                final_report_datatable.row.add(value).draw();    

                                                    
                        }
                        // var rows = document.getElementById('company_details_tbody').children
                        // for (const r in rows){
                        //         console.log(rows[r].children)
                        //         if(rows[r].children[17].innerHTML == 'true'){
                        //                 rows[r].style.color = 'green'
                        //         }
                        //         else{
                        //                 rows[r].style.color = 'red'

                        //         }

                        // }


                        $('.dataTables_paginate').children()[0].innerHTML = '&laquo; Previous'
                        $('.dataTables_paginate').children()[2].innerHTML = 'Next &raquo;'
                }
                
        });

        $("#final_report_tbody").on( "click", 'button', function() {
                actn = $(this).attr('id')
                actn_arr = actn.split('_')
                if (confirm('Are you sure you want to '+ (actn_arr[0]).toUpperCase() +' ?')) {
                        if (actn_arr[0] == 'edit'){
                                var table_row = document.getElementById('final_report_tbody').children[actn_arr[2]].children
                                data = []
                                for (var i = 0; i < table_row.length; i++) {
                                        var tableChild = table_row[i].innerHTML;
                                        data.push(tableChild)
                                        // Do stuff
                                      }
                                window.location.href= "/edit_final_report/"+actn_arr[1];
                               
                        }
                        else if(actn_arr[0]=='approve'){
                                $.ajax({
                                        url: "approve_final_report_row",
                                        type: 'POST',
                                        data: {
                                        "data":actn
                                        },
                                        dataType: 'json',
                                        success: function (data) {
                                                action = data.status
                                                // if (action == 'edit'){}
                                                $("#final_report_a")[0].click();
                                        }
                                });

                        }
                        else if (actn_arr[0] == 'delete'){

                                $.ajax({
                                        url: "delete_final_report_row",
                                        type: 'POST',
                                        data: {
                                        "data":actn
                                        },
                                        dataType: 'json',
                                        success: function (data) {
                                                action = data.action
                                                // if (action == 'edit'){}
                                                $("#final_report_a")[0].click();
                                        }
                                });
                        }
                }


                $('.dataTables_paginate').children()[0].innerHTML = '&laquo; Previous'
                $('.dataTables_paginate').children()[2].innerHTML = 'Next &raquo;'

              });


                $( "#add_client_button1" ).on( "click", function(){
                        $('#add_client_form_div').css('visibility', 'visible')
                } );

                $( "#add_client_cross_button" ).on( "click", function(){
                        $('#add_client_form_div').css('visibility', 'hidden')
                } );


                $('.dataTables_paginate').children()[0].innerHTML = '&laquo; Previous'
                $('.dataTables_paginate').children()[2].innerHTML = 'Next &raquo;'

});
