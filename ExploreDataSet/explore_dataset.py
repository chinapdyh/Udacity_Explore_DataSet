import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

EXPLORE_DATA = {'1': 'C:/Users/Dyh-PC/My Documents/UdacityNumpyPandas/DataSets/ExploreDataSet/tmdb_movies.csv',
                '2': 'C:/Users/Dyh-PC/My Documents/UdacityNumpyPandas/DataSets/ExploreDataSet/noshowappointments_kagglev2_may_2016.csv',
                '3': 'C:/Users/Dyh-PC/My Documents/UdacityNumpyPandas/DataSets/ExploreDataSet/ncis_and_census_data/gun_data.csv',
                '4': 'C:/Users/Dyh-PC/My Documents/UdacityNumpyPandas/DataSets/ExploreDataSet/ncis_and_census_data/U.S. Census Data.csv'
                }

dataset_type_list = {'1', '2', '3'}

def choose_dataset_type():
    '''
    选择需要分析的数据集,并返回数据集类型
    '''
    dataset_name_list = ['Tmdb电影数据',
                         '未前往就诊挂号预约数据',
                         'FBI枪支数据']
    dataset_type = input_mode('\n请选择需要分析的数据集:1.TMdb电影数据；2.未前往就诊挂号预约数据；3.FBI枪支数据'
                              '(请输入数字1,2,3进行数据集选择)\n',
                              '请输入正确的格式，如1或2',
                              dataset_type_list,
                              lambda x: x
                              )
    print('您选择的数据集是：{}'.format(dataset_name_list[int(dataset_type) - 1]))
    return dataset_type

def load_data(dataset_type):
    '''
    从csv文件中加载数据
    :param dataset_type: 数据集类型
    :return: DataFrame
    '''
    df1 = ''
    df2 = ''
    if dataset_type in dataset_type_list:
        df1 = pd.read_csv(EXPLORE_DATA[dataset_type])
    if dataset_type == '3':
        df2 = pd.read_csv(EXPLORE_DATA['4'])
    return df1, df2

def clean_data(df1, df2):
    '''
    清洗数据
    '''
    print('\n正在清洗数据，请稍等...\n')
    if df1 is not None:
        print(df1.info())

    return df1, df2

def analysis_data(df1, df2, dataset_type):
    '''
    分析并处理数据
    '''
    print('\n正在分析数据，请稍等...\n')

    if dataset_type == '1':
        analysis_tmdb_dataset(df1)

    #elif dataset_type == '2':
    #elif dataset_type == '3':

def analysis_tmdb_dataset(df1):
    '''
    分析tmdb电影数据集
    '''
    if df1 is not None:
        print(df1.columns)

        # 问题1：票房最高的电影的演职人员是谁？导演是谁？发布公司是谁？是哪一年的？是什么电影等。
        condition = df1['revenue'] == df1['revenue'].max()
        df = df1[condition]
        print('\n票房最高的电影是：{}'.format(df['original_title'].iloc[0]))
        print('票房最高的电影的预算花费是：{}'.format(df['budget'].iloc[0]))
        print('票房最高的电影的预算花费(通胀)是：{}'.format(df['budget_adj'].iloc[0]))
        print('票房最高的电影的票房是：{}'.format(df['revenue'].iloc[0]))
        print('票房最高的电影的票房(通胀)是：{}'.format(df['revenue_adj'].iloc[0]))
        print('票房最高的电影的导演是：{}'.format(df['director'].iloc[0]))
        print('票房最高的电影的演职人员有：{}'.format(df['cast'].iloc[0]))
        print('票房最高的电影的发行公司是：{}'.format(df['production_companies'].iloc[0]))
        print('票房最高的电影的发行年份是:{}'.format(df['release_year'].iloc[0]))
        print('票房最高的电影的流行度(popularity)是：{}'.format(df['popularity'].iloc[0]))
        print('票房最高的电影投票得分是: {}\n'.format(df['vote_average'].iloc[0]))

        # 数据处理 处理 '|'
        new_rows = split_tmdb_data(df1)

        #问题2：哪位演职人员最近的一年票房最高？
        condition = new_rows['release_year'].max() == new_rows['release_year']
        df = new_rows[condition]
        actor = df.groupby('actor')['revenue'].sum().idxmax()
        revenue = df.groupby('actor')['revenue'].sum().max()
        print('\n最近1年(2015)年演员{}的票房总收入最高，总票房为：{}\n'.format(actor, revenue))

        #问题3：哪位演职人员的历史总票房最高？
        actor = new_rows.groupby('actor')['revenue'].sum().idxmax()
        revenue = new_rows.groupby('actor')['revenue'].sum().max()
        print('\n演员{}的历史总票房最高，总票房为：{}\n'.format(actor, revenue))

        #问题4：哪位导演最近一年的电影票房最高？
        condition = df1['release_year'].max() == df1['release_year']
        df = df1[condition]
        director = df.groupby('director')['revenue'].sum().idxmax()
        revenue = df.groupby('director')['revenue'].sum().max()
        print('\n最近1年(2015)年导演{}的票房总收入最高，总票房为：{}\n'.format(director, revenue))

        #问题5：哪位导演的历史总票房最高？
        director = df1.groupby('director')['revenue'].sum().idxmax()
        revenue = df1.groupby('director')['revenue'].sum().max()
        print('\n导演{}的历史总票房最高，总票房为：{}\n'.format(director, revenue))

        #问题6：哪家发行公司的电影历史总票房最高？
        compony = new_rows.groupby('company')['revenue'].sum().idxmax()
        revenue = new_rows.groupby('company')['revenue'].sum().max()
        print('\n{}公司的历史总票房最高，总票房为：{}\n'.format(compony, revenue))

        #问题7：最受欢迎（popularity）最高的电影类别(genres)是什么？
        category = new_rows.groupby('category')['popularity'].mean().idxmax()
        popularity = new_rows.groupby('category')['popularity'].mean().max()
        print('\n{}类型的电影受欢迎程度最高，平均受欢迎程度为{}\n'.format(category, popularity))

        #问题8：平均投票得分(vote average)最高的电影类别(genres)是什么？
        category = new_rows.groupby('category')['vote_average'].mean().idxmax()
        vote_average = new_rows.groupby('category')['vote_average'].mean().max()
        print('\n{}类型的电影平均投票得分最高，平均投票得分为{}\n'.format(category, vote_average))

        #问题9：票房高的电影有哪些特点？
        print('\n电影票房排名前10数据分析：')
        df = df1.sort_values(by='revenue', axis=0, ascending=False)
        df = df.iloc[0:10]
        titles = df['original_title']
        for i in range(0, len(df)):
            print('票房排名第{}位的电影是{},导演是{}'.format(i + 1, df.iloc[i].original_title, df.iloc[i].director))
            print('这部电影的投资额是{}'.format(df.iloc[i].budget))
            print('这部电影的受欢迎程度是{}'.format(df.iloc[i].popularity))
            print('这部电影的投票得分是{}'.format(df.iloc[i].vote_average))

        new_table = new_rows.query('original_title == "{}"'.format(titles.iloc[0]))
        for i in range(1, len(titles)):
            tp = new_rows.query('original_title == "{}"'.format(titles.iloc[i]))
            new_table = new_table.append(tp)
        print('\n电影票房排名前10的电影里面，演员出演的次数：')
        print(new_table.groupby('actor')['actor'].count().sort_values(ascending=False))
        print('\n电影票房排名前10的电影里面，电影发行公司有：')
        print(new_table.groupby('company')['company'].count().sort_values(ascending=False))
        print('\n电影票房排名前10的电影里面，电影类型为：')
        print(new_table.groupby('category')['category'].count().sort_values(ascending=False))

        #问题10：流行度最高的电影是什么？导演是谁？票房多少？
        condition = df1['popularity'] == df1['popularity'].max()
        df = df1[condition]
        print('\n流行度最高的电影是{},导演是{},票房是{}'.format(df.original_title.iloc[0], df.director.iloc[0], df.revenue.iloc[0]))

        #问题11：评分最高的电影是什么？导演是谁？票房多少？
        condition = df1['vote_average'] == df1['vote_average'].max()
        df = df1[condition]
        print('\n平均评分最高的电影是{},导演是{}, 平均得分是{}'.format(df.original_title.iloc[0], df.director.iloc[0], df.vote_average.iloc[0]))

        #问题12：超过1000人评价的电影中，平均评分最高的电影是什么？导演是谁？评分多少？
        condition = df1['vote_count'] > 1000
        df = df1[condition]
        condition = df['vote_average'] == df['vote_average'].max()
        df = df[condition]
        print('\n超过1000人评价的电影中，平均评分最高的电影是{},导演是{}, 平均得分是{}'.format(df.original_title.iloc[0], df.director.iloc[0], df.vote_average.iloc[0]))

        #问题13: 最近1年（2015年），超过1000人评价的电影中，平均评分最高的电影是什么？导演是谁？评分多少？
        condition = df1['release_year'] == 2015
        df = df1[condition]
        condition = df['vote_count'] > 1000
        df = df[condition]
        condition = df['vote_average'] == df['vote_average'].max()
        df = df[condition]
        print('\n最近1年（2015年），超过1000人评价的电影中，平均评分最高的电影是{},导演是{}, 平均得分是{}'.format(df.original_title.iloc[0], df.director.iloc[0], df.vote_average.iloc[0]))

def draw_data(df1, df2, dataset_type):
    '''
    绘制图形
    '''

    if dataset_type == '1':
        draw_tmdb_data(df1)

    #elif dataset_type == '2':
    #elif dataset_type == '3':

def draw_tmdb_data(df1):
    '''
    绘制Tmdb电影数据集数据
    '''
    if df1 is not None:
        # 数据处理 处理 '|'
        new_rows = split_tmdb_data(df1)

        #1.从1975年到2015年，历年来詹姆斯卡梅隆（James Cameron）和斯蒂芬斯皮尔伯格(Steven Spielberg)票房对比。
        condition = df1['release_year'] > 1974
        df = df1[condition]
        x = range(1975, 2016)
        df_James  = df[df['director'] == 'James Cameron']
        df_Steven = df[df['director'] == 'Steven Spielberg']
        plt.bar(df_James.release_year, df_James.revenue, width=0.5, color='r', label='James Cameron')
        plt.bar(df_Steven.release_year + 0.5, df_Steven.revenue, width=0.5, color='b', label='Steven Spielberg')
        plt.ylabel('Revenue')
        plt.xlabel('Year')
        plt.title('James Cameron and Steven Spielberg Revenue')
        plt.legend(loc=0)
        plt.show()

        #2.显示历史票房排名前五的电影导演。
        director_total_revenue = df1.groupby('director')['revenue'].sum().sort_values(ascending=False)
        y = director_total_revenue.iloc[0:5]
        plt.bar(y.index, y, width=0.25, color='r', label='Total Revenue')
        plt.ylabel('Revenue')
        plt.xlabel('Director')
        plt.title('Director revenue')
        plt.show()

        #3.显示历史上获取票房最多的制片公司（前5）。
        company_total_revenue = new_rows.groupby('company')['revenue'].sum().sort_values(ascending=False)
        y = company_total_revenue.iloc[0:5]
        plt.bar(y.index, y, width=0.25, color='r', label='Total Revenue')
        plt.ylabel('Revenue')
        plt.xlabel('Company')
        plt.title('Company revenue')
        plt.show()

        #4.最受欢迎的100部电影的类别统计。
        df = new_rows.sort_values(by='popularity', axis=0, ascending=False)
        category_by_popularity = df.groupby('category')['popularity'].mean().sort_values(ascending=False)
        y = category_by_popularity.iloc[0:10]
        plt.bar(y.index, y, width=0.25, color='r', label='Category')
        plt.ylabel('Total')
        plt.xlabel('Category')
        plt.title('Category Total')
        plt.show()

        #5.超过1000人的电影评价中，排名前十名电影是什么。
        condition = df1['vote_count'] > 1000
        df = df1[condition]
        df = df.sort_values(by='vote_average', axis=0, ascending=False)
        y = df.iloc[0:5]
        plt.bar(y.original_title, y.vote_average, width=0.25, color='r', label='Vote_Avg')
        plt.ylabel('Vote_Avg')
        plt.xlabel('Movie')
        plt.title('Vote_Avg Movie')
        plt.show()

        #6.在流行度排名前100的电影中，绘制流行度与票房收入的散点图，二者是否有关联。
        df = df1.sort_values(by='popularity', axis=0, ascending=False)
        df = df.iloc[0:100]
        df = df[df['revenue'] != 0]
        plt.scatter(df.revenue, df.popularity, marker='o')
        plt.ylabel('popularity')
        plt.xlabel('Revenue')
        plt.title('Revenue popularity')
        plt.show()

        #7.票房排名前100名的电影，其流行度与票房的散点图。
        df = df1.sort_values(by='revenue', axis=0, ascending=False)
        df = df.iloc[0:100]
        plt.scatter(df.revenue, df.popularity, marker='o')
        plt.ylabel('popularity')
        plt.xlabel('Revenue')
        plt.title('Revenue popularity')
        plt.show()

        #8.1000人以上的评分的电影中，评分前500名的电影评分与电影票房的关系。
        condition = df1['vote_count'] > 1000
        df = df1[condition]
        df = df1.sort_values(by='vote_average', axis=0, ascending=False)
        df = df.iloc[0:500]
        temp = df[df['revenue'] > 100000]
        plt.scatter(temp.vote_average, temp.revenue, marker='o')
        plt.ylabel('Revenue')
        plt.xlabel('vote_average')
        plt.title('Revenue vote_average')
        plt.show()

        #9.查看所有电影流行度与票房间的关系。
        df = df1[df1['revenue'] != 0]
        plt.scatter(df.revenue, df.popularity, marker='o')
        plt.ylabel('popularity')
        plt.xlabel('Revenue')
        plt.title('Revenue popularity')
        plt.show()

        #10.查看所有评分与电影票房间的关系。
        df = df1[df1['revenue'] > 0]
        plt.scatter(df.vote_average, df.revenue, marker='o')
        plt.ylabel('Revenue')
        plt.xlabel('vote_average')
        plt.title('Revenue vote_average')
        plt.show()

        #考虑通胀情况
        df = df1[df1['revenue_adj'] > 0]
        plt.scatter(df.vote_average, df.revenue_adj, marker='o')
        plt.ylabel('Revenue')
        plt.xlabel('vote_average')
        plt.title('Revenue vote_average - Adj')
        plt.show()

        #11.查看不同类型的电影的票房对比。
        df_sum = new_rows.groupby('category')['revenue'].sum().sort_values(ascending=False)
        df_sum = df_sum.iloc[0:10]
        plt.bar(df_sum.index, df_sum, width=0.25, color='r', label='Category Revenue')
        plt.show()

        #12.电影预算与电影票房间的关系。
        df = df1[df1['revenue'] > 100000]
        df = df[df['budget'] > 100000]
        plt.scatter(df.budget, df.revenue, marker='o')
        plt.ylabel('Revenue')
        plt.xlabel('Budget')
        plt.title('Revenue - Budget')
        plt.show()

        #电影预算与电影票房间的关系(考虑通胀)。
        df = df1[df1['revenue_adj'] > 100000]
        df = df[df['budget_adj'] > 100000]
        plt.scatter(df.budget_adj, df.revenue_adj, marker='o')
        plt.ylabel('Revenue')
        plt.xlabel('Budget')
        plt.title('Revenue - Budget - Adj')
        plt.show()

def split_tmdb_data(df1):
    '''
    处理tmdb 数据集中的 '|'
    '''
    df_01 = df1.copy()
    df_02 = df1.copy()
    df_03 = df1.copy()
    df_04 = df1.copy()
    df_05 = df1.copy()
    df_01['actor'] = df1['cast'].str.split('|', expand=True)[0]
    df_02['actor'] = df1['cast'].str.split('|', expand=True)[1]
    df_03['actor'] = df1['cast'].str.split('|', expand=True)[2]
    df_04['actor'] = df1['cast'].str.split('|', expand=True)[3]
    df_05['actor'] = df1['cast'].str.split('|', expand=True)[4]

    df_01['company'] = df1['production_companies'].str.split('|', expand=True)[0]
    df_02['company'] = df1['production_companies'].str.split('|', expand=True)[1]
    df_03['company'] = df1['production_companies'].str.split('|', expand=True)[2]
    df_04['company'] = df1['production_companies'].str.split('|', expand=True)[3]
    df_05['company'] = df1['production_companies'].str.split('|', expand=True)[4]

    df_01['category'] = df1['genres'].str.split('|', expand=True)[0]
    df_02['category'] = df1['genres'].str.split('|', expand=True)[1]
    df_03['category'] = df1['genres'].str.split('|', expand=True)[2]
    df_04['category'] = df1['genres'].str.split('|', expand=True)[3]
    df_05['category'] = df1['genres'].str.split('|', expand=True)[4]
    new_rows = df_01.append(df_02).append(df_03).append(df_04).append(df_05)
    return new_rows

def keep_alphabeta(str):
    '''
    只保留字符串中的字符
    '''
    temp = ''
    for c in str:
        if c.isalpha():
            temp = temp + c
    return temp

def keep_num(str):
    '''
    只保留数字
    '''
    temp = ''
    for c in str:
        if c.isdigit() or c == '.':
            temp = temp + c
    return temp

def keep_str_start_with_alpha(str):
    '''
    确保字符串以字母开始，删除开头其他无用字符
    '''
    temp = ''
    for c in str:
        if c.isdigit() is not True:
            temp = temp + c
    return temp

def delete_index(str):
    '''
    删除字符串开头索引
    '''
    temp = ''
    for c in str:
        if c.isdigit() is False:
            break
    for c in str:
        temp = temp + c
    return temp

def input_mode(input_print, error_print, enterable_list, get_value):
    '''
    输入，与输出
    '''
    ret = get_value(input(input_print))
    while ret not in enterable_list:
        ret = get_value(input(error_print))
    return ret

def main():
    while True:
        dataset_type = choose_dataset_type()
        df1, df2 = load_data(dataset_type)
        df1, df2 = clean_data(df1, df2)
        analysis_data(df1, df2, dataset_type)
        draw_data(df1, df2, dataset_type)
        restart = input('\n是否继续探索数据集? 输入yes 或 y继续；其它退出.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break

if __name__ == "__main__":
    main()