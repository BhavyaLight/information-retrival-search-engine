from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.externals import joblib
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn import feature_extraction
from pymongo import MongoClient
import string, os
import re
from lemmatization import lemmatization
#from HealthNews.Utility.MySQL import MySQL
import time


class classify(object):
    def train_data(self):
        lem = lemmatization()
        client = MongoClient()
        db = client['IR']
        collection = db['Movies']
        #path = os.getcwd() + "/model_files/"
        path = "/mnt/d/info-ret/mongodb_script/information-retrival-search-engine/informationRetrival/classification/model_files/"

        regex1=re.compile('horr*|evil|blood*|spirit*|entity*|devil*|demon*|possess*|paranormal',re.IGNORECASE)
        regex2=re.compile('romanc*|romant*|love*|heart*|relationship*|',re.IGNORECASE)
        regex3=re.compile('rob*|murder*|kill*|heist|FBI|crim*|investigat*|detective*|police*',re.IGNORECASE)
        
        query_results = collection.find({'$or': [{'$and': [{"genre.name":"Horror"},{"overview":regex1}]},{'$and': [{"genre.name":"Romance"},{"overview":regex2}]},{'$and': [{"genre.name":"Crime"},{"overview":regex3}]}]})
        ite=0
        dict = []
        categ = []
        train = []
        for record in query_results:
        
            train.append(record['overview'])
            for genre in record['genre']:
                if ((genre['name']=='Horror') or (genre['name']=='Romance') or (genre['name']=='Crime')):
                   ca = genre['name']
                   categ.append(ca)
                   break

            d = record['overview'].lower()
            d = d.translate(string.punctuation)
            d = lem.removeStopWords(d.split(" "))
            if d not in dict:
                dict.extend(d)
            ite=ite+1
        dict = filter(None, list(set(dict)))
        
        model1 = SVC(kernel='linear', C=1, gamma=1)
        model2 = LogisticRegression()
        model3 = GaussianNB()
        model4 = MultinomialNB()
        model5 = BernoulliNB()
        model6 = RandomForestClassifier(n_estimators=50)
        model7 = BaggingClassifier(model2, n_estimators=50)
        model8 = GradientBoostingClassifier(loss='deviance', n_estimators=100)
        model9 = VotingClassifier(
            estimators=[("SVM", model1), ("LR", model2), ("Gauss", model3), ("Multinom", model4), ("Bernoulli", model5),
                        ("RandomForest", model6), ("Bagging", model7), ("GB", model8)], voting='hard')
        model10 = VotingClassifier(estimators=[("SVM", model1), ("LR", model2), ("Gauss", model3),("RandomForest", model6)], voting='hard',weights=[1, 1, 2, 2])

        cv1 = feature_extraction.text.CountVectorizer(vocabulary=dict)
        cv2 = feature_extraction.text.TfidfVectorizer(vocabulary=dict)
        cv_list = [cv1, cv2]
        #model_list = [model1, model2, model3, model4, model5, model6, model7, model8, model9, model10]
        model_list = [model10]
        model_used = ["SVM", "LOGISTIC REGRESSION", "GAUSSIAN NB",
                      "MULTINOMIAL NB", "BERNOULLI NB", "RANDOM FOREST", "BAGGING", "GRADIENT",
                      "Voting", "Voting With Weights"]
        #model_used = ["Voting With Weights"]
        cv_used = ["COUNT VECTORIZER", "TFIDF VECTORIZER"]

        joblib.dump(dict, path + "DICTIONARY")
        print ite
        print len(categ)
        print "Training..."
        for counter_model in range(0, len(model_list)):
            for counter_cv in range(0, len(cv_list)):
                model = model_list[counter_model]
                cv = cv_list[counter_cv]
                X = cv.fit_transform(train).toarray()
                
                model.fit(X, categ)
                joblib.dump(model, path + model_used[counter_model] + "_" + cv_used[
                    counter_cv] + ".pkl")  # Save as file
                print model_used[counter_model] + " done."
    
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
        #path = os.getcwd() + "/model_files/" 
        path = "/mnt/d/info-ret/mongodb_script/information-retrival-search-engine/informationRetrival/classification/model_files/"

        regex1=re.compile('horr*|evil|blood*|spirit*|entity*|devil*|demon*|possess*|paranormal',re.IGNORECASE)
        regex2=re.compile('romanc*|romant*|love*|heart*|relationship*|',re.IGNORECASE)
        regex3=re.compile('rob*|murder*|kill*|heist|FBI|crim*|investigat*|detective*|police*',re.IGNORECASE)
        qr1=collection.find({'$and': [{"genre.name":"Horror"},{"overview":regex1}]})
        qr2=collection.find({'$and': [{"genre.name":"Romance"},{"overview":regex2}]})
        qr3=collection.find({'$and': [{"genre.name":"Crime"},{"overview":regex3}]})
        qr4=collection.find({"genre.name":"Horror"})
        qr5=collection.find({"genre.name":"Romance"})
        qr6=collection.find({"genre.name":"Crime"})
        doc_ids=[]
        horr=[]
        for rec in qr1:
            doc_ids.append(rec['_id'])
        qr1=qr1.rewind()
        qr1=qr1.limit(75)
        for rec in qr1:
            horr.append(rec)
            
        i=0
        for rec in qr4:
            if rec['_id'] not in doc_ids:
                i=i+1
                horr.append(rec)
            if i>=25:
                break
        qr2=qr2.rewind()
        qr2=qr2.limit(100)
        rom=[]
        for rec in qr2:
            rom.append(rec)

        doc_ids=[]
        crime=[]
        for rec in qr3:
            doc_ids.append(rec['_id'])
        qr3=qr3.rewind()
        qr3=qr3.limit(75)
        for rec in qr3:
            crime.append(rec)
            
        i=0
        for rec in qr6:
            if rec['_id'] not in doc_ids:
                i=i+1
                crime.append(rec)
            if i>=25:
                break
        
        
        test_data = []
        query_results=[]
        for rec in horr:
            query_results.append(rec)
        for rec in rom:
            query_results.append(rec)
        for rec in crime:
            query_results.append(rec)


        test_categ = []
        for record in query_results:
            test_data.append(record['overview'])
            for genre in record['genre']:
                if ((genre['name']=='Horror') or (genre['name']=='Romance') or (genre['name']=='Crime')):
                   ca = genre['name']
                   test_categ.append(ca)
                   break

        
        cv_used = ["COUNT VECTORIZER", "TFIDF VECTORIZER"]
        model_used = ["SVM", "LOGISTIC REGRESSION", "GAUSSIAN NB",
                      "MULTINOMIAL NB", "BERNOULLI NB", "RANDOM FOREST", "BAGGING", "GRADIENT",
                      "Voting","Voting With Weights"]
        dict = joblib.load(path + "DICTIONARY")
        cv1 = feature_extraction.text.CountVectorizer(vocabulary=dict)
        cv2 = feature_extraction.text.TfidfVectorizer(vocabulary=dict)
        cv_list = [cv1, cv2]
        result = []
        for counter_model in range(0, len(model_used)):
            for counter_cv in range(0, len(cv_used)):
                model = joblib.load(path + model_used[counter_model] + "_" + cv_used[counter_cv].replace('-', '') + ".pkl")
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
                print("MODEL      :  " + model_used[counter_model])
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
                     [model_used[counter_model].title(), cv_used[counter_cv][:-11], horror, romance, crime,
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
            path = os.getcwd() + "/HealthNews/Classification/model files/"
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
        #path = os.getcwd() + "/model_files/"
        path = "/Users/bhavyachandra/Desktop/model_files/"
        print ("The content: ", content)
        t0 = time.clock()

        model = joblib.load(path + "GAUSSIAN NB_COUNT VECTORIZER" + ".pkl")
        dict = joblib.load(path + "DICTIONARY")
        cv = feature_extraction.text.CountVectorizer(vocabulary=dict)
        Y = cv.fit_transform([content]).toarray()
        predicted = model.predict(Y)

        print predicted
        return predicted, str(round(time.clock() - t0, 3)) + " seconds"

# c = classify()
#c.train_data()
#c.classification_results()
# c.classify_on("Fifteen years after murdering his sister on Halloween night 1963, Michael Myers escapes from a mental hospital and returns to the small town of Haddonfield to kill again.")

