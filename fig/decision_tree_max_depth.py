from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import plotly.express as px

data = fetch_ucirepo(id=602)   # fetch dataset
X = data.data.features        # data (as pandas dataframes)
y = data.data.targets

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)

accuracy_list = []
for i in range(4,25+1,1):

  dt = DecisionTreeClassifier(criterion='gini',
                              max_depth=i,
                              min_samples_split=2,
                              min_samples_leaf=1,
                              random_state=123)

  # เริ่มเทรนร
  dt.fit(X_train, y_train)

  # Training set
  y_train_pred = dt.predict(X_train)
  acc_train = accuracy_score(y_train, y_train_pred)

  # Test set
  y_test_pred = dt.predict(X_test)
  acc_test = accuracy_score(y_test, y_test_pred)

  # Track accuracy
  accuracy_list.append([i, acc_train, 'train'])
  accuracy_list.append([i, acc_test, 'test'])

df = pd.DataFrame(accuracy_list, columns=['max_depth', 'accuracy', 'set'])
fig = px.line(df,
        y='accuracy',
        x='max_depth',
        color='set',
        log_y=True,
        text='accuracy',
        markers=True)        
fig.update_traces(texttemplate="%{y}")
fig.update_layout(yaxis_tickformat=".1%")
fig.update_traces(textposition='bottom right',textfont_size=9)
fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
)
fig.update_layout(legend=dict(
    yanchor="bottom",
    y=0.01,
    xanchor="right",
    x=0.99
))
fig.write_image('fig/decision_tree_max_depth.svg', width=900, height=400)
