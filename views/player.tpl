<!DOCTYPE html>
<html lang="en">
<head>
    % include('_header.tpl', title=title)
</head>
<body>
<div class="container text-center">

    % include('_navbar.tpl')

<div class="col-md-12">
  <h1 class=""> {{ vm.name }} </h1>
  % if not vm.is_global:
    % if vm.updated_date:
      <p> Last updated: {{ vm.updated_date }} </p>
    % end
    % if vm.latest_match_date:
      <p> Last seen playing Ranked: {{ vm.latest_match_date }} </p>
    % end
  % end
  % if vm.is_global:
      <p> View statistics compiled from thousands of players and millions of matches. </p>
      <p> Filter by league to see how the matchups change based on the players' skill level. </p>
      <p> For example, see how Dictator (aka Bison) performs in <a href="/matchup?player=Bronze&opponent=Bronze#Dictator">Bronze</a> league compared to <a href="/matchup?player=Platinum&opponent=Platinum#Dictator">Platinum</a>.</p>
  % end
  <hr/>
</div>

% if vm.is_global:
    % include('_filter.tpl', vm=vm)
% end

% if vm.data_exists:
% if vm.is_global:
<div class="col-md-12">
  <h3> JUMP TO CHARACTER </h3>
  <br/>
  % for char_vm in vm.character_order:
    <a class="char_link" href="#{{ char_vm.name }}">
      <img class="char_portrait" src="{{ char_vm.img }}">
    </a>
  % end
  <br/>
  <br/>
  <hr/>
</div>

<div class='col-md-1'></div>
<div class='col-md-10'>
  <h3> STATS </h3>
  <br/>
  <table class="table">
    <thead>
      <tr>
        <th> Victory Type </th>
        <th> Most Likely </th>
        <th> Least Likely </th>
      </tr>
    </thead>
    <tbody>
    % for win_type in [6, 7, 1, 4, 3]:
      <tr>
        <td> {{ vm.win_types[win_type].name.upper() }} </td>
        <td><a href="#{{ vm.win_types[win_type].best.name }}">{{ vm.win_types[win_type].best.name }}</td>
        <td><a href="#{{ vm.win_types[win_type].worst.name }}">{{ vm.win_types[win_type].worst.name }}</td>
      </tr>
    % end
    <tr>
      <td> {{ vm.win_types[5].name.upper() }} </td>
        <td><a href="#{{ vm.win_types[5].best.name }}">{{ vm.win_types[5].best.name }}</td>
      <td> N/A </td>
    </tr>
    </tbody>
  </table>
</div>
<div class='col-md-1'></div>
<div class="col-md-12">
  <hr/>
</div>
% else:
<div class='col-md-3'></div>
<div class='col-md-6'>
  <h3> STATS </h3>
  <br/>
  <table class="table">
    <tbody>
      <tr>
        <td>Games Played</td>
        <td> {{ vm.data.game_count }} </td>
      </tr>
      <tr>
        <td>Overall Win Rate</td>
        <td> {{ int(100*vm.data.game_wins/vm.data.game_count) }}% </td>
      </tr>
      <tr>
        <td>League Rank</td>
        <td> {{ vm.league.name }} </td>
      </tr>
      <tr>
        <td>League Points</td>
        <td> {{ vm.league_points }} </td>
      </tr>
      % if vm.player.region:
      <tr>
        <td>Region</td>
        <td> {{ vm.player.region }} </td>
      </tr>
      % end
      % if vm.player.platform:
      <tr>
        <td>Platform</td>
        <td> {{ vm.player.platform.upper() }} </td>
      </tr>
      % end
    </tbody>
  </table>
</div>
<div class='col-md-3'></div>
<div class="col-md-12">
  <hr/>
</div>
% end

<div class="col-md-12">
  <h3> CHARACTER MATCHUPS </h3>
  <br/>
% for char in vm.data.characters_sorted:
  <a href="#" name="{{ char.vm.name }}" class="inactiveLink">
    <img class="char_portrait" src="{{ char.vm.img }}" />
  </a>
  <table class="table matchup-table" id="table-{{ char.character_id }}">
    <thead>
      <tr>
        <th>Character</th>
        <th>Opponent</th>
        <th>Win Rate</th>
        <th>Games Played</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>{{ char.vm.name }}</td>
        <td>- overall -</td>
        <td>{{ int(100*char.game_wins/char.game_count) }}%</td>
        <td>{{ char.game_count }}</td>
      </tr>
    % for opp in char.opponents_sorted:
      <tr>
        <td>{{ char.vm.name }}</td>
        % if vm.is_global:
          <td><a href="#{{ opp.vm.name }}">{{ opp.vm.name }}</a></td>
        % else:
          <td>{{ opp.vm.name }}</td>
        %end
        <td>{{ int(100*opp.game_wins/opp.game_count) }}%</td>
        <td>{{ opp.game_count }}</td>
      </tr>
    % end
    </tbody>
  </table>
  <br/>
% end
% else:
  <hr/>
  % if vm.is_global:
    <p> No data exists for this matchup. </p>
  % else:
    <p> This player hasn't played any Ranked games. </p>
  % end
% end
</div>
% include('_copyright.tpl')
</div>
<script type="text/javascript">
$(document).ready(function() {
  $('.matchup-table').each(function (){
    $(this).DataTable({
      "paging": false,
      "ordering": true,
      "info": false,
      "bFilter": false,
      "columnDefs": [
        { "orderable": false, "targets": 0 }
      ],
      "order": [[3, 'desc']],
    });
  });
});
</script>
</body>
</html>
