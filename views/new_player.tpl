<!DOCTYPE html>
<html lang="en">
<head>
    % include('_header.tpl', title='New Player')
</head>
<body>
<div class="container text-center">

    % include('_navbar.tpl')

  <div class="col-md-12">
    REGISTRATION HAS BEEN CLOSED
    <hr/>
  </div>

  <div class="col-md-12">
    <h1> REGISTER NEW PLAYER </h1>
    <p> Add yourself to the site by typing in your CFN fighter id: </p>
    <input id="new_player_name" size="50" placeholder="example: Fchampryan"/>
    <br/>
    <br/>
    <button type="button" class="btn dark"id="submit_new_player">
        SUBMIT
    </button>
    <br/>
    <br/>
    <p id="message"></p>
  </div>
% include('_copyright.tpl')
</div>

<script type="text/javascript">
$(document).ready(function () {
    function player_link(player_name){
        return (
            '<h4><a href="/player/' + player_name +
            '">' + player_name + '</a></h4>'
        );
    }

    function new_message(player_name){
        return (
            "You have been successfully added! You can view your details here:" +
            player_link(player_name) +
            "It can take up to a couple of hours before the latest data is pulled and you show up in the dropdown.<br/>Please be patient and check in periodically.<br/>After that, your information will be updated around once per day."
        )
    }

    function old_message(player_name){
        return (
            "You already exist in the system! You can view your details here:" +
            player_link(player_name)
        )
    }

    function submit_new_player(){
        var new_player_name = $('#new_player_name').val();
        if (new_player_name.length == 0){
            return;
        }
        $('#message').html("Checking, this could take a minute...");
        $('#new_player_name').prop("disabled", true);
        $('#submit_new_player').prop("disabled", true);
        $.ajax({
            url: 'http://{{ api_host }}/sfv/new_player/' + new_player_name,
            type: 'POST',
            contentType: "charset=utf-8",
        }).done(function (data){
            var message = null;
            if (data.is_match && data.is_new) {
                message = new_message(data.player_name);
            }
            if (data.is_match && !data.is_new) {
                message = old_message(data.player_name);
            }
            if (!data.is_match) {
                message = "Player not found. Double check the spelling and try again?";
            }
            if (data.is_error) {
                message = "There was a problem connecting to CFN. Please try again in a couple minutes."
            }
            $('#message').html(message);
            $('#new_player_name').prop("disabled", false);
            $('#submit_new_player').prop("disabled", false);
        }).fail(function (){
            $('#message').html('There was an error. Please check <a href="http://status.fightinggame.community/">status.fightinggame.community</a> for more details.');
        });
    }
    $('#new_player_name').keypress(function (evt) {
        if (evt.which == 13) {
            submit_new_player();
            return false;
        }
    });
    $('#submit_new_player').on("click", function(evt){
        evt.preventDefault();
        submit_new_player();
    });

    // #SHUTDOWN disable buttons
    $('#new_player_name').prop("disabled", true);
    $('#submit_new_player').prop("disabled", true);
});
</script>
</body>
</html>
