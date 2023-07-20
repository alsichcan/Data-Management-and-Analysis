# TODO: CHANGE THIS FILE NAME TO DMA_project2_team##.py
# EX. TEAM 1 --> DMA_project2_team01.py

# TODO: IMPORT LIBRARIES NEEDED FOR PROJECT 2
import mysql.connector
import os
import surprise
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import KFold
from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn import tree
import graphviz
from mlxtend.frequent_patterns import association_rules, apriori
import csv

np.random.seed(0)

# TODO: CHANGE GRAPHVIZ DIRECTORY
#os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz2.47.1/bin/'
os.environ["PATH"] += os.pathsep + '/usr/local/Cellar/graphviz/2.47.1/bin/' # for MacOS

# TODO: CHANGE MYSQL INFORMATION, team number 
HOST = 'localhost'
USER = 'root'
PASSWORD = 'root'
SCHEMA = 'DMA_team08'
team = 8


# PART 1: Decision tree 
def part1():
    cnx = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')
    cursor.execute('USE %s;' % SCHEMA)

    # TODO: Requirement 1-1. MAKE best_item column
    cursor.execute('CREATE TABLE item ADD best_item TINYINT(1) DEFAULT 0')
    with open("best_item_list.txt", "r", encoding="utf-8") as best_item_list:
        for best_item in best_item_list:
            cursor.execute(f'UPDATE item SET best_item = 1 WHERE id = {best_item}')
            cnx.commit()

    # TODO: Requirement 1-2. WRITE MYSQL QUERY AND EXECUTE. SAVE to .csv file
    cursor.execute('''
    SELECT
    t1.id,
    t1.best_item,
    t1.ratings,
    COALESCE(t2.num_of_specs, 0) AS num_of_specs,
    COALESCE(t3.num_of_tags, 0) AS num_of_tags,
    COALESCE(t4.num_of_users, 0) AS num_of_users,
    COALESCE(t4.avg_usage_time, 0) AS avg_usage_time,
    COALESCE(t5.num_of_reviews, 0) AS num_of_reviews,
    COALESCE(t5.sum_of_recommend, 0) AS sum_of_recommend,
    COALESCE(t5.avg_review_len, 0) AS avg_review_len

    FROM
    (SELECT id, best_item, ratings FROM item) t1
    LEFT JOIN
    (SELECT item_id, COUNT(*) AS num_of_specs FROM item_specs GROUP BY item_id) t2 ON (t1.id = t2.item_id)
    LEFT JOIN
    (SELECT item_id, COUNT(*) AS num_of_tags FROM tag GROUP BY item_id) t3 ON (t1.id = t3.item_id)
    LEFT JOIN
    (SELECT item_id, COUNT(*) AS num_of_users, AVG(usagetime_total) AS avg_usage_time FROM user_item GROUP BY item_id) t4 ON (t1.id = t4.item_id)
    LEFT JOIN
    (SELECT item_id, COUNT(*) AS num_of_reviews, SUM(recommend) AS sum_of_recommend, AVG(body) AS avg_review_len FROM review GROUP BY item_id) t5 ON (t1.id = t5.item_id)
    ''')

    result = cursor.fetchall()
    with open('DMA_project2_team%02d_part1.csv' % team, 'w', encoding='utf-8') as f:
        a = csv.writer(f, delimiter=',')
        a.writerow(["id",
                    "best_item",
                    "ratings",
                    "num_of_specs",
                    "num_of_tags",
                    "num_of_users",
                    "avg_usage_time",
                    "num_of_reviews",
                    "sum_of_recommend",
                    "avg_review_len"])
        a.writerows(result)

    # TODO: Requirement 1-3. MAKE AND SAVE DECISION TREE
    # gini file name: DMA_project2_team##_part1_gini.pdf
    # entropy file name: DMA_project2_team##_part1_entropy.pdf

    data = pd.read_csv('DMA_project2_team%02d_part1.csv' % team)
    criteria = ['gini', 'entropy']

    for criterion in criteria:
        DT = tree.DecisionTreeClassifier(criterion=criterion, min_samples_leaf=10, max_depth=5)
        DT.fit(X=data.drop(["id", "best_item"], axis=1), y=data["best_item"])
        graph = tree.export_graphviz(DT,
                                     out_file=None,
                                     feature_names=['ratings',
                                                    'num_of_specs',
                                                    'num_of_tags',
                                                    'num_of_users',
                                                    'avg_usage_time',
                                                    'num_of_reviews',
                                                    'sum_of_recommend',
                                                    'avg_review_len'],
                                     class_names=['normal', 'BEST']
                                     )
        graph = graphviz.Source(graph)
        graph.render('DMA_project2_team%02d_part1_%s' % (team, criterion), view=True)

    # TODO: Requirement 1-4. Don't need to append code for 1-4

    cursor.close()
    

