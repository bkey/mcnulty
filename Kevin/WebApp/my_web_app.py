import flask
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd

#---------- MODEL IN MEMORY ----------------#

# Read the scientific data on breast cancer survival,
# Build a LogisticRegression predictor on it
df = pd.read_csv("homeowner.data")

X = df[['age','marital_status','edu_level_id','income_total']]
Y = df['own']
PREDICTOR = KNeighborsClassifier(n_neighbors=100).fit(X,Y)


#---------- URLS AND WEB PAGES -------------#

# Initialize they app
app = flask.Flask(__name__)

# Homepage
@app.route("/")
def viz_page():
    """ Homepage: serve our visualization page, awesome.html
    """
    with open("viz.html", 'r') as viz_file:
        return viz_file.read()

# Get an example and return it's score from the predictor model
@app.route("/score", methods=["POST"])
def score():
    """  When A POST request with json data is made to this uri,
         Read the example from the json, predict probability and
         send it with a response
    """
    # Get decision score for our example that came with the request
    data = flask.request.json
    x = np.matrix(data["example"])
    score = PREDICTOR.predict_proba(x)
    # Put the result in a nice dict so we can send it as json
    results = {"score": score[0 , 0]}
    return flask.jsonify(results)

#--------- RUN WEB APP SERVER ------------#
app.debug = True
# Start the app server on port 80
# (The default website port)
app.run()

