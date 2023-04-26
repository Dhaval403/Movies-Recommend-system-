#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import ast


# In[2]:


credits = pd.read_csv('C:/Users/dhpat/OneDrive/Desktop/test jupyter/Movies Recommender System Project/tmdb_5000_credits.csv')
movies = pd.read_csv('C:/Users/dhpat/OneDrive/Desktop/test jupyter/Movies Recommender System Project/tmdb_5000_movies.csv')


# In[3]:


movies.head(1)


# In[4]:


credits.head(1)


# In[5]:


credits.head(1)['cast'].values


# In[6]:


movies.head(1)


# # merge two Data('credits','movies')

# In[7]:


movies = movies.merge(credits,on='title')


# In[8]:


movies.head(1)


# In[9]:


movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]


# In[10]:


movies.info()


# In[11]:


movies.head(1)


# # missing Data 

# In[12]:


movies.isnull().sum()


# In[13]:


movies.dropna(inplace=True)


# In[14]:


movies.duplicated().sum()


# In[15]:


movies.iloc[0].genres


# In[16]:


def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L      


# In[17]:


movies['genres'] = movies['genres'].apply(convert)


# In[18]:


movies['keywords'] = movies['keywords'].apply(convert)


# In[19]:


def convert3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L   


# In[20]:


movies['cast'] = movies['cast'].apply(convert3)


# In[21]:


movies.head(1)


# In[22]:


def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L      


# In[23]:


movies['crew'] = movies['crew'].apply(fetch_director)


# In[24]:


movies.head(1)


# In[25]:


movies['overview'] = movies['overview'].apply(lambda x:x.split())


# In[26]:


movies.head()


# In[27]:


movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","")for i in x])
movies['keywords'] =  movies['keywords'].apply(lambda x:[i.replace(" ","")for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","")for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","")for i in x])


# In[28]:


movies.head()


# In[29]:


movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']


# In[30]:


movies.head()


# In[31]:


new_df = movies[['movie_id','title','tags']]


# In[32]:


new_df.head()


# In[33]:


new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))


# In[34]:


new_df.head()


# In[35]:


new_df['tags'][0]


# In[36]:


new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())


# In[37]:


new_df.head()


# In[38]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')


# In[39]:


vectors = cv.fit_transform(new_df['tags']).toarray()


# In[40]:


vectors


# In[41]:


vectors[0]


# In[42]:


cv.get_feature_names_out()


# In[43]:


import nltk


# In[44]:


from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


# In[45]:


def stem(text):
    y = []
    
    for i in text.split():
        y.append(ps.stem(i))
        
    return " ".join(y)    


# In[46]:


stem('In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization. Action Adventure Fantasy ScienceFiction cultureclash future spacewar spacecolony society spacetravel futuristic romance space alien tribe alienplanet cgi marine soldier battle loveaffair antiwar powerrelations mindandsoul 3d SamWorthington ZoeSaldana SigourneyWeaver JamesCameron')


# In[47]:


new_df['tags'] =  new_df['tags'].apply(stem)


# In[48]:


from sklearn.metrics.pairwise import cosine_similarity


# In[49]:


similarity = cosine_similarity(vectors)


# In[50]:


similarity[1]


# In[51]:


sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]


# In[52]:


def recommend(movie):
    try:
        movie_index = new_df[new_df['title'] == movie].index[0]
    except IndexError:
        print(f"{movie} is not a valid movie title in the 'new_df' DataFrame")
        return
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    for i in movies_list:
        print(new_df.iloc[i[0]].title)


# In[53]:


recommend('Batman Begins')


# In[54]:


new_df.iloc[1216].title


# In[55]:


import pickle


# In[56]:


pickle.dump(new_df.to_dict(),open('movie_dict.pkl','wb'))  


# In[57]:


pickle.dump(similarity,open('similarity.pkl','wb'))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




