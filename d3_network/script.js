// Width and height
var w = 900;
var h = 700;

// Load Data
d3.json("data.json",function(dataset){

	// Initialize a default force layout, using the nodes and edges
	var force = d3.layout.force()
		.nodes(dataset.nodes)
		.links(dataset.edges)
		.size([w, h])
		.linkDistance([10])
		.charge([-100])
		.start();

	var colors = d3.scale.category10();

	// Create SVG element
	var svg = d3.select("body")
		.append("svg")
		.attr("width", w)
		.attr("height", h);		

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
		.attr("r", function(d){return d.reviewcount})
		.style("fill", function(d,i){return colors(i);})
		.call(force.drag);
				
	// Draw text on the screen
	nodes.append("title")
		.data(dataset.nodes)
		.text(function(d){return d.person});
			
	// Every time the simulation "ticks", this will be called
	force.on("tick", function() {
		edges.attr("x1",function(d){return d.source.x;})
				.attr("y1",function(d){return d.source.y;})
				.attr("x2",function(d){return d.target.x;})
				.attr("y2",function(d){return d.target.y;});
		nodes.attr("cx",function(d){return d.x;})
				.attr("cy",function(d){return d.y;});
	
		});
});
