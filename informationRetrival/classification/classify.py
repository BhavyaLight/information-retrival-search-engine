import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import string, os
import re
from lemmatization import lemmatization
import pickle
import time
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import confusion_matrix
from sklearn.externals import joblib
from sklearn import feature_extraction
from pymongo import MongoClient




class Classification(object):
    def Train(self):
        """
        Function to train data set
        """
        
        lem = lemmatization()
        #Get Mongo client
        client = MongoClient()
        db = client['IR']
        collection = db['Movies']

        #Path to folder to store trained data set
        path = os.getcwd() + "/model_files/"

        #Queries to get 500 horror, romance and crime movies
        qr1=collection.find({"genre.name":"Horror"}).limit(500)
        qr2=collection.find({"genre.name":"Romance"}).limit(500)
        qr3=collection.find({"genre.name":"Crime"}).limit(500)

        #Combine queries
        query_results=[]
        for rec in qr1:
            query_results.append(rec)
        for rec in qr2:
            query_results.append(rec)
        for rec in qr3:
            query_results.append(rec)

        #Dictionary to store the terms appearing in the genres
        dictionary = []

        #List to store category of each record
        categories = []
        
        training_data = []

        #Document ids of records to be trained
        doc_ids = []
        
        for record in query_results:
        
            training_data.append(record['overview'])
            doc_ids.append(record['_id'])
            
            for genre in record['genre']:
                if ((genre['name']=='Horror') or (genre['name']=='Romance') or (genre['name']=='Crime')):
                   categories.append(genre['name'])
                   break
            #Convert to lower case and remove stop words from overview
            dict_rec = record['overview'].lower()
            dict_rec = dict_rec.translate(string.punctuation)
            dict_rec = lem.removeStopWords(dict_rec.split(" "))

            #Add to dictionary
            if dict_rec not in dictionary:
                dictionary.extend(dict_rec)
    
        dictionary = filter(None, list(set(dictionary)))

        #Store dictionary in a file
        joblib.dump(dictionary, path + "_Genre_Dictionary")
        
        #Store doc ids of trained data in a file
        myfile = open(r'doc_ids.pkl', 'wb')
        pickle.dump(doc_ids,myfile)
        myfile.close()

        #Initialize training models
        mod_1 = SVC(kernel='linear', C=1, gamma=1)
        mod_2 = LogisticRegression()
        mod_3 = GaussianNB()
        mod_4 = MultinomialNB()
        mod_5 = BernoulliNB()

        #Ensemble classifiers
        mod_6 = RandomForestClassifier(n_estimators=50)
        mod_7 = BaggingClassifier(mod_2, n_estimators=50)
        mod_8 = GradientBoostingClassifier(loss='deviance', n_estimators=100)

        mod_9 = VotingClassifier(
            estimators=[("SVM", mod_1), ("LR", mod_2), ("Gauss", mod_3), ("Multinom", mod_4), ("Bernoulli", mod_5),
                        ("RandomForest", mod_6), ("Bagging", mod_7), ("GB", mod_8)], voting='hard')
        mod_10 = VotingClassifier(estimators=[("SVM", mod_1), ("LR", mod_2), ("Multinom", mod_4),("Bernoulli", mod_5),("Bagging",mod_7)], voting='hard',weights=[1, 2, 3, 2,1])

        #Vectorizers for feature extraction
        vec_1 = feature_extraction.text.CountVectorizer(vocabulary=dictionary)
        vec_2 = feature_extraction.text.TfidfVectorizer(vocabulary=dictionary)
        
        vec_list = [vec_1, vec_2]

        #List of training models
        model_list = [mod_1, mod_2, mod_3, mod_4, mod_5, mod_6, mod_7, mod_8, mod_9, mod_10]
        
        models_used = ["SVM", "LOGISTIC REGRESSION", "GAUSSIAN NB",
                      "MULTINOMIAL NB", "BERNOULLI NB", "RANDOM FOREST", "BAGGING", "GRADIENT",
                      "Voting", "Voting With Weights"]

        vec_used = ["COUNT VECTORIZER", "TFIDF VECTORIZER"]

        print "Starting training. This might take a while..."

        #Start training
        for model in range(0, len(model_list)):
            for vec in range(0, len(vec_list)):
                mod = model_list[model]
                vector = vec_list[vec]
                X = vector.fit_transform(training_data).toarray()
                mod.fit(X, categories)
                
                #Store in a file
                joblib.dump(mod, path + models_used[model] + "_" + vec_used[vec] + ".pkl")
                
                print models_used[model] + " " + vec_used[vec]+" finished!"
                
        print "All Done!!"
    def classification_results(self):

        # TEST DATA
        lem = lemmatization()
        #database_name = "IR"
        #collection_name = "Movies"
        client = MongoClient()
        db = client['IR']
        collection = db['Movies']
        #mysql_object = MySQL()
        #mysql_object.use_database(database_name)
        path = os.getcwd() + "/model_files/" 
        #path = "/mnt/d/info-ret/mongodb_script/information-retrival-search-engine/informationRetrival/classification/mod__files/"
        #path  = "/mnt/d/mod__files/"
        """
        regex1=re.compile('horr*|evil|blood*|spirit*|entity*|devil*|demon*|possess*|paranormal',re.IGNORECASE)
        regex2=re.compile('romanc*|romant*|love*|heart*|relationship*|',re.IGNORECASE)
        regex3=re.compile('rob*|murder*|kill*|heist|FBI|crim*|investigat*|detective*|police*',re.IGNORECASE)
        qr1=collection.find({'$and': [{"genre.name":"Horror"},{"overview":regex1}]})
        qr2=collection.find({'$and': [{"genre.name":"Romance"},{"overview":regex2}]})
        qr3=collection.find({'$and': [{"genre.name":"Crime"},{"overview":regex3}]})
        """
        trained_docs=[]
        myfile = open(r'doc_ids.pkl', 'rb')
        trained_docs=pickle.load(myfile)
        qr4=collection.find({"genre.name":"Horror"})
        qr5=collection.find({"genre.name":"Romance"})
        qr6=collection.find({"genre.name":"Crime"})
        """
        doc_ids=[]
        horr=[]
        for rec in qr1:
            doc_ids.append(rec['_id'])
        
        qr1=qr1.rewind()
        qr1=qr1.limit(75)
        for rec in qr1:
            horr.append(rec)
        """
        horr=[]
        i=0
        for rec in qr4:
            if rec['_id'] not in trained_docs:
               i=i+1
               horr.append(rec)
               
            if i>=100:
                break
        """
        qr2=qr2.rewind()
        qr2=qr2.limit(100)
        rom=[]
        for rec in qr2:
            rom.append(rec)

        doc_ids=[]
        """
        rom=[]
        i=0
        for rec in qr5:
            if rec['_id'] not in trained_docs:
               i=i+1
               rom.append(rec)
 
            if i>=100:
                break
        """
        crime=[]
        for rec in qr3:
            doc_ids.append(rec['_id'])
        
        qr3=qr3.rewind()
        qr3=qr3.limit(75)
        for rec in qr3:
            crime.append(rec)
        """
        crime=[]
        i=0
        for rec in qr6:
            if rec['_id'] not in trained_docs:
               i=i+1
               crime.append(rec)
               
            if i>=100:
                break
        
        print len(horr)
        print len(rom)
        print len(crime)
        test_data = []
        query_results=[]
        for rec in horr:
            query_results.append(rec)
        for rec in rom:
            query_results.append(rec)
        for rec in crime:
            query_results.append(rec)

        arr=[]
        test_categ = []
        for record in query_results:
            test_data.append(record['overview'])
            d={}
            d['overview']=record['overview']
            d['id']=record['_id']
            for genre in record['genre']:
                if ((genre['name']=='Horror') or (genre['name']=='Romance') or (genre['name']=='Crime')):
                   ca = genre['name']
                   d['genre']=ca
                   test_categ.append(ca)
                   break
            arr.append(d)
        """    
        f=open('test_data.tsv','w')
        for ele in arr:
            f.write((str(ele['id'])+'\t'+ele['overview']+'\t'+ele['genre']+'\n').encode('utf-8'))
        f.close()
        """
        cv_used = ["COUNT VECTORIZER", "TFIDF VECTORIZER"]
        models_used = ["SVM", "LOGISTIC REGRESSION", "GAUSSIAN NB",
                      "MULTINOMIAL NB", "BERNOULLI NB", "RANDOM FOREST", "BAGGING", "GRADIENT",
                      "Voting","Voting With Weights"]
        dict = joblib.load(path + "_Genre_Dictionary")
        cv1 = feature_extraction.text.CountVectorizer(vocabulary=dict)
        cv2 = feature_extraction.text.TfidfVectorizer(vocabulary=dict)
        cv_list = [cv1, cv2]
        result = []
        for counter_model in range(0, len(models_used)):
            for counter_cv in range(0, len(cv_used)):
                model = joblib.load(path + models_used[counter_model] + "_" + cv_used[counter_cv].replace('-', '') + ".pkl")
                cv = cv_list[counter_cv]
                Y = cv.fit_transform(test_data).toarray()
                predicted = model.predict(Y)
                
                j = 0
                horror = 0
                romance = 0
                crime = 0
                y_true = []
                y_pred = []
                for i in predicted:
                    if (test_categ[j] == "Horror"):
                        if (i == "Horror"):
                            horror += 1
                            y_pred.append(0)
                        elif (i == "Romance"):
                            y_pred.append(1)
                        else:
                            y_pred.append(2)
                        y_true.append(0)
                    elif (test_categ[j] == "Romance"):
                        if (i == "Romance"):
                            romance += 1
                            y_pred.append(1)
                        elif (i == "Horror"):
                            y_pred.append(0)
                        else:
                            y_pred.append(2)
                        y_true.append(1)
                    elif (test_categ[j] == "Crime"):
                        if (i == "Crime"):
                            crime += 1
                            y_pred.append(2)
                        elif (i == "Horror"):
                            y_pred.append(0)
                        else:
                            y_pred.append(1)
                        y_true.append(2)
                    j += 1
                score = precision_recall_fscore_support(y_true, y_pred, average='weighted')
                print("_______________________")
                print("model      :  " + models_used[counter_model])
                print("VECTORIZER :  " + cv_used[counter_cv])
                print("Horror     :  %d/100" % (horror))
                print("Romance    :  %d/100" % (romance))
                print("Crime      :  %d/100" % (crime))
                print("Precision  :  %.5f" % (score[0]))
                print("Recall     :  %.5f" % (score[1]))
                print("F(1) Score :  %.5f" % ((score[1] * score[0] / (score[1] + score[0])) * 2))
                print("F(W) Score :  %.5f" % (score[2]))
                print("Accuracy   :  %.5f" % accuracy_score(y_true, y_pred))
                #print(confusion_matrix(y_true, y_pred))
                result.append(
                     [models_used[counter_model].title(), cv_used[counter_cv][:-11], horror, romance, crime,
                      round(score[0], 3), round(score[1], 3), round(accuracy_score(y_true, y_pred), 3),
                      round(((score[1] * score[0] / (score[1] + score[0])) * 2), 3), round(score[2], 3)])
        #         print result
        joblib.dump(result, path + "classification_stats.txt")
        print "Done"
        # print result
        return result
    
    """

    def get_classification_stats(self):
        try:
            path = os.getcwd() + "/HealthNews/Classification/mod_ files/"
            stats = joblib.load(path + "classification_stats.txt")
            return stats
        except EOFError as eoferror:
            print ("Classification statistics do not exist. Creating one...")
            return self.classification_results()
        except IOError as ioerror:
            print ("Classification statistics do not exist. Creating one...")
            return self.classification_results()
    
    """
    def classify_on(self,content):
        content = content.lower()
        path = os.getcwd() + "/model_files/"
        #path = "/mnt/d/info-ret/mongodb_script/information-retrival-search-engine/informationRetrival/classification/mod__files/"
        print ("The content: ", content)
        t0 = time.clock()

        model = joblib.load(path + "Voting With Weights_TFIDF VECTORIZER" + ".pkl")
        dictionary = joblib.load(path + "_Genre_Dictionary")
        cv = feature_extraction.text.CountVectorizer(vocabulary=dictionary)
        Y = cv.fit_transform([content]).toarray()
        predicted = model.predict(Y)

        print predicted
        return predicted, str(round(time.clock() - t0, 3)) + " seconds"

c = Classification()
#c.Train()
#c.classification_results()
c.classify_on("Romance")
