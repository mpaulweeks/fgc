
<nav class="navbar navbar-default navbar-static-top">

  <div class="container-fluid">
    <a class="navbar-brand mobileHide" href="http://www.fightinggame.community/">FightingGame.Community</a>
    <a class="navbar-brand mobileShow" href="http://www.fightinggame.community/">FG.C</a>

    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navHeaderCollapse">
      <span class="sr-only">Toggle navigation</span>
      <span class="icon-bar"></span>
      <span class="icon-bar"></span>
      <span class="icon-bar"></span>
    </button>
    <div class="collapse navbar-collapse navHeaderCollapse">
      <ul class="nav navbar-nav navbar-right">
        <li><a href="/">Welcome</a></li>
        <li><a href="/matchup">Character Matchups</a></li>
        <li><a href="/leaderboard">Leaderboard</a></li>
        <li><a href="/player">Find Player</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </div>
  </div>
</nav>

% if (not defined('is_goodbye')) or (not is_goodbye):
  <div class="col-md-12">
  <p> SFV.FGC stopped updating on June 29. </p>
  <p> <a href="/goodbye">Thanks for everything!</a> </p>
  <hr/>
  </div>
% end
