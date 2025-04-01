from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import loader
import numpy as np

class Model:
    """
    A class used to represent modelling process (training, testing, and evaluation).

    Attributes
    ----------
    model: RandomForestClassifier | None
        The classification model that will be used to predict the class from audio data.

    Methods
    -------
        train(x_train, y_train)
            Train the model using random forest classifier if there is no model. Otherwise, this part will be skipped.

        test(x_test)
            Predict the testing set using the model.

        evaluate(x_test, y_test)   
            Evaluate the model using some evaluation metrics, such as accuracy, precision, recall, and F1-score to make sure the model can performs well to new data.
    """
     
    def __init__(self):
        """        
        Load the model using pickle library if exists. Otherwise, set the model as none so it can be validated when the model is about 
        to be trained.
        """
        try:
            self.model = loader.load_model()
        except:
            self.model = None

    def train(self, x_train, y_train):
        """
        Train the model using random forest classifier if there is no model. Otherwise, this part will be skipped.

        Parameters
        ----------
        x_train : np.ndarray
            Feature data from training set.

        y_train : np.ndarray
            Label data from training set.
        """
        if self.model == None:  
            self.model = RandomForestClassifier(max_features='log2', min_samples_split=3, n_estimators=200)
            print('training start')
            self.model.fit(x_train, y_train)

    def test(self, x_test):
        """
        Predict the testing set using the model.

        Parameters
        ----------
        x_test : np.ndarray
            Features data from testing set.

        Returns
        -------
            A np.ndarray of probability score for each class.
        """
        return self.model.predict_proba(x_test)

    def evaluate(self, x_test, y_test):
        """
        Evaluate the model using some evaluation metrics, such as accuracy, precision, recall, and F1-score to make sure the model can performs well to new data.

        Parameters
        ----------
        x_test : np.ndarray
            Feature data from testing set.
        y_test: np.ndarray
            Label data from testing set.
        """
        y_pred = self.test(x_test)
        y_pred = [np.argmax(pred) for pred in y_pred]
        print(classification_report(y_test, y_pred))
