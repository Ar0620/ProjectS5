import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(-5,5,num=100)
print (x)
y=x**2
plt.xlabel("x")
plt.plot(x,y)
plt.xlabel("y")
plt.show()

