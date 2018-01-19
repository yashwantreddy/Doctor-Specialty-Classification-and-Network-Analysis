import networkx as nx
import pandas as pd

def import_data(f1,f2):
    '''Import Data by entering the 2 different filepaths for the Dataframes'''
    df1 = pd.read_csv(str(f1))
    df2 = pd.read_csv(str(f2))
    return df1,df2


def transform_generate_dataframes(df1,df2):
    df2['Cardiologist'] = pd.get_dummies(df2.specialty)['Cardiology']
    df2.columns = ['physician_id','specialty','Cardiologist']
    merged = pd.merge(df1, df2, left_on='physician_id',right_on='physician_id',how='outer')
    
    indices=[]
    for i,proc in enumerate(merged.procedure):
        w=[]
        w.append(proc.replace('_', ' '))
        if 'typically' in w[0].split():
        indices.append(i)

    merged_not_typically = merged.drop(merged.index[list(indices)])
    merged_not_typically = merged_not_typically.reset_index()
    merged_not_typically.drop('index',axis=1,inplace=True)
    merged_not_typically_only_un = merged_not_typically[merged_not_typically.specialty=='Unknown']
    merged_not_typically_only_un.reset_index(drop=True, inplace=True)

    return merged_not_typically,merged_not_typically_only_un

def net_maker(df):
    procs = df.specialty.value_counts()
    procs_no_un = procs.index.drop('Unknown')
    d1= {}
    for i in range(len(procs_no_un)):
        if procs_no_un[i] not in d1.keys():
            d1[procs_no_un[i]]= list(df[df.specialty==procs_no_un[i]]['procedure_code'].unique())
    
    undirected_g = nx.Graph(d1)

    return undirected_g


def dict_generator(df,g):
    some_uns = df.unique()[:50]
    dee={}
    for un in some_uns:
        for proc in df[df.physician_id==un]['procedure_code'].values:
            if un not in dee.keys():
                dee[un] = g.neighbors(proc)
            if un in dee.keys():
                dee[un] += g.neighbors(proc)

    return dee

def master_batch_plotter(d):
    for key in d.keys():
        plt.figure(figsize=(25,15))
        plt.title('Doctor ID: {}'.format(key))
        sns_plot = sns.countplot(d[key]).get_figure()
        plt.xticks(rotation=90)
        #filename= 'Doctor_ID_{}'.format(key)
        #sns_plot.savefig(str(filename))
        #plt.show()


if __name__=="__main__":
    proc,phy = import_data('data/procedures.csv','data/physicians.csv')
    merged_not_typically,merged_not_typically_only_un = transform_generate_dataframes(proc,phy)
    undirected_g = net_maker(merged_not_typically)
    dee = dict_generator(df=merged_not_typically_only_un,g=undirected_g)
    master_batch_plotter(d=dee)



