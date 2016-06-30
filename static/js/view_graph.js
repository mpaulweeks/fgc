(function(module){

    var tool = Module("tool");
    var str_format = tool.str_format;

    var COLORS = [
        "#d11141",
        "#00b159",
        "#00aedb",
        "#f37735",
        "#ffc425",
        "#a200ff"
    ];
    var color_id = 0;


    var CHART_HTML = '<div class="chart_holder"><div class="chart_title">{2}<br/><br/></div><canvas class="chart" id="{1}" width="600" height="600"></canvas></div>';

    function next_color(){
        color_id = (color_id + 1) % COLORS.length;
        return COLORS[color_id];
    }

    function highlight(color){
        return tool.shadeColor(color, 0.2);
    }

    function lowlight(color){
        return tool.shadeColor(color, -0.2);
    }

    function get_pie_chart(base_chart, dp_data, dp_type){
        var graph_data = [];
        for (var label in dp_data){
            var d = {};
            d.value = dp_data[label].count;
            d.label = label;
            d.color = next_color();
            d.highlight = highlight(d.color);
            graph_data.push(d);
        }
        return base_chart.Pie(graph_data);
    }

    function get_polar_chart(base_chart, dp_data, dp_type){
        var graph_data = [];
        for (var label in dp_data){
            var d = {};
            d.value = dp_data[label].count;
            d.label = label;
            d.color = next_color();
            d.highlight = highlight(d.color);
            graph_data.push(d);
        }
        return base_chart.PolarArea(graph_data);
    }

    function display_factory(chart, dp_data, dp_name){
        var func = function(evt){
            var info = chart.getSegmentsAtEvent(evt);
            console.log(info);
            var label = info[0].label;
            var cards = dp_data[label].cards;
            var title = dp_name + ' - ' + label;
            display_cards(cards, title);
        };
        return func;
    }

    module.run = function(){
        var data_str = $('#server_data').html()
        $('#server_data').empty()
        var data = JSON.parse(data_str);
        var dp_data = {};
        var total_data = 0;
        data.forEach(function (char_tuple){
            dp_data[char_tuple[0]] = {
                count: char_tuple[1],
            };
            total_data += char_tuple[1];
        })

        var dp_name = 'characters';
        var chart_title = 'Character distribution for ' + total_data + ' games';
        $("#charts").append(str_format(CHART_HTML, dp_name, chart_title));
        var div = $(".chart#" + dp_name);
        var base_chart = new Chart(div.get(0).getContext("2d"));
        var chart_factory = get_pie_chart;
        var chart = chart_factory(base_chart, dp_data, dp_name);
        // div.click(display_factory(chart, dp_data, dp_name));
    };

})(Module('view_graph'));
