
/*=============================================================
    Authour URI: www.binarytheme.com
    License: Commons Attribution 3.0

    http://creativecommons.org/licenses/by/3.0/

    100% To use For Personal And Commercial Use.
    IN EXCHANGE JUST GIVE US CREDITS AND TELL YOUR FRIENDS ABOUT US

    ========================================================  */

//var alertList = document.querySelectorAll('.alert')
//alertList.forEach(function (alert) {
// new bootstrap.Alert(alert)
//})

(function ($) {
    "use strict";
$(document).ready($(function () {
    //---------------------Validation---------------

        $("#learn-id-err").hide();
        $("#payment_for_submit").hide();


        $("#em-err").hide();
        $("#usn-err").hide();
        $("#usnl-err").hide();
        $("#ps-1-err").hide();
        $("#ps-2-err").hide();

        var err_un = false;
        var err_em = false;
        var err_p1 = false;
        var err_p2 = false;
        var err_r_e = false;



        $('#learner_id').focusout(function(){
            check_learner_id();
        });
        $('#username').focusout(function(){
            console.log("focus out")
            check_username();
        });
        $('#id_username').focusout(function(){
            console.log("focus out")
            check_username_login();
        });

        $('#email').focusout(function(){
            check_email();
        });
//
        $('#password1').focusout(function(){
            check_password1();
        });

        $('#password2').focusout(function(){
            check_password2();
        });

        $('#re-email').focusout(function(){
            check_r_email();
        });


        function check_learner_id(){
                var learner_id = $("#learner_id").val()
                $.ajax({
                        url: 'validate-learner-id',
                        data: {
                            'learner_id' : learner_id,
                        },
                        datatype : 'json',
                        success: function(data){
                            if (data.paid){
                                $("#learn-id-err").text(learner_id+" has already paid, Thanks");
                                $("#learn-id-err").show();
                                err_un = true;

                            }else if(data.non_learner){
                                 $("#learn-id-err").text(learner_id+" is an invalid ID");
                                    $("#learn-id-err").show();
                                    err_un = true;
                            }
                            else{
                                    $("#learn-id-err").hide();
                                    $("#payment_for_submit").show();
                                }
                        }
                        })
            }

        function check_username(){
            var username_length = $("#username").val().length;

            var username = $("#username").val()


            $.ajax({
            url: 'validate-username',
            data: {
                'username' : username,
            },
            datatype : 'json',
            success: function(data){
                if (data.is_taken){
                    $("#usn-err").text("username already taken");
                    $("#usn-err").show();
                    err_un = true;

                }else if(username_length<2){
                    console.log(username_length)
                        $("#usn-err").text("username is too short, should be more than 2 character long");
                        $("#usn-err").show();
                        err_un = true;
                    }else{
                        $("#usn-err").hide();
                    }
            }
            })

        }

        function check_username_login(){
            var username = $("#id_username").val()

            $.ajax({
            url: 'validate-username',
            data: {
                'username' : username,
            },
            datatype : 'json',
            success: function(data){
                if (data.is_taken){
                    $("#usn-err").hide();
                }else {
                    $("#usn-err").text("username doesnt exist");
                    $("#usn-err").show();
                    }
            }
            })

        }
        function check_password1() {
            var password_length = $("#password1").val().length;

            if(password_length < 8){
                $("#ps-1-err").text("Password must be at least 8 characters");
                $("#ps-1-err").show();
                err_p1 = true;
            }else{
                $("#ps-1-err").hide();
            }
        }

        function check_password2() {
            var password1 = $("#password1").val();
            var password2 = $("#password2").val();

            if(password1 != password2){
                $("#ps-2-err").text("Passwords don't match");
                $("#ps-2-err").show();
                err_p2 = true;
            }else{
                $("#ps-2-err").hide();
            }
        }

        function check_email() {
            var pattern= new RegExp(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-z]{2,4}$/i);
            var email = $("#email").val()

            $.ajax({
            url: 'validate-email',
            data: {
                'email' : email,
            },
            datatype : 'json',
            success: function(data){
                if (data.is_taken){
                    if(pattern.test($("#email").val())){
                        $("#em-err").text("user with this email already exists");
                        $("#em-err").show();
                        err_em = true;
                    }else{
                        $("#em-err").hide();
                    }
                } else if(pattern.test($("#email").val())){
                        $("#em-err").hide();
                    }else{
                        $("#em-err").text("Invalid email address");
                        $("#em-err").show();
                        err_em = true;
                    }
            }
            })




        }

        $("#learner-form").submit(function() {
            err_em = false;

            check_email();

            if(err_em==false){
                return true;
            }else {
                return false;
            }
        });
        function check_r_email() {
            var email = $("#re-email").val()

            $.ajax({
            url: 'validate-reset-email',
            data: {
                'email' : email,
            },
            datatype : 'json',
            success: function(data){
                if (data.exists){
                    $("#em-err").hide();
                    enableBtn()
                } else {
                    $("#em-err").text("Email not registered");
                    $("#em-err").show();
                    disableBtn()
                    err_r_e = true;
                    }
            }
            })
        }
        $("#r-email").submit(function() {
            err_r_e = false;

            check_r_email();

            if(err_r_e==false ){
                return true;
            }else {
                return false;
            }
        });
    }));
}(jQuery));