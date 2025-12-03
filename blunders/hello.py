#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#%%
temp = {'x':np.linspace(0, 20, 100), 'y': np.sin(np.linspace(0, 20, 100))}

#%%
df = pd.DataFrame(temp)  # Create a list of evenly-spaced numbers over the range
plt.plot(df.x, df.y)       # Plot the sine of each x point
plt.show()

