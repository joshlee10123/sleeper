#!/usr/bin/env python
# coding: utf-8

# In[4]:


from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Congratulations, it's a web app!"


# In[3]:


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


# In[ ]:




