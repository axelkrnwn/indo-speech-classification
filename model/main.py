from sklearn.model_selection import train_test_split
import pandas as pd
import loader
import model
import preprocess
        
cepstral_coefficients, labels = loader.load_all()
df = pd.DataFrame(preprocess.resampling(cepstral_coefficients))

df['label'] = labels
X = df.drop(columns=['label'], axis=0)
X = preprocess.normalize(X)
X = preprocess.reduce_dimension(X)
Y = df['label']

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
clf = model.Model()
clf.train(x_train, y_train)
clf.evaluate(x_test, y_test)
loader.save_model(clf.model, 'model')