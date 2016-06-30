<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="/static/css/select2.css">

    % include('_header.tpl', title='Find Player')

    <script src="/static/js/select2.js"> </script>
</head>
<body>
<div class="container text-center">

    % include('_navbar.tpl')

    <div class="col-md-12">
      <h1>FIND PLAYER</h1>
      <p>
        Look up players by typing in their Fighter ID
      </p>
      <p id="message">
        loading list of players, please wait...
      </p>
      <div class="col-md-4"></div>
      <div class="col-md-4">
        <select id="lookup-select" hidden>
          <option></option>
          % for name in player_names:
            <option value="{{name}}">{{name}}</option>
          % end
        </select>
      </div>
      <div class="col-md-4"></div>
      <div class="col-md-12">
        <br/>
        <a href="/new_player">
        <button type="button" class="btn dark">
          Don't see yourself listed?
        </button>
        </a>
      </div>
  </div>

    % include('_copyright.tpl')
</div>

<script type="text/javascript">
    $(document).ready(function () {
      $('#lookup-select').select2({
          minimumInputLength: 3,
          placeholder: "example: TS-Sabin",
          width: '80%',
      }).change(function (){
          var val = $(this).val();
          window.location.href = '/player/' + val;
      });
      $('#message').html("Click below and start typing:");
      $('#s2id_lookup-select').show();
    });
</script>
</body>
</html>
