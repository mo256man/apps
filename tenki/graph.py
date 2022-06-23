import numpy as np
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def make_graph():
    image = io.BytesIO()
    x = np.linspace(0, 10)
    y = np.sin(x)
    plt.plot(x, y)
    plt.savefig(image, format='png')
    image.seek(0)
    return send_file(image,
                     attachment_filename="image.png",
                     as_attachment=True)