# PART 2: Association analysis
def part2():
    cnx = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')
    cursor.execute('USE %s;' % SCHEMA)

    # TODO: Requirement 2-1. CREATE VIEW AND SAVE to .csv file

    fopen = open('DMA_project2_team%02d_part2_bundle.csv' % team, 'w', encoding='utf-8')
    cursor.execute('''
    CREATE VIEW bundle_score AS
    SELECT bundle_id, bundle_name, num_item, num_genre, num_user, num_item + num_genre + num_user as score
    FROM
        (SELECT bundle_id, bundle_name, 100*ifnull(n_item, 0) AS num_item, 100*ifnull(n_genre, 0) AS num_genre, ifnull(n_user/ifnull(n_item,1), 0) AS num_user
        FROM
            (SELECT id as bundle_id, bundle_name FROM bundle)a
            LEFT JOIN
            (SELECT bundle_id AS id, count(item_id) AS n_item FROM bundle_item GROUP BY bundle_id)b
            ON a.bundle_id=b.id
            LEFT JOIN
            (SELECT bundle_id AS id, count(genre_id) AS n_genre FROM bundle_genre GROUP BY bundle_id)c
            ON a.bundle_id = c.id
            LEFT JOIN
            (SELECT bundle_id AS id, count(user_id) AS n_user 
            FROM 
                (bundle_item LEFT JOIN user_item ON bundle_item.item_id=user_item.item_id) 
            GROUP BY bundle_id)d
            ON a.bundle_id = d.id)x
    ORDER BY score DESC LIMIT 30
    ''')
    cursor.execute("SELECT * FROM bundle_score")
    result = cursor.fetchall()
    a = csv.writer(fopen, delimiter=',')
    a.writerows(["bundle_id, bundle_name, num_item, num_genre, num_user"])
    a.writerows(result)
    fopen.close()

    # # TODO: Requirement 2-2. CREATE 2 VIEWS AND SAVE partial one to .csv file

    fopen = open('DMA_project2_team%02d_part2_UBR.csv' % team, 'w', encoding='utf-8')
    cursor.execute('''
    CREATE VIEW user_bundle_rating AS 
    SELECT user_id as user, bundle_name as bundle, 5*ifnull(n_recommend, 0) + if(n_used<5, ifnull(n_used,0) ,5) AS rating
    FROM
        bundle_score
        LEFT JOIN
            (SELECT * FROM (SELECT b.user_id, b.bundle_id, n_used, n_recommend
            FROM
                (SELECT user_id, bundle_id, count(*) as n_used FROM bundle_item LEFT JOIN user_item ON bundle_item.item_id=user_item.item_id GROUP BY user_id, bundle_id)b
                LEFT JOIN
                (SELECT user_id, bundle_id, count(if(recommend=1, 1, null)) as n_recommend 
                FROM 
                    bundle_item 
                    LEFT JOIN
                    review
                    ON bundle_item.item_id=review.item_id GROUP BY bundle_id, user_id)c
                ON b.bundle_id=c.bundle_id AND b.user_id=c.user_id)g
            UNION
            SELECT * FROM (SELECT d.user_id, d.bundle_id, n_used, n_recommend
            FROM
                (SELECT user_id, bundle_id, count(*) as n_used FROM bundle_item LEFT JOIN user_item ON bundle_item.item_id=user_item.item_id GROUP BY user_id, bundle_id)d
                RIGHT JOIN
                (SELECT user_id, bundle_id, count(if(recommend=1, 1, null)) as n_recommend 
                FROM 
                    bundle_item 
                    LEFT JOIN
                    review
                    ON bundle_item.item_id=review.item_id GROUP BY bundle_id, user_id)e
                ON d.bundle_id=e.bundle_id AND d.user_id=e.user_id)h)k
        ON bundle_score.bundle_id=k.bundle_id
    ''')
    cursor.execute('''
    CREATE VIEW partial_user_bundle_rating AS 
    SELECT user_bundle_rating.user, user_bundle_rating.bundle, user_bundle_rating.rating 
    FROM 
        user_bundle_rating 
        INNER JOIN 
        (SELECT user FROM user_bundle_rating GROUP BY user HAVING count(*)>=20)a 
        ON user_bundle_rating.user=a.user
    ''')
    cursor.execute("SELECT * FROM partial_user_bundle_rating")
    result = cursor.fetchall()
    a = csv.writer(fopen, delimiter=',')
    a.writerow(["user", "bundle", "rating"])
    a.writerows(result)
    fopen.close()

    # TODO: Requirement 2-3. MAKE HORIZONTAL VIEW
    # file name: DMA_project2_team##_part2_horizontal.pkl
    # use to_pickle(): df.to_pickle(filename)
    df = pd.read_sql("SELECT * FROM partial_user_bundle_rating", cnx)
    bundles = pd.read_sql("SELECT bundle FROM partial_user_bundle_rating GROUP BY bundle;", cnx)
    users = pd.read_sql("SELECT user FROM partial_user_bundle_rating GROUP BY user;", cnx)
    horizontal_df = pd.DataFrame(0, index=users['user'], columns=bundles['bundle'])
    for bundleNuser in df[['bundle', 'user']].values:
        bundle = bundleNuser[0]
        user = bundleNuser[1]
        horizontal_df.loc[user, bundle] = 1
    horizontal_df.to_pickle("DMA_project2_team%02d_part2_horizontal.pkl" % team)

    # TODO: Requirement 2-4. ASSOCIATION ANALYSIS
    # filename: DMA_project2_team##_part2_association.pkl (pandas dataframe)
    df = pd.read_pickle("DMA_project2_team%02d_part2_horizontal.pkl" % team)
    freq_itemsets = apriori(df.astype('bool'), min_support=0.35, use_colnames=True)
    freq_itemsets.to_pickle("freq_itemsets.pkl")
    freq_itemsets = pd.read_pickle("freq_itemsets.pkl")
    rules = association_rules(freq_itemsets, metric='lift', min_threshold=2)
    rules.to_pickle("DMA_project2_team%02d_part2_association.pkl" % team)

    cursor.close()



