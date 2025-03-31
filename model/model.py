from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import loader
import parameter

class Model:
    def __init__(self):
        try:
            self.model = loader.load_model()
        except:
            self.model = None

    def train(self, x_train, y_train):
        if self.model == None:  
            self.model = GridSearchCV(RandomForestClassifier(), parameter.grid)
            print('training start')
            self.model.fit(x_train, y_train)

    def test(self, x_test):
        return self.model.predict(x_test)

    def evaluate(self, x_test, y_test):
        y_pred = self.test(x_test)
        print(classification_report(y_test, y_pred))
        print(self.model.best_estimator_)
        print(self.model.best_params_)
