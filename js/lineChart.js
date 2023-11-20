// define the constructor function
function LineChart() {
  var self = this;
  self.init();
}

// initialize the line chart
LineChart.prototype.init = function () {
  var self = this;
  self.margin = { top: 30, right: 20, bottom: 60, left: 70 }; // margins
  var lineChartDiv = d3.select("#line-chart")

  self.svgWidth = 550 - self.margin.left - self.margin.right;
  self.svgHeight = 500;

  self.mainSVG = lineChartDiv.append("svg")
    .attr("width", self.svgWidth + self.margin.left + self.margin.right)
    .attr("height", self.svgHeight + self.margin.top + self.margin.bottom);

  // append a group element with transformation to the center
  self.svg = self.mainSVG.append("g")
    .attr("transform", "translate(" + self.margin.left + "," + self.margin.top + ")");

  // checkbox event listeners here to update the line chart
  d3.select("#positiveCheckbox").on("change", function () {
    self.update(self.currentStory);
  });
  d3.select("#neutralCheckbox").on("change", function () {
    self.update(self.currentStory);
  });
  d3.select("#negativeCheckbox").on("change", function () {
    self.update(self.currentStory);
  });
}

// update the line chart
LineChart.prototype.update = function (story) {
  var self = this;
  self.currentStory = story;

  // checking the current state of the checkboxes
  var isPositiveChecked = document.getElementById("positiveCheckbox").checked;
  var isNeutralChecked = document.getElementById("neutralCheckbox").checked;
  var isNegativeChecked = document.getElementById("negativeCheckbox").checked;

  // clear previous elements
  self.svg.selectAll("path").remove();
  self.svg.selectAll("g.axis").remove();
  self.svg.selectAll("text.axis-title").remove();

  // define the necessary scales
  var xScale = d3.scaleLinear()
    .domain([0, 1])
    .range([0, self.svgWidth]);

  var yScale = d3.scaleLinear()
    .domain([0, 1])
    .range([self.svgHeight, 0]);

  // make line generators for each type of sentiment
  var positiveLine = d3.line()
    .x(function (d, i) { return xScale(i / (story.length - 1)); })
    .y(function (d) { return yScale(d.Positive_Score); });

  var neutralLine = d3.line()
    .x(function (d, i) { return xScale(i / (story.length - 1)); })
    .y(function (d) { return yScale(d.Neutral_Score); });

  var negativeLine = d3.line()
    .x(function (d, i) { return xScale(i / (story.length - 1)); })
    .y(function (d) { return yScale(d.Negative_Score); });

  var totalLength = [0, 0, 0];

  // draw its sentiment line ONLY if the checkbox is checked
  ["positive", "neutral", "negative"].forEach(function (type, index) {
    if ((type === "positive" && !isPositiveChecked) || (type === "neutral" && !isNeutralChecked) || (type === "negative" && !isNegativeChecked)) {
      return;
    }

    // chose the appropriate line function and color depending on the type of sentiment
    var lineFunction = (type === "positive") ? positiveLine : (type === "neutral") ? neutralLine : negativeLine;
    var color = (type === "positive") ? "green" : (type === "neutral") ? "blue" : "red";

    // plot the corresponding lines and animate the drawing using transitions
    self.svg.append("path")
      .datum(story)
      .attr("fill", "none")
      .attr("stroke", color)
      .attr("stroke-width", 1.5)
      .attr("d", lineFunction)
      .each(function () {
        totalLength[index] = this.getTotalLength();
      })
      .attr("stroke-dasharray", totalLength[index] + " " + totalLength[index])
      .attr("stroke-dashoffset", totalLength[index])
      .transition()
      .duration(2000)
      .attr("stroke-dashoffset", 0);
  });

  // x, y values with custom tick values and formatting
  var tickValues = [0, 0.2, 0.4, 0.6, 0.8, 1];

  var xAxis = d3.axisBottom(xScale)
    .tickValues(tickValues)
    .tickFormat(d3.format(".0%"));

  var yAxis = d3.axisLeft(yScale).tickFormat(d3.format(".0%"));

  // draw the x-axis and animate its appearance
  self.svg.append("g")
    .attr("transform", "translate(0," + self.svgHeight + ")")
    .attr("class", "axis")
    .call(xAxis)
    .style("opacity", 0)
    .transition()
    .duration(1000)
    .style("opacity", 1);

  // draw the y-axis and animate its appearance
  self.svg.append("g")
    .attr("class", "axis")
    .call(yAxis)
    .style("opacity", 0)
    .transition()
    .duration(1000)
    .style("opacity", 1);

  // draw the x-axis label and animate its appearance
  self.svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - self.margin.left - 5)
    .attr("x", 0 - (self.svgHeight / 2))
    .attr("dy", "1em")
    .attr("class", "axis-title")
    .style("text-anchor", "middle")
    .text("Sentiment Percentage Score")
    .style("opacity", 0)
    .transition()
    .duration(1500)
    .style("opacity", 1);

  // draw the y-axis label and animate its appearance
  self.svg.append("text")
    .attr("transform", "translate(" + (self.svgWidth / 2) + " ," + (self.svgHeight + self.margin.bottom - 5) + ")")
    .attr("class", "axis-title")
    .style("text-anchor", "middle")
    .text("Story Completion Rate")
    .style("opacity", 0)
    .transition()
    .duration(1500)
    .style("opacity", 1);
}
