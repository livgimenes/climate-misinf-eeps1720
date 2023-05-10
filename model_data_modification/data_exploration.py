import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('cleaned_data/training.csv')
label_counts = data['claim'].value_counts()

plt.bar(label_counts.index, label_counts.values, color='c')

# add a title and axis labels
plt.title('Distribution of Superclaims in Data Set', fontweight='heavy')
plt.xlabel('Superclaim', fontweight='heavy')
plt.ylabel('Count', fontweight='heavy')
plt.savefig("data_dist.png", dpi=300)

# show the plot
plt.show()