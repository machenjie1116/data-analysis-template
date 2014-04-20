var w = 800
var h = 700
var	r = 6


function network(data)
{
	d3.json("data/" + data, function(dataset){
		d3.select("svg").remove()
		// Initialize a default force layout, using the nodes and edges
		var force = d3.layout.force()
			.nodes(dataset.nodes)
			.links(dataset.edges)
			.size([w, h])
			.linkDistance([10])
			.charge([-50])
			.start();

		// Create SVG element
		var svg = d3.select("body")
			.append("svg")
			.attr("width", w)
			.attr("height", h);			

		var colors = d3.scale.category20();

		// Create edges as lines
		var edges = svg.selectAll("line")
			.data(dataset.edges)
			.enter()
			.append("line")
			.style("stroke", "#ccc")
			.style("stroke-width", 0.2);
			
		// Create nodes as circles
		var nodes = svg.selectAll("circle")
			.data(dataset.nodes)
			.enter()
			.append("circle")
			.attr("r", function(d){
				if (d.user_reviewcount){return d.user_reviewcount}
				else if (d.bus_reviewcount){ 
					if (d.bus_reviewcount < 1000){return d.bus_reviewcount}
					else {return d.bus_reviewcount/10}
				}
			})
			.style("fill", function(d,i){return colors(i);})
			.call(force.drag);
				
		// Draw text on the screen, 
		nodes.append("title")
			.data(dataset.nodes)
			.text(function(d){
				content = d._name
				if (d.bus_reviewcount){content += '\nReview Count: ' + d.bus_reviewcount*10}
				return content});
		
		// Every time the simulation "ticks", this will be called
		force.on("tick", function() {
			nodes.attr("cx", function(d) { return d.x = Math.max(r, Math.min(w - r, d.x)); })
				.attr("cy", function(d) { return d.y = Math.max(r, Math.min(h - r, d.y)); });
			
			edges.attr("x1", function(d) { return d.source.x; })
				.attr("y1", function(d) { return d.source.y; })
				.attr("x2", function(d) { return d.target.x; })
				.attr("y2", function(d) { return d.target.y; });
		});
	});

};

function init()
{
    d3.select("#Berkeley")
        .on("click", function(d,i) {
            network('Berkeley.json')
        })   
    d3.select("#NewYork")
        .on("click", function(d,i) {
            network('New_York.json')
        })   
    d3.select("#LosAngeles")
        .on("click", function(d,i) {
            network('Los_Angeles.json')
        })
    //make the network
    network('Berkeley.json')
};
