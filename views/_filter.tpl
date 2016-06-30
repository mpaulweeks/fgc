
<form action="/matchup" method="get">
  <div class="col-md-2">
    <h5>
        Filter by League:
    </h5>
  </div>
  <div class="col-md-4">
    <select class="selectpicker" multiple data-none-selected-text='all leagues' name="player" id="player-select">
      % for league in vm.cfn_league_cache.leagues():
        <option value="{{ league.code }}"
            {{ "selected" if not vm.p1_all_leagues and league.code in vm.p1_league_codes else "" }}
        >
            {{ league.name }}
        </option>
      % end
    </select>
    <button type="button" class="btn dark btn-sm" id="player-clear">
      reset
    </button>
  </div>
  <div class="col-md-1">
    <h5>VS</h5>
  </div>
  <div class="col-md-4">
    <select class="selectpicker" multiple data-none-selected-text='all leagues' name="opponent" id="opponent-select">
      % for league in vm.cfn_league_cache.leagues():
        <option value="{{ league.code }}"
            {{ "selected" if not vm.p2_all_leagues and league.code in vm.p2_league_codes else "" }}
        >
            {{ league.name }}
        </option>
      % end
    </select>
    <button type="button" class="btn dark btn-sm" id="opponent-clear">
      reset
    </button>
  </div>
  <div class="col-md-1">
    <button type="submit" class="btn dark">
      Load
    </button>
  </div>
</form>

<script type="text/javascript">
$(document).ready(function() {
    $('#player-clear').click(function (){
        $('#player-select').selectpicker('val', '');
    });
    $('#opponent-clear').click(function (){
        $('#opponent-select').selectpicker('val', '');
    });
});
</script>

<div class="col-md-12">
  <hr/>
</div>
