from flask import Flask,render_template,request,redirect
from flask import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn.decomposition import TruncatedSVD
app = Flask(__name__)
collaborative_dict = dict()
content_dict= dict()
sametype_dict= dict()
samebrand_dict= dict()
import pickle
@app.route('/')
def hello():
    q = request.args['q']
    q=int(q)
    with open('user.pkl', 'rb') as handle:
        collaborative_dict = pickle.load(handle)
    with open('user_content.pkl', 'rb') as handle:
        content_dict = pickle.load(handle)
    ans=0
    content_based=0
    if q in collaborative_dict.keys():
        ans= collaborative_dict[q]
        print("inside if")
    if q in content_dict.keys():
        content_based= content_dict[q]
    print(ans,content_based)
    print(type(ans))
    if type(ans) is list and type(content_based) is list:
        print("hehe\n\n\n\n\n")
        return jsonify({'collaborative':ans,"similar_product_content_based": content_based})
    


    data=pd.read_csv("C://Users//arjun//Desktop//hackathon//hack.csv")
    # print(data[data["product_id"]==463570586]["brand"])
    group= pd.read_csv("C://Users//arjun//Desktop//hackathon//content_utility_data")
    print("group data found")
    content_df= pd.read_csv("C://Users//arjun//Desktop//hackathon//newcontentresult")
    sample = content_df[content_df['user_id']==515125723].sort_values(by='predicted_interaction',ascending=False).merge(group[['product_id','category_code','brand','price','price_category']].drop_duplicates('product_id'),on='product_id')[:10]
    rem=sample["product_id"]
    mybrand=sample["brand"][0]
    mycategory=sample["category_code"][0]
    other_brand= sample["brand"].unique()
    sim_brand= sample[sample["brand"] == mybrand]
    sim_product= sample[sample["category_code"] == mycategory]
    sim_brand_product_id= list(sim_brand["product_id"])
    sim_product_product_id= list(sim_product["product_id"])
    
    print("halfway there")







    temp=pd.read_csv("C://Users//arjun//Desktop//hackathon//collaborative_newdataset.csv")
    
    amazon_ratings1 = temp.head(10000)
    ratings_utility_matrix = amazon_ratings1.pivot_table(values='Rating', index='UserId', columns='ProductId', fill_value=0)    #slowest step
    # print(ratings_utility_matrix)
    X = ratings_utility_matrix.T
    X1 = X
    SVD = TruncatedSVD(n_components=10)
    decomposed_matrix = SVD.fit_transform(X)
    correlation_matrix = np.corrcoef(decomposed_matrix)
    print("before i")
    i=temp[temp["UserId"]==q]["ProductId"].iloc[0]
    print("after i")
    product_names = list(X.index)
    product_ID = product_names.index(i)
    correlation_product_ID = correlation_matrix[product_ID]
    Recommend = list(X.index[correlation_product_ID > 0.90])

