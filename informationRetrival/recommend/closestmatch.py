import pickle
#from unidecode import unidecode
#pkl_file = open('data.pkl', 'rb')
encoding="utf8"

overviews=pickle.load(open( "overviews.p", "rb"))
ids=pickle.load(open( "ids.p", "rb" ))
overdict=pickle.load(open( "overdict.p", "rb" ),encoding="latin-1")
iddict=pickle.load(open( "iddict.p", "rb" ))
iddictinv=pickle.load(open( "iddictinv.p", "rb" ))

cosinesim=pickle.load(open( "cosinesimilarity.p", "rb" ),encoding="latin-1")

# Function takes input as id
def findsim(i):
    
    sim=0
    maxsim=[]
    for j in iddict.keys():
        if j!=i:
            if cosinesim[(i,j)]>sim:
                sim=cosinesim[(i,j)]
                
                maxsim.append(j)
    maxsim=sorted(maxsim,reverse=True)
    #returns top 5 matching results
    return maxsim[:5]


#returning only values for iddict[:50]
x=0

for i in iddict.keys():
    if x<=50:
        print(i,findsim(i))
        x=x+1
        