# TODO: Requirement 3-1. WRITE get_top_n
def get_top_n(algo, testset, id_list, n, user_based=True):
    results = defaultdict(list)
    if user_based:
        # TODO: testset의 데이터 중에 user id가 id_list 안에 있는 데이터만 따로 testset_id로 저장
        # Hint: testset은 (user_id, bundle_name, default_rating)의 tuple을 요소로 갖는 list
        testset_id = []

        for i in range(len(testset)):
            for j in id_list :
                if (str(testset[i][0]) == j) :
                    testset_id.append(testset[i])

        predictions = algo.test(testset_id)
        for uid, bname, true_r, est, _ in predictions:
            # TODO: results는 user_id를 key로, [(bundle_name, estimated_rating)의 tuple이 모인 list]를 value로 갖는 dictionary
            results[uid].append((bname,est))
    else:
        # TODO: testset의 데이터 중 bundle name이 id_list 안에 있는 데이터만 따로 testset_id라는 list로 저장
        # Hint: testset은 (user_id, bundle_name, default_rating)의 tuple을 요소로 갖는 list
        testset_id = []

        for i in range(len(testset)):
            for j in id_list :
                if(str(testset[i][1]) == j) :
                    testset_id.append(testset[i])

        predictions = algo.test(testset_id)
        for uid, bname, true_r, est, _ in predictions:
            # TODO: results는 bundle_name를 key로, [(user_id, estimated_rating)의 tuple이 모인 list]를 value로 갖는 dictionary
            results[bname].append((uid,est))

    for id_, ratings in results.items():
        # TODO: rating 순서대로 정렬하고 top-n개만 유지
        ratings.sort(key=lambda x: x[1], reverse = True)
        results[id_] = ratings[:n]

    return results


# PART 3. Requirement 3-2, 3-3, 3-4
def part3():
#    file_path = 'DMA_project2_team%02d_part2_UBR.csv' % team
#    reader = Reader(line_format='user item rating', sep=',', rating_scale=(1, 10), skip_lines=1)
#    data = Dataset.load_from_file(file_path, reader=reader)
    file_path = 'DMA_project2_team%02d_part2_UBR.csv' % team
    df = pd.read_csv(file_path)
    reader = Reader(line_format='user item rating', sep=',', rating_scale=(1, 10), skip_lines=1)
    data = Dataset.load_from_df(df, reader=reader)

    trainset = data.build_full_trainset()
    testset = trainset.build_anti_testset()

    # TODO: Requirement 3-2. User-based Recommendation
    uid_list = ['8051826169', '8027368512', '7998746368', '8054453794', '8030770479']
     # TODO: set algorithm for 3-2-1
     sim_options = {'name':'cosine','user_based':True}
     algo = surprise.KNNBasic(sim_options = sim_options)
     algo.fit(trainset)
     results = get_top_n(algo, testset, uid_list, n=5, user_based=True)
     with open('3-2-1.txt', 'w') as f:
         for uid, ratings in sorted(results.items(), key=lambda x: x[0]):
             f.write('User ID %s top-5 results\n' % uid)
             for bname, score in ratings:
                 f.write('Bundle NAME %s\n\tscore %s\n' % (bname, str(score)))
             f.write('\n')
    
     # TODO: set algorithm for 3-2-2
     sim_options = {'name':'Pearson','user_based':True}
     algo = surprise.KNNWithMeans(sim_options = sim_options)
     algo.fit(trainset)
     results = get_top_n(algo, testset, uid_list, n=5, user_based=True)
     with open('3-2-2.txt', 'w') as f:
         for uid, ratings in sorted(results.items(), key=lambda x: x[0]):
             f.write('User ID %s top-5 results\n' % uid)
             for bname, score in ratings:
                 f.write('Bundle NAME %s\n\tscore %s\n' % (bname, str(score)))
             f.write('\n')

    # TODO: 3-2-3. Best Model
    kf = KFold(n_splits = 5, random_state= 0)
    acc=[]

    algos = []

    sim_options = [
        {'name':'cosine','user_based':True},
        {'name':'pearson','user_based':True},
        {'name':'msd','user_based':True},
        {'name':'pearson_baseline','user_based':True}
    ]

    bsl_options = [
        {'method': 'als','n_epochs': 10,'reg_u': 15,'reg_i': 10},
        {'method': 'als','n_epochs': 20,'reg_u': 15,'reg_i': 10},
        {'method': 'sgd','n_epochs': 20,'learning_rate':0.005},
        {'method': 'sgd','n_epochs': 20,'learning_rate':0.0005},
    ]

    for sim_option in sim_options:
        algos.append(surprise.KNNBasic(sim_options=sim_option, verbose=False))
        algos.append(surprise.KNNWithMeans(sim_options=sim_option, verbose=False))
        algos.append(surprise.KNNWithZScore(sim_options=sim_option, verbose=False))
        for bsl_option in bsl_options:
            algos.append(surprise.KNNBaseline(sim_options=sim_option, bsl_options=bsl_option, verbose=False))

    for algo in algos:
        temp = []
        for i, (trainset, testset) in enumerate(kf.split(data)):
            algo.fit(trainset)
            predictions = algo.test(testset)
            temp.append(surprise.accuracy.rmse(predictions))
        acc.append(np.mean(temp))
    
    best_algo_ub = algos[acc.index(min(acc))]

    print("-" * 50)
    print("Best Model for User-based Recommendation : ")
    print(best_algo_ub.__class__, best_algo_ub.sim_options, best_algo_ub.bsl_options)
    print("MIN RMSE : ", min(acc))
    print("-" * 50)

    # TODO: Requirement 3-3. Item-based Recommendation
    bname_list = ['World of Magicka Bundle',
                  'Borderlands Triple Pack',
                  'Tripwire Complete Bundle',
                  'Grand Theft Auto V & Great White Shark Cash Card',
                  'Killing Floor 1 Complete Your Set!']
     # TODO - set algorithm for 3-3-1
     sim_options = {'name':'cosine','user_based':False}
     algo = surprise.KNNBasic(sim_options = sim_options)
     algo.fit(trainset)
     results = get_top_n(algo, testset, bname_list, n=10, user_based=False)
     with open('3-3-1.txt', 'w') as f:
         for bname, ratings in sorted(results.items(), key=lambda x: x[0]):
             f.write('Bundle NAME %s top-10 results\n' % bname)
             for uid, score in ratings:
                 f.write('User ID %s\n\tscore %s\n' % (uid, str(score)))
             f.write('\n')
    
     # TODO: set algorithm for 3-3-2
     sim_options = {'name':'Pearson','user_based':False}
     algo = surprise.KNNWithMeans(sim_options = sim_options)
     algo.fit(trainset)
     results = get_top_n(algo, testset, bname_list, n=10, user_based=False)
     with open('3-3-2.txt', 'w') as f:
         for bname, ratings in sorted(results.items(), key=lambda x: x[0]):
             f.write('Bundle NAME %s top-10 results\n' % bname)
             for uid, score in ratings:
                 f.write('User ID %s\n\tscore %s\n' % (uid, str(score)))
             f.write('\n')

    # TODO: 3-3-3. Best Model
    acc=[]

    algos = []

    sim_options = [
        {'name':'cosine','user_based':False},
        {'name':'pearson','user_based':False},
        {'name':'msd','user_based':False},
        {'name':'pearson_baseline','user_based':False}
    ]

    bsl_options = [
        {'method': 'als','n_epochs': 10,'reg_u': 15,'reg_i': 10},
        {'method': 'als','n_epochs': 20,'reg_u': 15,'reg_i': 10},
        {'method': 'sgd','n_epochs': 20,'learning_rate':0.005},
        {'method': 'sgd','n_epochs': 20,'learning_rate':0.0005},
    ]

    for sim_option in sim_options:
        algos.append(surprise.KNNBasic(sim_options=sim_option, verbose=False))
        algos.append(surprise.KNNWithMeans(sim_options=sim_option, verbose=False))
        algos.append(surprise.KNNWithZScore(sim_options=sim_option, verbose=False))
        for bsl_option in bsl_options:
            algos.append(surprise.KNNBaseline(sim_options=sim_option, bsl_options=bsl_option, verbose=False))

    for algo in algos:
        temp = []
        for i, (trainset, testset) in enumerate(kf.split(data)):
            algo.fit(trainset)
            predictions = algo.test(testset)
            temp.append(surprise.accuracy.rmse(predictions))
        acc.append(np.mean(temp))


    print("-" * 50)
    print("Best Model for Item-based Recommendation : ")
    best_algo_ib = algos[acc.index(min(acc))]
    print(best_algo_ib.__class__, best_algo_ib.sim_options, best_algo_ib.bsl_options)
    print("RMSE : ", min(acc))
    print("-" * 50)

