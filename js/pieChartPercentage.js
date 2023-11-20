// constructor for the pie chart showing sentiment percentages
function PieChartPercentage() {
  var self = this;
  self.init();
}

// initialize the pie chart with svg, margin, and transformation
PieChartPercentage.prototype.init = function () {
  var self = this;
  self.margin = { top: 30, right: 20, bottom: 30, left: 50 }; // svg margins
  var pieChartDiv = d3.select("#pie-chart") // div container in the html

  self.svgWidth = 450 - self.margin.left - self.margin.right;
  self.svgHeight = 400;

  // creates svg element within the div
  self.mainSVG = pieChartDiv.append("svg")
    .attr("width", self.svgWidth + self.margin.left + self.margin.right)
    .attr("height", self.svgHeight + self.margin.top + self.margin.bottom);

  // appends a g with transformation to the center
  self.svg = self.mainSVG.append("g")
    .attr("transform", "translate(" + (self.svgWidth / 2 + self.margin.left) + "," + (self.svgHeight / 2 + self.margin.top) + ")");
}

// render the tooltip
PieChartPercentage.prototype.tooltip_render = function (tooltip_data) {
  var self = this;
  var text = "<ul>";
  // make the tooltip content based on the data
  tooltip_data.result.forEach(function (row) {
    text += row.sentiment + ":\t\t" + "" + row.percentage + "%" + "</li>";
  });
  text += "</ul>";
  return text;
}

// draw the legend
PieChartPercentage.prototype.drawLegend = function () {
  var self = this;

  // remove any existing legend
  d3.select("#pie-chart-legend").select("svg").remove();

  // some constants used in this function
  const legendRectSize = 17.5;
  const legendSpacing = 5.25;
  const color = d3.scaleOrdinal()
    .domain(['Negative', 'Neutral', 'Positive'])
    .range(['#9b1c31', '#002366', '#136207']);

  // dimensions for the legend
  const legendSVGWidth = 200;
  const legendSVGHeight = 150;

  const legendSVG = d3.select("#pie-chart-legend")
    .append("svg")
    .attr("width", legendSVGWidth)
    .attr("height", legendSVGHeight);

  // add the rectangles 
  const legend = legendSVG.selectAll('.legend')
    .data(color.domain())
    .enter()
    .append('g')
    .attr('class', 'legend')
    .attr('transform', function (d, i) {
      const height = legendRectSize + legendSpacing;
      const offset = height * color.domain().length / 2; // if needed
      const horz = 10;
      const vert = i * height + legendSpacing;
      return 'translate(' + horz + ',' + vert + ')'; // translate the legend
    });

  // add the rects and the text using d3
  legend.append('rect')
    .attr('width', legendRectSize)
    .attr('height', legendRectSize)
    .style('fill', color)
    .style('stroke', color);

  legend.append('text')
    .style("font-size", "0.90rem")
    .attr('x', legendRectSize + legendSpacing)
    .attr('y', legendRectSize - legendSpacing + 1.2)
    .text(function (d) { return d; });
}

PieChartPercentage.prototype.update = function (story) {
  var self = this;

  // create the tooltip using d3.tip
  var tip = d3.tip().attr('class', 'd3-tip')
    .direction('s')
    .html(function (event) {
      var d = d3.select(this).datum();
      var tooltip_data = {
        "result": [
          { "sentiment": d.data.sentiment, "percentage": d.data.percentage }
        ]
      };
      return self.tooltip_render(tooltip_data);
    });

  // counts total number of each sentiment
  const totalCount = [0, 0, 0]
  story.forEach(function (sentence) {
    if (sentence.Highest_Label == "Negative") {
      totalCount[0] += 1
    } else if (sentence.Highest_Label == "Neutral") {
      totalCount[1] += 1
    } else if (sentence.Highest_Label == "Positive") {
      totalCount[2] += 1
    }
  });

  // calculate percentages of sentiment
  const total = totalCount[0] + totalCount[1] + totalCount[2];
  const percentages = [
    { sentiment: 'Negative', percentage: ((totalCount[0] / total) * 100).toFixed(2) },
    { sentiment: 'Neutral', percentage: ((totalCount[1] / total) * 100).toFixed(2) },
    { sentiment: 'Positive', percentage: ((totalCount[2] / total) * 100).toFixed(2) },
  ];

  const pie = d3.pie()
    .value(d => parseFloat(d.percentage))
    .sort(null);

  const radius = Math.min(self.svgWidth, self.svgHeight) / 2;
  const arc = d3.arc()
    .innerRadius(0)
    .outerRadius(radius);

  // defining a color scale
  const color = d3.scaleOrdinal()
    .domain(['Negative', 'Neutral', 'Positive'])
    .range(['#9b1c31', '#002366', '#136207']);

  // bind the data to the pie segments
  const pathUpdate = self.svg.selectAll('path')
    .data(pie(percentages));

  pathUpdate.exit().remove();

  // apply transitions, append the path, and add the tooltip
  pathUpdate.enter()
    .append('path')
    .attr('fill', d => color(d.data.sentiment))
    .on('mouseover', tip.show)
    .on('mouseleave', tip.hide)
    .merge(pathUpdate)
    .call(tip)
    .transition()
    .duration(1000)
    // http://4waisenkinder.de/blog/2014/05/11/d3-dot-js-tween-in-detail/ for the cool transition 
    .attrTween('d', function (d) {
      const interpolate = d3.interpolate({ startAngle: 0, endAngle: 0 }, d);
      return function (t) {
        return arc(interpolate(t));
      };
    });

  // call the draw the legend function
  self.drawLegend();
}
