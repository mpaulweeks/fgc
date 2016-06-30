(function(module){

    module.is_local = window.location.href.indexOf('file:///') > -1;
    module.is_firefox = navigator.userAgent.toLowerCase().indexOf('firefox') > -1;

    module.str_format = function(str) {
        var args = arguments;
        return str.replace(/{(\d+)}/g, function(match, number) { 
            return typeof args[number] != 'undefined' ? args[number] : match;
        });
    };

    module.read_url_param = function(param_name, as_list){
        as_list = as_list || false;
        var vars = {};
        var q = document.URL.split('?')[1];
        if(q != undefined){
            q = q.split('&');
            for(var i = 0; i < q.length; i++){
                var param = q[i].split('=');
                var name = param[0];
                var value = param[1];
                vars[name] = vars[name] || [];
                vars[name].push(value);
            }
        }
        if (vars.hasOwnProperty(param_name)){
            if (vars[param_name].length == 1 && !as_list){
                return vars[param_name][0];
            }
            return vars[param_name];
        }
        return null;
    };

    // http://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors
    function shadeColor2(color, percent) {
        var f=parseInt(color.slice(1),16),t=percent<0?0:255,p=percent<0?percent*-1:percent,R=f>>16,G=f>>8&0x00FF,B=f&0x0000FF;
        return "#"+(0x1000000+(Math.round((t-R)*p)+R)*0x10000+(Math.round((t-G)*p)+G)*0x100+(Math.round((t-B)*p)+B)).toString(16).slice(1);
    }
    module.shadeColor = shadeColor2;

})(Module('tool'));
