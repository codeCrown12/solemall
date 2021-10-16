$(document).ready(function(){

    $("#changepass").click(function(e){
      e.preventDefault()
      var currpass = $("#currpass").val()
      var currpass2 = $("#currpass2").val()
      if(currpass == "" || currpass2 == ""){
        Swal.fire(
          'Error',
          'All fields are required!',
          'error'
        )
      }
      else if(currpass != currpass2){
        Swal.fire(
          'Error',
          'Passwords do not match!',
          'error'
        )
      }
      else{
        SlickLoader.enable();
        SlickLoader.setText("Please wait...");
        $.ajax({
          type: "POST",
          data: {pass: currpass},
          url: "/updatepass"
        }).done(function(res){
          if (res == "true"){
            SlickLoader.disable()
            Swal.fire({
              title: 'Success',
              text: "A token has been sent to your email address!",
              icon: 'success',
              showCancelButton: false,
              confirmButtonColor: '#3085d6',
              confirmButtonText: 'OK'
              }).then((result) => {
              if (result.isConfirmed) {
                location.replace("/verifychangepass")
              }
            })
          }
          else{
            SlickLoader.disable()
            Swal.fire(
              'Error',
              res,
              'error'
            )
          }
        }).fail(function(e){
          console.log(e)
        })
      }
    })


    
    $("#c-email").click(function(e){
      e.preventDefault()
      var email = $("#email").val()
      if(email == ""){
        Swal.fire(
          'Error',
          'Fields is required',
          'error'
        )
      }
      else{
        SlickLoader.enable();
        SlickLoader.setText("Please wait...");
        $.ajax({
          type: "POST",
          data: {newemail: email},
          url: "/updemail"
        }).done(function(res){
          if (res == "Successful"){
            SlickLoader.disable()
            Swal.fire({
              title: 'Success',
              text: "A token has been sent to your new email address!",
              icon: 'success',
              showCancelButton: false,
              confirmButtonColor: '#3085d6',
              confirmButtonText: 'OK'
              }).then((result) => {
              if (result.isConfirmed) {
                location.replace("/changemail")
              }
            })
          }
          else{
            SlickLoader.disable()
            Swal.fire(
              'Error',
              res,
              'error'
            )
          }
          
        }).fail(function(e){
          console.log(e)
        })
      }
    })


    $("#save-billing").click(function(e){
        e.preventDefault()
        var street = $("#street").val()
        var state = $("#state").val()
        var city = $("#city").val()
        var zip = $("#zip").val()
        if (street == "" || state == "" || city == "" || zip == ""){
          Swal.fire(
            'Error',
            'All fields are required',
            'error'
          )
        }
        else{
          $.ajax({
            type: "POST",
            data: {street: street, state: state, city: city, zip: zip},
            url: "/updatebilling"
          }).done(function(res){
            if (res == "true"){
                Swal.fire({
                title: 'Success',
                text: "Billing address updated successfully!",
                icon: 'success',
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'OK'
                }).then((result) => {
                if (result.isConfirmed) {
                    location.reload()
                }
              })
            }
            else if (res == "You're not logged in") {
              Swal.fire({
                title: 'Sorry!',
                text: res,
                icon: 'warning',
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Login'
                }).then((result) => {
                if (result.isConfirmed) {
                    location.replace('/login')
                }
              })
            }
            else{
              console.log(res)
            }
          }).fail(function(e){
            console.log(e)
          })
        }
    })

    //Function to update personal information
    $("#save-details").click(function(e){
        e.preventDefault()
        var fname = $("#fname").val()
        var lname = $("#lname").val()
        var mobile = $("#mobile").val()
        if(fname == "" || lname == "" || mobile == ""){
          Swal.fire(
            'Error',
            'All fields are required',
            'error'
          )
        }
        else{
          $.ajax({
            type: "POST",
            data: {fname: fname, lname: lname, mobile: mobile},
            url: "/updateuser"
          }).done(function(res){
            if (res == "true"){
                Swal.fire({
                title: 'Success',
                text: "Personal info updated successfully",
                icon: 'success',
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'OK'
                }).then((result) => {
                if (result.isConfirmed) {
                    location.reload()
                }
              })
            }
            else if (res == "You're not logged in") {
              Swal.fire({
                title: 'Sorry!',
                text: res,
                icon: 'warning',
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Login'
                }).then((result) => {
                if (result.isConfirmed) {
                    location.replace('/login')
                }
              })
            }
            else{
              console.log(res)
            }
          }).fail(function(e){
            console.log(e)
          })
        }
    })
})