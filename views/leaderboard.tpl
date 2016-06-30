<!DOCTYPE html>
<html lang="en">
<head>
    % include('_header.tpl', title='Leaderboard')
</head>
<body>
<div class="container text-center">

    % include('_navbar.tpl')

  <div class="col-md-12">
    <h1 class=""> LEADERBOARD </h1>
    <p> View the top 500 Street Fighter V players according to the CFN leaderboards. </p>
    <p> Click on any player's name to see their individual stats. </p>
    <hr/>

    <table class="table" id="leaderboard">
      <thead>
        <tr>
          <th>Rank #</th>
          <th>Player</th>
          <th>League Rank</th>
          <th>League Points</th>
          <th>Current Character</th>
          <th>Most Used Character</th>
          <th>Region</th>
          <th>Platform</th>
        </tr>
      </thead>
      <tbody>
      % for pr in vm.player_rankings:
        <tr>
          <td>{{ pr.placement }}</td>
          <td><a href='/player/{{ pr.name }}'>{{ pr.name }}</a></td>
          <td>{{ pr.league.name }}</td>
          <td>{{ pr.league_points }}</td>
          <td>{{ pr.favorite_character.name }}</td>
          <td>{{ pr.most_used_character.name }}</td>
          <td>{{ pr.region }}</td>
          <td>{{ pr.platform.upper() if pr.platform else 'N/A' }}</td>
        </tr>
      % end
      </tbody>
    </table>
  </div>
% include('_copyright.tpl')
</div>
<script type="text/javascript">
$(document).ready(function() {
  $('#leaderboard').DataTable({
    "fixedHeader": true,
    "paging": false,
    "ordering": true,
    "info": false,
    "bFilter": false,
    "order": [[0, 'asc']],
  });
});
</script>
</body>
</html>
