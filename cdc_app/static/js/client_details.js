
$(document).ready(
    function(){
                var client_details_datatable = $("#client_details_table").DataTable({
                        "dom": "Bfrtip",
                        "responsive": true,
                        "destroy": true,
                        "createdRow": function( row, data) {
                                if ( data[19] == true ) {        
                                        $(row).css('color','green');
                                }
                                else{
                                        $(row).css('color','red');

                                }
                         
                   
                       },
                       "buttons":[
                        {
                            extend: 'copyHtml5',
                            text:      '<i class="fa fa-files-o"> Copy</i>',
                            exportOptions: {
                                columns: [ 0, 1, 2, 3, 4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
                            },
                        },
                        {
                            extend: 'excelHtml5',
                            text:      '<i class="fa fa-download"> Download</i>',
                            exportOptions: {
                                columns: [ 0, 1, 2, 3, 4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
                            },
                            title: 'Clients Database'


                        },
                        
                       
                    ]
                        
                });
            $.ajax({
                url: "get_client_details",
                type: 'POST',
                data: {
                       
                },
                dataType: 'json',
                success: function (data) {
                        
                        console.log(data)
                        client_details_datatable.clear().draw();
                        client_details_datatable.search("").draw()
                        var fetchedData = data.clients
                        var ctr = 0
                        for (const [key, value] of Object.entries(fetchedData)) {
                                
                                var new_value = value.concat('<button class = "edit_btn" id =edit_' + key +'_'+ctr+'><i class="fa fa-edit">Edit</i></button>'+
                                                                '<button class = "delete_btn" id =delete_' +  key +'_'+ctr+'><i class="fa fa-trash">Delete</i></button>');
                                if(data.role == 'SuperAdmin'){
                                        if(value[19]==true){
                                                var new_value2 = new_value.concat('Approved');

                                        }
                                        else{
                                                var new_value2 = new_value.concat('<button class = "approve_btn" id =approve_' + key +'><i class="fa fa-check">Approve</i></button>');
                                        }
                                        client_details_datatable.row.add(new_value2).draw();  
 

                                }
                                else{
                                        client_details_datatable.row.add(new_value).draw();    

                                }
                                ctr += 1
                                if(ctr == 10){
                                        ctr = 0
                                }
                                                    
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

        $("#client_details_tbody").on( "click", 'button', function() {
                actn = $(this).attr('id')
                actn_arr = actn.split('_')
                if (confirm('Are you sure you want to '+ (actn_arr[0]).toUpperCase() +' ?')) {
                        if (actn_arr[0] == 'edit'){
                                var table_row = document.getElementById('client_details_tbody').children[actn_arr[2]].children
                                data = []
                                for (var i = 0; i < table_row.length; i++) {
                                        var tableChild = table_row[i].innerHTML;
                                        data.push(tableChild)
                                        // Do stuff
                                      }
                                window.location.href= "/edit_client_details/"+actn_arr[1];
                               
                        }
                        else if(actn_arr[0]=='approve'){
                                $.ajax({
                                        url: "approve_client_details_row",
                                        type: 'POST',
                                        data: {
                                        "data":actn
                                        },
                                        dataType: 'json',
                                        success: function (data) {
                                                action = data.status
                                                // if (action == 'edit'){}
                                                $("#client_details_a")[0].click();
                                        }
                                });

                        }
                        else if (actn_arr[0] == 'delete'){

                                $.ajax({
                                        url: "delete_client_details_row",
                                        type: 'POST',
                                        data: {
                                        "data":actn
                                        },
                                        dataType: 'json',
                                        success: function (data) {
                                                action = data.action
                                                // if (action == 'edit'){}
                                                $("#client_details_a")[0].click();
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
