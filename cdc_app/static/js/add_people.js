
$(document).ready(
  function(){
              var user_details_datatable = $("#user_details_table").DataTable({
                      "responsive": true,
                      "destroy": true,
              });
          $.ajax({
              url: "get_user_details",
              type: 'POST',
              data: {
                     
              },
              dataType: 'json',
              success: function (data) {
                      user_details_datatable.clear().draw();
                      user_details_datatable.search("").draw()
                      var fetchedData = data.profiles
                      ctr = 0
                      for (const [key, value] of Object.entries(fetchedData)) {
                              var new_value = value.concat('<button class = "edit_btn" id =edit_' + key +'_'+ctr+'><i class="fa fa-edit">Edit</i></button>'+
                              '<button class = "delete_btn" id =delete_' +  key +'_'+ctr+'><i class="fa fa-trash">Delete</i></button>');
                                user_details_datatable.row.add(new_value).draw();           

                                ctr += 1
                                if(ctr == 10){
                                        ctr = 0
                                }
                      }

              }
      });

      // function notify() {
      //         console.log('making it visible')
      //         $('#add_user_div').css('visibility', 'visible')
      // }

      // function hide(){
      //         $('#add_user_div').css('visibility', 'hidden')
      // }

      


      $("#add_people_tbody").on( "click", 'button', function() {
        
        actn = $(this).attr('id')
        actn_arr = actn.split('_')
        if (confirm('Are you sure you want to '+ (actn_arr[0]).toUpperCase() +' ?')) {
                if (actn_arr[0] == 'edit'){
                        var table_row = document.getElementById('add_people_tbody').children[actn_arr[2]].children
                        data = []
                        for (var i = 0; i < table_row.length; i++) {
                                var tableChild = table_row[i].innerHTML;
                                data.push(tableChild)
                                // Do stuff
                              }
                        window.location.href= "/edit_people/"+actn_arr[1];
                        
                       
                }
                else if (actn_arr[0] == 'delete'){

                        $.ajax({
                                url: "delete_people_row",
                                type: 'POST',
                                data: {
                                "data":actn
                                },
                                dataType: 'json',
                                success: function (data) {
                                        action = data.action
                                        if (action == 'delete'){
                                        window.location.href= "/add_people";
                                        }
                                }
                        });
                }
        }


        $('.dataTables_paginate').children()[0].innerHTML = '&laquo; Previous'
        $('.dataTables_paginate').children()[2].innerHTML = 'Next &raquo;'

        });
        $( "#add_people_button1" ).on( "click", function(){
        $('#add_people_form_div').css('visibility', 'visible')
        } );

        $( "#add_people_cross_button" ).on( "click", function(){
                $('#add_people_form_div').css('visibility', 'hidden')
        } );

});

