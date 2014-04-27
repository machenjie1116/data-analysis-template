var w = 900
var h = 700
var	r = 6


function network(data)
{
	d3.json("data/" + data, function(dataset){
		// Delete previous svg to load different city
		d3.select("svg").remove()
		// Initialize a default force layout, using the nodes and edges
		var force = d3.layout.force()
			.nodes(dataset.nodes)
			.links(dataset.edges)
			.size([w, h])
			.linkDistance([10])
			.charge([-50])
			.start();

		// Create SVG
		var svg = d3.select("body")
			.append("svg")
			.attr("width", w)
			.attr("height", h);			

		var colors = d3.scale.category20();

		// Create links between user and user reviewed businesses
		var edges = svg.selectAll("line")
			.data(dataset.edges)
			.enter()
			.append("line")
			.style("stroke", "#ccc")
			.style("stroke-width", 0.2);
			
		// Create nodes, sized by review count
		var nodes = svg.selectAll("circle")
			.data(dataset.nodes)
			.enter()
			.append("circle")
			.attr("r", function(d){
				if (d.user_reviewcount){return d.user_reviewcount}
				else if (d.bus_reviewcount){return d.bus_reviewcount/3} 
			})
			.style("fill", function(d,i){return colors(i);})
			.call(force.drag);
				
		// Text when hover
		nodes.append("title")
			.data(dataset.nodes)
			.text(function(d){
				content = d._name
				if (d.bus_reviewcount){content += '\nReview Count: ' + d.bus_reviewcount}
				else if (d.user_reviewcount){content += '\nReview Count: ' + d.user_reviewcount + '\nUser Match: ' + d.user_match + '\nRestaurant Recommendation: ' + d.rest_rec}
				return content});
		
		// Make locations for nodes according to ticks
		force.on("tick", function() {
			nodes.attr("cx", function(d) { return d.x = Math.max(r, Math.min(w - r, d.x)); })
				.attr("cy", function(d) { return d.y = Math.max(r, Math.min(h - r, d.y)); });
			
			edges.attr("x1", function(d) { return d.source.x; })
				.attr("y1", function(d) { return d.source.y; })
				.attr("x2", function(d) { return d.target.x; })
				.attr("y2", function(d) { return d.target.y; });
		});
	});
main()
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
    d3.select("#Houston")
        .on("click", function(d,i) {
            network('Houston.json')
        })
    d3.select("#Boston")
        .on("click", function(d,i) {
            network('Boston.json')
        })
    //	make Berkeley default network
    network('Berkeley.json')
};
