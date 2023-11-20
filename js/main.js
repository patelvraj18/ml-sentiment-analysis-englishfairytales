(function () {
  var instance = null;
  function init() {
    // creating instances for each visualization
    var lineChart = new LineChart();
    var pieChartPercentage = new PieChartPercentage();

    // pass this data and instances of all the charts that update in booksDisplay
    var booksDisplay = new BooksDisplay(lineChart, pieChartPercentage);

    // set up the initial layout for when the browser loads
    booksDisplay.update();
  }

  /**
   *
   * @constructor
   */
  function Main() {
    if (instance !== null) {
      throw new Error("Cannot instantiate more than one class");
    }
  }

  /**
   *
   * @returns {Main singleton class |*}
   */
  Main.getInstance = function () {
    var self = this
    if (self.instance == null) {
      self.instance = new Main();

      //called only once when the class is initialized
      init();
    }
    return instance;
  }

  Main.getInstance();
})();