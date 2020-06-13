import pdb
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import pickle
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import scale, LabelEncoder, OneHotEncoder
#from kmodes import kmodes, kprototypes
from kmodes.kmodes import KModes

#import mca
def prep_kmodes(df_):
    print("-----prep_kmodes----------")
    '''
    Prepare input dataframe for k-modes clustering.

    :param df_: dataframe to be prepared
    :returns: prepared dataframe
    '''
    df = df_.copy()
    cols_to_keep = ['gender', 'past_3_years_bike_related_purchases',
                    'job_title', 'job_industry_category', 'CustAgeBuckets',
                    'wealth_segment', 'deceased_indicator', 'owns_car', 'state',
                    'tenure', 'property_valuation', 'Giant Bicycles',
                    'Norco Bicycles', 'OHM Cycles', 'Solex', 'Trek Bicycles',
                    'WeareA2B', 'sum_profit', 'pcnt_online_tran']
    df = df[cols_to_keep]
    le = LabelEncoder()
    enc_dct = dict()
    print(df.columns)

    for col in df.columns:
        if df[col].dtype == object:
            print(col)
            df[col] = le.fit_transform(df[col])
            enc_dct[col] = le

    return df


def run_kmodes(X, init_method='Huang', n_clusters=5):
    '''
    Perform k-modes clustering.

    :param X: prepared array for clustering
    :param init_method: initiation method for k-prototypes clustering, default = 'Huang'
    :param n_clusters: number of clusters for model to segment data, default = 4
    :returns: k-modes models, array of labels
    '''
    km = KModes(n_clusters=n_clusters, n_init=10, init=init_method, verbose=1, random_state=1)
    labels = km.fit_predict(X)
    return km, labels


def plot_clusters(X, labels, n_clusters=4):
    '''
    Plot a 2-D representation of clusters.

    :param X: dimensionaly reduced feature space (i.e. array post-PCA)
    :param labels: array of labels for X
    :param n_clusters: number used to cluster input array X
    :returns: None, saved plot to 'img' folder
    '''
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    cmap = cm.get_cmap("Spectral")
    colors = cmap(labels.astype(float) / n_clusters)

    ax.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7, c=colors)
    plt.savefig('img/plotted_clusters.png'.format(n_clusters), dpi=200)
    plt.close()


