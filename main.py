#!/usr/bin/env python
# coding: utf-8

# In[9]:


from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Congratulations, it's a web app!"

@app.route("/celsius")
def fahrenheit_from(celsius):
    """Convert Celsius to Fahrenheit degrees."""
    try:
        fahrenheit = float(celsius) * 9 / 5 + 32
        fahrenheit = round(fahrenheit, 3)  # Round to three decimal places
        return str(fahrenheit)
    except ValueError:
        return "invalid input"


# In[10]:


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


# In[ ]:




