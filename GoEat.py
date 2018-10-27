#import modules
import numpy as np
import scipy
import pandas as pd
import math
import random
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.utils import shuffle
from scipy.sparse.linalg import svds
from itertools import combinations
import matplotlib.pyplot as plt
from nltk.corpus import stopwords


def smooth_user_preference(x):
    return math.log(1+x, 2)

interactions_full_df = interactions_from_selected_users_df \
                    .groupby(['userId', 'foodId'])['eventStrength'].mean() \
                    .apply(smooth_user_preference).reset_index()
print('# of unique user/item interactions: %d' % len(interactions_full_df))
interactions_full_df.head(10)


def get_items_interacted(person_id, interactions_df):
    # Get the user's data and merge in the movie information.
    interacted_items = interactions_df.loc[person_id]['foodId']
    return set(interacted_items if type(interacted_items) == pd.Series else [interacted_items])


#Top-N accuracy metrics consts

#EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS = 0

class ModelEvaluator:

    def set_random_sample_non_interacted(self,EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS):
        self.EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS = EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS


    def get_not_interacted_items_sample(self, person_id, sample_size, seed=42):
        interacted_items = get_items_interacted(person_id, interactions_full_indexed_df)
        all_items = set(food_df['foodId'])
        non_interacted_items = all_items - interacted_items

        random.seed(seed)
        non_interacted_items_sample = random.sample(non_interacted_items, sample_size)
        return set(non_interacted_items_sample)

    def _verify_hit_top_n(self, item_id, recommended_items, topn):
            try:
                index = next(i for i, c in enumerate(recommended_items) if c == item_id)
            except:
                index = -1
            hit = int(index in range(0, topn))
            return hit, index

    def evaluate_model_for_user(self, model, person_id):
        #Getting the items in test set
        interacted_values_testset = interactions_test_indexed_df.loc[person_id]
        if type(interacted_values_testset['foodId']) == pd.core.series.Series:
            person_interacted_items_testset = set(interacted_values_testset['foodId'])
        else:
            person_interacted_items_testset = set([int(interacted_values_testset['foodId'])])
        interacted_items_count_testset = len(person_interacted_items_testset)

        #Getting a ranked recommendation list from a model for a given user
        person_recs_df = model.recommend_items(person_id,
                                               items_to_ignore=get_items_interacted(person_id,
                                                                                    interactions_train_indexed_df),
                                               topn=10000000000)

        hits_at_5_count = 0
        hits_at_10_count = 0
        #For each item the user has interacted in test set
        for item_id in person_interacted_items_testset:
            #Getting a random sample (100) items the user has not interacted
            #(to represent items that are assumed to be no relevant to the user)
            non_interacted_items_sample = self.get_not_interacted_items_sample(person_id,
                                                                          sample_size=self.EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS,
                                                                          seed=item_id%(2**32)) ## seed=item_id%(2**32)
            #Combining the current interacted item with the 100 random items
            items_to_filter_recs = non_interacted_items_sample.union(set([item_id]))

            #Filtering only recommendations that are either the interacted item or from a random sample of 100 non-interacted items
            valid_recs_df = person_recs_df[person_recs_df['foodId'].isin(items_to_filter_recs)]
            valid_recs = valid_recs_df['foodId'].values
            #Verifying if the current interacted item is among the Top-N recommended items
            hit_at_5, index_at_5 = self._verify_hit_top_n(item_id, valid_recs, 5)
            hits_at_5_count += hit_at_5
            hit_at_10, index_at_10 = self._verify_hit_top_n(item_id, valid_recs, 10)
            hits_at_10_count += hit_at_10

        #Recall is the rate of the interacted items that are ranked among the Top-N recommended items,
        #when mixed with a set of non-relevant items
        recall_at_5 = hits_at_5_count / float(interacted_items_count_testset)
        recall_at_10 = hits_at_10_count / float(interacted_items_count_testset)

        person_metrics = {'hits@5_count':hits_at_5_count,
                          'hits@10_count':hits_at_10_count,
                          'interacted_count': interacted_items_count_testset,
                          'recall@5': recall_at_5,
                          'recall@10': recall_at_10}
        return person_metrics

    def evaluate_model(self, model):
        #print('Running evaluation for users')
        people_metrics = []
        for idx, person_id in enumerate(list(interactions_test_indexed_df.index.unique().values)):
            #if idx % 100 == 0 and idx > 0:
            #    print('%d users processed' % idx)
            person_metrics = self.evaluate_model_for_user(model, person_id)
            person_metrics['_person_id'] = person_id
            people_metrics.append(person_metrics)
        print('%d users processed' % idx)

        detailed_results_df = pd.DataFrame(people_metrics) \
                            .sort_values('interacted_count', ascending=False)

        global_recall_at_5 = detailed_results_df['hits@5_count'].sum() / float(detailed_results_df['interacted_count'].sum())
        global_recall_at_10 = detailed_results_df['hits@10_count'].sum() / float(detailed_results_df['interacted_count'].sum())

        global_metrics = {'modelName': model.get_model_name(),
                          'recall@5': global_recall_at_5,
                          'recall@10': global_recall_at_10}
        return global_metrics, detailed_results_df

