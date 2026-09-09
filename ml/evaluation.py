from sklearn.metrics import accuracy_score, precision_recall_fscore_support
def metrics(y_true,y_pred):
    p,r,f,_=precision_recall_fscore_support(y_true,y_pred,average='weighted',zero_division=0)
    return {'accuracy':round(accuracy_score(y_true,y_pred),4),'precision':round(p,4),'recall':round(r,4),'f1_score':round(f,4)}
