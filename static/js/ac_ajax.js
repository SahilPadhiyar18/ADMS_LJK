

function acToggle(data, field) {
    console.log(JSON.stringify({'ac_uuid':data.value,'field':field ,'status': data.checked}))
    $.ajax({
        url: "/ac_status_change",
        type: "GET",
        dataType: "json",
        data: {'ac_uuid':data.value,'field':field ,'status': data.checked},
        success: (data) => {
          console.log(data);
          location.reload();
        },
        error: (error) => {
          console.log(error);
        }
      });
}