# TODO: Requirement 3-4. Matrix-factorization Recommendation
     # TODO: set algorithm for 3-4-1
     algo = surprise.SVD(n_factors=100, n_epochs=50, biased=False)
     algo.fit(trainset)
     results = get_top_n(algo, testset, uid_list, n=5, user_based=True)
     with open('3-4-1.txt', 'w') as f:
         for uid, ratings in sorted(results.items(), key=lambda x: x[0]):
             f.write('User ID %s top-5 results\n' % uid)
             for bname, score in ratings:
                 f.write('Bundle NAME %s\n\tscore %s\n' % (bname, str(score)))
             f.write('\n')
    
     # TODO: set algorithm for 3-4-2
     algo = surprise.SVD(n_factors=200, n_epochs=100, biased=True)
     algo.fit(trainset)
     results = get_top_n(algo, testset, uid_list, n=5, user_based=True)
     with open('3-4-2.txt', 'w') as f:
         for uid, ratings in sorted(results.items(), key=lambda x: x[0]):
             f.write('User ID %s top-5 results\n' % uid)
             for bname, score in ratings:
                 f.write('Bundle NAME %s\n\tscore %s\n' % (bname, str(score)))
             f.write('\n')
    
     # TODO: set algorithm for 3-4-3
     algo = surprise.SVDpp(n_factors=100, n_epochs=50)
     algo.fit(trainset)
     results = get_top_n(algo, testset, uid_list, n=5, user_based=True)
     with open('3-4-3.txt', 'w') as f:
         for uid, ratings in sorted(results.items(), key=lambda x: x[0]):
             f.write('User ID %s top-5 results\n' % uid)
             for bname, score in ratings:
                 f.write('Bundle NAME %s\n\tscore %s\n' % (bname, str(score)))
             f.write('\n')
    
     # TODO: set algorithm for 3-4-4
     algo = surprise.SVDpp(n_factors=100, n_epochs=100)
     algo.fit(trainset)
     results = get_top_n(algo, testset, uid_list, n=5, user_based=True)
     with open('3-4-4.txt', 'w') as f:
         for uid, ratings in sorted(results.items(), key=lambda x: x[0]):
             f.write('User ID %s top-5 results\n' % uid)
             for bname, score in ratings:
                 f.write('Bundle NAME %s\n\tscore %s\n' % (bname, str(score)))
             f.write('\n')

    # TODO: 3-4-5. Best Model
    acc=[]

    algos = []

    for n_factor in [100, 200]:
        for n_epoch in [50, 100, 150]:
            for bias in [False, True]:
                algos.append(surprise.SVD(n_factors=n_factor, n_epochs=n_epoch, biased=bias, verbose=False))
            algos.append(surprise.SVDpp(n_factors=n_factor, n_epochs=n_epoch, verbose=False))
            algos.append(surprise.NMF(n_factors=n_factor, n_epochs=n_epoch, verbose=False))

    for algo in algos :
        temp = []
        for i, (trainset, testset) in enumerate(kf.split(data)):
            algo.fit(trainset)
            predictions = algo.test(testset)
            temp.append(surprise.accuracy.rmse(predictions))
        acc.append(np.mean(temp))

    print("-" * 50)
    print("Best Model for Matrix-factorization Recommendation : ")
    best_algo_mf = algos[acc.index(min(acc))]
    print(best_algo_mf.__class__, best_algo_mf.n_factors, best_algo_mf.n_epochs, best_algo_mf.biased)
    print("RMSE: ", min(acc))
    print("-" * 50)

if __name__ == '__main__':
    part1()
    part2()
    part3()
    




