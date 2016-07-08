<!DOCTYPE html>
<html lang="en">
<head>
    % include('_header.tpl', title='About SFV.FGC')
</head>
<body>
<div class="container text-center">

    % include('_navbar.tpl')

    <div class="col-md-12">
        <h1> FightingGame.Community </h1>
    </div>
    <div class="col-md-1"></div>
    <div class="col-md-4">
        <br/>
        <a class="twitter-timeline" href="https://twitter.com/fgc_status" data-widget-id="706198119713783810">Tweets by @fgc_status</a>
        <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
    </div>
    <div class="col-md-7 text-left">
        <h3> frequently asked questions </h3>
        <p class="question"> Who made this? </p>
        <p> A scrub named M. Paul Weeks </p>
        <p class="question"> How can I find out about updates? </p>
        <p> Follow <a href="https://twitter.com/fgc_status">@fgc_status</a> or check the sidebar on this page.</p>
        <p class="question"> I just played some games last night. Why aren't they included on my player page? </p>
        <p> It could take up to 24 hours any given player's history to update. </p>
        <p class="question"> Why doesn't the leaderboard match what's in game? </p>
        <p> The leaderboard updates once a day, in the morning. It could be slightly behind. </p>
        <p class="question"> I registered a Fighter ID. Why can't I find it? </p>
        <p> Follow the instructions <a href="/new_player">here</a>. Give it up to an hour to refresh. </p>
        <p class="question"> Why is it only showing 100 matches when I've played more than that? </p>
        <p> When a player is first added, all I can grab are the last 100 matches. <br/> From that point on, all future matches will be recorded and stored. </p>
        <p class="question"> Is this only showing Ranked matches? </p>
        <p> Yes, for now. </p>
        <p class="question"> Why aren't you tracking every player automatically? </p>
        <p> I would love to but I simply don't have the resources. </p>
        <p class="question"> Where do you get your data? </p>
        <p> Everything you see on this site is available through the game! <br/> I'm just helping you look at it :) </p>
        <p class="question"> Will you provide a public API? </p>
        <p> Eventually! It's pretty low on my list of priorities though. <br/> If you require any specific data, let me know and I'll try to work it in. </p>
        <p class="question"> I have a bug / great idea / question not answered by this FAQ! </p>
        <p> You can email <a href="mailto:fightinggamedotcommunity@gmail.com">fightinggamedotcommunity@gmail.com</a> or find me on twitter at <a href="https://twitter.com/fgc_status">@fgc_status</a> (DMs allowed)</p>
    </div>
% include('_copyright.tpl')
</div>
</body>
</html>
