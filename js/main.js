// referred to assignment 2 when making this OOP approach :)
(function () {
  var instance = null;
  function init() {
    // creating instances for each visualization
    var lineChart = new LineChart();
    var pieChartPercentage = new PieChartPercentage();

    // pass this data and instances of all the charts that update in booksDisplay
    var booksDisplay = new BooksDisplay(lineChart, pieChartPercentage);

    // set up the initial layout for when the browser loads
    booksDisplay.adjustDimensions();
    booksDisplay.update();

    // window resize listener upon changing, https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener
    window.addEventListener('resize', function () {
      booksDisplay.adjustDimensions();
      booksDisplay.update();
    });
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