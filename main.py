#!/usr/bin/env python
# coding: utf-8

# In[11]:


from flask import Flask
from sleeper_wrapper import League, User
import pandas as pd
from pandas.io.json import json_normalize

app = Flask(__name__)

@app.route("/")
def index():
    # call in League ID
    League = League(650030921247977472)
    
    # get users, rosters, playoffs
    rosters = League.get_rosters()
    users = League.get_users()
    standings = League.get_standings(rosters,users)
    playoffs = League.get_playoff_winners_bracket()
    
    # normalize JSON format to df
    playoffs_df = pd.json_normalize(playoffs)
    users_df = pd.json_normalize(users)
    rosters_df = pd.json_normalize(rosters)
    
    # clean users df
    users_df_cleaned = users_df[['user_id','display_name']]
    users_df_cleaned = users_df_cleaned.drop([4])
    
    # clean rosters df
    rosters_df_cleaned = rosters_df[['roster_id','starters','players','owner_id']]
    
    # merge rosters and users to match roster_id to username
    final_users_df = pd.merge(left=users_df_cleaned, right=rosters_df_cleaned, how='left', left_on='user_id', right_on='owner_id')
    final_users_df['roster_id'] = final_users_df['roster_id'].astype(int)
    
    # create empty playoffs df
    final_playoffs_df = pd.DataFrame()
    
    # create xlookup function
    def xlookup(lookup_value, lookup_array, return_array, if_not_found:str = ''):
        match_value = return_array.loc[lookup_array == lookup_value]
        if match_value.empty:
            return f'"{lookup_value}" not found!' if if_not_found == '' else if_not_found
        else:
            return match_value.tolist()[0]
        
    # fill final playoffs df
    final_playoffs_df['round'] = ['wc','wc','semis','semis','5th place match','finals','3rd place match']
    final_playoffs_df['home'] = playoffs_df['t1'].apply(xlookup, args=(final_users_df['roster_id'],
                                                                                   final_users_df['display_name']))
    final_playoffs_df['away'] = playoffs_df['t2'].apply(xlookup, args=(final_users_df['roster_id'],
                                                                                   final_users_df['display_name']))
    final_playoffs_df['winner'] = playoffs_df['w'].apply(xlookup, args=(final_users_df['roster_id'],
                                                                                   final_users_df['display_name']))
    final_playoffs_df['loser'] = playoffs_df['l'].apply(xlookup, args=(final_users_df['roster_id'],
                                                                                   final_users_df['display_name']))
    
    # extract finals matchup
    finals_df = final_playoffs_df.loc[final_playoffs_df['round'] == 'finals']
    
    # create long term standings table
    long_term_pool_standings = final_users_df[['display_name','roster_id']]
    long_term_pool_standings['count'] = 0
    
    # create winners list
    winners = ['kelvinsava10']
    
    # increment long term pool standings with winners
    long_term_pool_standings.loc[long_term_pool_standings.display_name.isin(winners), 'count'] += 1    
    
    # display in sorted fashion
    display = long_term_pool_standings.sort_values('count', ascending=False)
    
    return display

#@app.route("/<celsius>")
#def fahrenheit_from(celsius):
#    """Convert Celsius to Fahrenheit degrees."""
#    try:
#        fahrenheit = float(celsius) * 9 / 5 + 32
#        fahrenheit = round(fahrenheit, 3)  # Round to three decimal places
#        return str(fahrenheit)
#    except ValueError:
#        return "invalid input"


# In[10]:


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


# In[ ]:




