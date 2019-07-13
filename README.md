# Books2Movies
项目描述：
我们希望发现一种新的电影分类方式——基于观众的喜好来分类。我们选取豆瓣的用户作为电影的观众，以阅读的书籍作为观众的偏好依据。我们将在以阅读书籍为参考的用户图上运行社区发现算法，从而将观众分类。然后对每一个社区的电影喜好进行整合，形成每个社区的偏好。最后用每个社区的偏好为依据构建电影图并进行新的社区发现，从而发现不同电影之间的隐藏联系。

预期结果：
同类的电影应该会被同一类人所喜爱，因此，统一社区的人应该喜欢同一类型的电影。所以在电影社区中，大多数的电影应该属于同一类型。同时，由于一些电影是深受广大群众喜欢的，所以不同的社区的交集会形成一个中心区，代表最受欢迎的电影。

数据集：
我们在GitHub上找到了一份关于豆瓣电影评论的数据集，其中包含大约%条数据，同时，我们也通过网络数据爬虫获取了豆瓣书籍的TOP250榜单的评论及其用户。经过筛选，获得了%条有效的用户信息。最终形成的数据集包含：用户的名称，用户在书籍TOP250榜单中评论的书籍，和用户在电影TOP250榜单上观看过的电影。

Project description
We hope to create a new method to classify movies, that is, according to the audience’s preferences.  We decide to choose the users of Douban as our sample of movie audience and select the books they read as the representation of audiences' preferences.  We will run Community Detection on the User Graph with the books as reference, so as to classify the audience.  By using this graph, we are able to integrate each community’s taste of movies.  Finally, we will build the Movie Graph based on the preferences of each community.  Then we can then run a new Community Detection on this graph, so as to discover the hidden relationship between different movies.

Dataset & Subclasses
We found a data set on GitHub about Douban Movie Comments, which contains about % record. We also got the comments and users of the TOP250 list of Douban Books through the web data crawler. After screening, we get % valid user information. The final data set consists of the user's name, the book that the user reviews in the book TOP250 list, and the movie that the user has watched on the movie TOP250 list.

Expected Analysis Results
Similar movies should be liked by the same kind of people, so people in the same community should like the same kind of movies. As a result, within the movie communities, most movies should belong to the same type. Meanwhile, because some movies are greatly loved by the masses, the gatherings of different communities will form a central area, representing the most popular movies.