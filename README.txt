READ ME!!!

Hi there! This is Vraj's Patel Assignment 3 website. Outside of the provided textbook of Interactive Data Visualization for the Web, I did use external resources:
* https://www.kaggle.com/code/robikscube/sentiment-analysis-python-youtube-tutorial/notebook (accessed on 10/21)
* https://www.w3schools.com/css/css_rwd_viewport.asp (accessed on 10/20)
* https://www.w3schools.com/tags/tag_input.asp (accessed on 10/22)
* https://huggingface.co/docs/transformers/model_doc/roberta (accessed on 10/21)
* https://pytorch.org/docs/stable/generated/torch.nn.functional.softmax.html (accessed on 10/21)
* https://docs.python.org/3/library/os.html (accessed on 10/21)
* https://docs.python.org/3/library/csv.html (accessed on 10/21)
* https://www.nltk.org/api/nltk.tokenize.html (accessed on 10/21)
* https://www.nltk.org/api/nltk.tokenize.punkt.html (accessed on 10/21)
* https://www.geeksforgeeks.org/writing-csv-files-in-python/ (accessed on 10/21)
* https://www.emailonacid.com/blog/article/email-development/emailology_media_queries_demystified_min-width_and_max-width/ (accessed on 10/22)
* https://www.w3schools.com/css/css3_box-sizing.asp (accessed on 10/22)
* https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener (accessed on 10/21)
* https://d3-graph-gallery.com/graph/pie_basic.html (accessed on 10/21)
* http://4waisenkinder.de/blog/2014/05/11/d3-dot-js-tween-in-detail/ (accessed on 10/21)
* https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/dispatchEvent (accessed on 10/21)
* https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-dasharray (accessed on 10/22)
* https://www.geeksforgeeks.org/d3-js-selection-classed-function/ (accessed on 10/22)
* https://d3js.org/d3-shape/line (accessed on 10/22)
* used google fonts api (accessed on 10/20)



A quick overview of the codebase: Majority of the code is within the js files and each specific design/visualization as its own file and a own object that is created in main.js. Main.js covers most of the OOP principles so that I can have objects of the various visualizations. Furthermore, the images folder hold the images alongside the css folder having the css corresponding to the two html sites: index.html and processbook.html. These two html files are at the primary directory to easily access. Then the associated libraries are within d3-components to access the d3.js and also the d3-tip as needed. Lastly, is the python script that I made to analyze and extract the sentiment analysis scores using the RoBERTa model within the python folder. The data that I processed was extracted into the data folder as a .csv file. So, this created the original data that I then processed to ensure that there no line breaks or awkward gaps. 

So, what may not be obvious for the scope of the class is the python script which I built with the help of some resources linked up top! In a large scope, it basically imports and initializes the appropriate models to then extract the sentiment score using the trained RoBERTa model to then use that later. I have the text of the various stories, and then a algorithm to extract each story one by one to analyze each sentence split by the nltk tokenizer. It gets the necessary scores and appends it to a array to be written to a csv file with the directory of data folder. Other than that the main js/html/css is pretty self explanatory using the OOP approach used in assignment 2 and encouraged for this project. 

