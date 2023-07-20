from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn import metrics
from sklearn.cluster import KMeans
import os

categories = ['opinion', 'business', 'world', 'us', 'arts', 'sports', 'books', 'movies']

data = load_files(container_path='text_all', categories=categories, shuffle=True,
                    encoding='utf-8', decode_error='replace')

# TODO - Data preprocessing and clustering
data_trans = Normalizer().fit_transform(TfidfTransformer(sublinear_tf=True).fit_transform(CountVectorizer(stop_words='english',max_features = 3500).fit_transform(data.data)))
clst = KMeans(n_clusters=14,random_state = 0,)
clst.fit(data_trans)

print(metrics.v_measure_score(data.target, clst.labels_))

#below is the code for the plotting of clustering results
# clusters = clst.labels_.tolist()
# labels = data.target
# colors = {0: '#FF0000', 1: '#FF7F00', 2: '#FFFF00', 3: '#00FF00', 4: '#0000FF', 5: '#000080', 6: '#8B00FF', 7: '#ff00a6', 8: '#228B22', 9: '#d4af37' , 10: '#000000', 11:'#87ceeb' , 12:'#A9A9A9' , 13:'#A52A2A' }

# pca = PCA(n_components=2).fit_transform(data_trans.toarray())
# xs, ys= pca[:, 0], pca[:, 1]
# df = pd.DataFrame(dict(x=xs, y=ys, label=clusters))
# groups = df.groupby('label')

# fig, ax = plt.subplots(figsize=(17,9))
# ax.margins(0.05)

# for idx, group in groups:
#     ax.plot(group.x, group.y, marker='o', linestyle='', ms=8, color=colors[idx], mec='none')
#     ax.set_aspect('auto')
#     ax.tick_params(
#         axis='x',
#         which='both',
#         bottom='off',
#         top='off',
#         labelbottom='off')
#     ax.tick_params(
#         axis='y',
#         which='both',
#         left='off',
#         top='off',
#         labelleft='off')
  
# plt.show()


