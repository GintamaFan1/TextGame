import pandas as pd
import matplotlib.pyplot as plt

# Load a sample dataset
url = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv'
df = pd.read_csv(url)

# Display basic statistics
print(df.describe())

# Plot a histogram of the sepal length
plt.hist(df['sepal_length'], bins=20, color='blue', edgecolor='black')
plt.title('Distribution of Sepal Length')
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Frequency')
plt.show()