# Removes the item already bought by the customer
    Recommend.remove(i) 
    # print(Recommend)
    result=Recommend[0:9]
    ans=[]
    # print("before i for loop")
    # print(temp)
    for i in result:
        if isinstance(data[data["product_id"]==i]["brand"].iloc[0],float):
            ans.append([i,temp[temp["ProductId"]==i]["category_code"].iloc[0],temp[temp["ProductId"]==i]["Price"].iloc[0],"New Brand"])
        else:
            ans.append([i,temp[temp["ProductId"]==i]["category_code"].iloc[0],temp[temp["ProductId"]==i]["Price"].iloc[0],data[data["product_id"]==i]["brand"].iloc[0]])
    print("after i for loop")
    similar_brand_products=[]
    similar_product_content_based=[]
    # print(temp.head())
    for i in sim_brand_product_id:
        if isinstance(data[data["product_id"]==i]["brand"].iloc[0],float):
            similar_brand_products.append([i,temp[temp["ProductId"]==i]["category_code"].iloc[0],temp[temp["ProductId"]==i]["Price"].iloc[0],"New Brand"])
        else:
            similar_brand_products.append([i,temp[temp["ProductId"]==i]["category_code"].iloc[0],temp[temp["ProductId"]==i]["Price"].iloc[0],data[data["product_id"]==i]["brand"].iloc[0]])
    
    
    for i in sim_product_product_id:
        if isinstance(data[data["product_id"]==i]["brand"].iloc[0],float):
            similar_product_content_based.append([i,temp[temp["ProductId"]==i]["category_code"].iloc[0],temp[temp["ProductId"]==i]["Price"].iloc[0],"New Brand"])
        else:
            similar_product_content_based.append([i,temp[temp["ProductId"]==i]["category_code"].iloc[0],temp[temp["ProductId"]==i]["Price"].iloc[0],data[data["product_id"]==i]["brand"].iloc[0]])
    
    collaborative_dict[q]= ans
    content_dict[q]=  similar_product_content_based
    with open('user.pkl', 'wb') as handle:
        pickle.dump(collaborative_dict, handle)
    
    with open('user_content.pkl', 'wb') as handle:
        pickle.dump(content_dict, handle)


    return jsonify({'collaborative':ans,"similar_product_content_based": similar_product_content_based})

@app.route('/samebrand/')
def samebrand():
    q = request.args['q']
    q=int(q)
    print(type(q))
    with open('samebrand.pkl', 'rb') as handle:
        print("opened file")
        samebrand_dict = pickle.load(handle)
    if q in samebrand_dict.keys():
        val= samebrand_dict[q]
        print("hehe")
        return jsonify({"result": val})
    
    data= pd.read_csv("C://Users//arjun//Desktop//hackathon//hack.csv")
    mybrand= data[data["product_id"]==q]["brand"].iloc[0]
    res= data[data["brand"]==mybrand][["category_code"]]
    ids= data[data["brand"]==mybrand][["product_id"]]
    prices= data[data["brand"]==mybrand][["price"]]
    val=[]
    for i in range(5):
        val.append([res.iloc[i][0],int(ids.iloc[i][0]),int(prices.iloc[i][0]),mybrand])
    # print(ids)
    # print(res)
    # print(res.iloc[1])
    ans=[]
    newans=[]
    # print(res.values)
    n=len(res)

    # print(ans)  
    print("about to save")
    samebrand_dict[q]= val
    with open('samebrand.pkl', 'wb') as handle:
        pickle.dump(samebrand_dict, handle)

    return jsonify({"result": val})

@app.route('/sametype/')
def sametype():
    q = request.args['q']
    q=int(q)
    
    print(type(q))
    with open('sametype.pkl', 'rb') as handle:
        print("opened file")
        sametype_dict = pickle.load(handle)
    if q in sametype_dict.keys():
        val= sametype_dict[q]
        print("hehe")
        return jsonify({"result": val})
    data= pd.read_csv("C://Users//arjun//Desktop//hackathon//hack.csv")
    mytype= data[data["product_id"]==q]["category_code"].iloc[0]
    res= data[data["category_code"]==mytype][["brand"]]
    ids= data[data["category_code"]==mytype][["product_id"]]
    prices= data[data["category_code"]==mytype][["price"]]
    val=[]
    n=5
    if len(ids)>n:
        pass
    else:
        n=len(ids)
    for i in range(n):
        val.append([res.iloc[i][0],int(ids.iloc[i][0]),int(prices.iloc[i][0]),mytype])
    # print(ids)
    # for i in ids:
    #     print(i)
    # print(res)
    # print(res.values)
    
    # for i in range(5):
    #     temp=list([res.iloc[i],temp10[0]])
    #     # 
        
    #     ans.append(temp)
    print("about to save")
    sametype_dict[q]= val
    with open('sametype.pkl', 'wb') as handle:
        pickle.dump(sametype_dict, handle)

    return jsonify({"result": val})
if __name__ == '__main__':
    app.run(debug=True)