class CFRecommender:

    MODEL_NAME = 'Collaborative Filtering'

    def __init__(self, cf_predictions_df, items_df=None):
        self.cf_predictions_df = cf_predictions_df
        self.items_df = items_df

    def get_model_name(self):
        return self.MODEL_NAME

    def recommend_items(self, user_id, items_to_ignore=[], topn=10, verbose=False):
        # Get and sort the user's predictions
        sorted_user_predictions = self.cf_predictions_df[user_id].sort_values(ascending=False) \
                                    .reset_index().rename(columns={user_id: 'recStrength'})

        # Recommend the highest predicted rating movies that the user hasn't seen yet.
        recommendations_df = sorted_user_predictions[~sorted_user_predictions['foodId'].isin(items_to_ignore)] \
                               .sort_values('recStrength', ascending = False) \
                               .head(topn)

        if verbose:
            if self.items_df is None:
                raise Exception('"items_df" is required in verbose mode')

            recommendations_df = recommendations_df.merge(self.items_df, how = 'left',
                                                          left_on = 'foodId',
                                                          right_on = 'foodId')[['recStrength', 'foodId', 'foodName']]


        return recommendations_df


def interactions_train_test_split(interactions_full_df, test_size=0.20):
    #randomise
    interactions_train_df, interactions_test_df = train_test_split(interactions_full_df,
                                   stratify=interactions_full_df['userId'],
                                   test_size=test_size)
    print('# interactions on Train set: %d' % len(interactions_train_df))
    print('# interactions on Test set: %d' % len(interactions_test_df))

    return interactions_train_df, interactions_test_df

#interactions_train_df, interactions_test_df = interactions_train_test_split(interactions_full_df, test_size=0.30)

def indexed_df(interactions_full_df,interactions_train_df,interactions_test_df):
    #Indexing by userId to speed up the searches during evaluation
    interactions_full_indexed_df = interactions_full_df.set_index('userId')
    interactions_train_indexed_df = interactions_train_df.set_index('userId')
    interactions_test_indexed_df = interactions_test_df.set_index('userId')

    return interactions_full_indexed_df, interactions_train_indexed_df, interactions_test_indexed_df

#interactions_full_indexed_df, interactions_train_indexed_df, interactions_test_indexed_df = indexed_df(interactions_full_df,interactions_train_df,interactions_test_df)

def users_items_svd(interactions_df, nfactors =15):
    #Creating a sparse pivot table with users in rows and items in columns
    users_items_pivot_matrix_df = interactions_df.pivot(index='userId',
                                                          columns='foodId',
                                                          values='eventStrength').fillna(0)

    users_items_pivot_matrix = users_items_pivot_matrix_df.values
    users_ids = list(users_items_pivot_matrix_df.index)

    #The number of factors to factor the user-item matrix.
    NUMBER_OF_FACTORS_MF = 15

    #Performs matrix factorization of the original user item matrix

    U, sigma, Vt = svds(users_items_pivot_matrix, k = NUMBER_OF_FACTORS_MF)

    sigma = np.diag(sigma)

    all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt)

    #Converting the reconstructed matrix back to a Pandas dataframe
    cf_preds_df = pd.DataFrame(all_user_predicted_ratings, columns = users_items_pivot_matrix_df.columns, index=users_ids).transpose()

    return cf_preds_df

#cf_preds_df = users_items_svd(interactions_train_df, nfactors =15)  
