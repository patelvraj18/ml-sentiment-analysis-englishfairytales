// constructor for the books display
function BooksDisplay(lineChart, pieChartPercentage) {
  var self = this;
  self.lineChart = lineChart; // line chart instance
  self.pieChartPercentage = pieChartPercentage; // pie chart instance
  self.init();
}

// initialize the books display
BooksDisplay.prototype.init = function () {
  // init the svg and much of the other components
  var self = this;
  self.margin = { top: 10, right: 20, bottom: 30, left: 20 }; // svg margins
  var booksDisplayDiv = d3.select("#books-display").classed("fullView", true);

  self.svgWidth = 725 - self.margin.left - self.margin.right;
  self.svgHeight = 250;

  // create svg element within the div
  self.svg = booksDisplayDiv.append("svg")
    .attr("width", self.svgWidth)
    .attr("height", self.svgHeight)

  this.update()

}

// BooksDisplay.prototype.adjustDimensions = function () {
//   var self = this;
//   self.svgWidth = d3.select("#books-display").node().clientWidth - self.margin.left - self.margin.right;
//   self.svg.attr("width", self.svgWidth);
// }

BooksDisplay.prototype.update = function () {
  var self = this;

  // dimensions of each rectangle
  let rectHeight = self.svgHeight / 5;
  let rectWidth = self.svgWidth;

  // data for each book
  self.books = [
    { BOOK: "I - MOLLY WHUPPIE", NUMBER: 1 },
    { BOOK: "II - THE STORY OF THE THREE BEARS", NUMBER: 2 },
    { BOOK: "III - THE FISH AND THE RING", NUMBER: 3 },
    { BOOK: "IV - THE THREE HEADS OF THE WELL", NUMBER: 4 },
    { BOOK: "V - MR. VINEGAR", NUMBER: 5 }
  ];

  // adding rectangles to the svg
  var rects = self.svg.selectAll("rect")
    .data(self.books)
    .enter().append("rect")

  rects
    .attr("x", (self.svgWidth - rectWidth) / 2)
    .attr("y", function (d, i) { return i * rectHeight; })
    .attr("width", rectWidth)
    .attr("height", rectHeight)
    .attr("fill", "#740F35")
    .attr("stroke", "white")
    .attr("class", "bookRect")
    .on("click", function (event, d) { // handling click events to switch between books
      self.svg.selectAll("rect").classed("active", false);
      d3.select(this).classed("active", true);
      loadInfo(d.NUMBER);
    });

  self.svg.selectAll(".bookRectText").remove();

  // adding text to each rectangle
  self.svg.selectAll(".bookRectText")
    .data(self.books)
    .enter().append("text")
    .attr("class", "bookRectText")
    .attr("fill", "#f9e279")
    .attr("x", 30)
    .attr("y", function (d, i) {
      return (i * rectHeight) + (rectHeight / 2) + 4;
    })
    .text(function (d) { return d.BOOK; });

  // load the data for the books and update the other visualizations
  function loadInfo(bookNumber) {
    var csvFile = "../data/processed/story_" + bookNumber + "_sentiment_processed.csv";
    d3.csv(csvFile)
      .then(function (bookData) {
        self.lineChart.update(bookData);
        self.pieChartPercentage.update(bookData);
      })
      .catch(function (error) {
        console.error("Error loading data:", error);
      });
  }

  // trigger click on Book 1 by default
  self.svg.selectAll("rect")
    .filter(function (d) { return d.NUMBER === 1; })
    .each(function (d) { this.dispatchEvent(new Event('click')); });
}

