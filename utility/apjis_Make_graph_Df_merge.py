import pandas as pd
import networkx as nx
from itertools import combinations
from collections import Counter
import os

# 전체 file 리스트 중, 특정 word가 포함된 것들을 불러와서 처리한 뒤 하나로 통합
def misq_apjis_preprocessing(data_path: str):
    data_list = os.listdir(data_path)
    result = []
    for keyword_file in [file for file in data_list if 'keyword' in file]:
        keyword_df = pd.read_csv(data_path + keyword_file).drop(columns='Unnamed: 0')
        method_df = pd.read_csv(data_path + keyword_file.replace('keyword', 'method')).rename(columns={'method': 'keyword'})
        theory_df = pd.read_csv(data_path + keyword_file.replace('keyword', 'theory')).rename(columns={'theory': 'keyword'})
        
        keyword_df['categories'] = 'keyword'
        method_df['categories'] = 'method'
        theory_df['categories'] = 'theory'
        
        total_df = pd.concat([keyword_df, method_df, theory_df], ignore_index=True).drop(columns='Unnamed: 0')
        result.append(total_df)
        
    return result

# List 형태의 데이터로부터 Graph를 형성함.
class graph_make():
    def __init__(self, df):
        self.DataFrame = df
        self.edge_list = self.edge_make()
        self.total_list = self.total_edge()
        self.mapping_dict = self.make_map_dict()
    
    def make_map_dict(self):
        mapping_dict = dict()
        for i in range(len(self.DataFrame)):
            keyword = self.DataFrame['keyword'][i]
            categories = self.DataFrame['categories'][i]
            mapping_dict[keyword] = categories
            
        return mapping_dict
        
    def edge_make(self):
        edge_list = []
        for i in self.DataFrame['num'].unique():
            temp_data = self.DataFrame[self.DataFrame['num'] == i]
            temp_list = list(temp_data['keyword'])
            edge_list.append(temp_list)
        return edge_list

    def create_tuples(self, lst):
        # 리스트에서 2개의 원소를 선택하여 튜플로 만듦
        tuples = list(combinations(lst, 2))

        # 튜플 순서를 정렬하여 중복 제거
        unique_tuples = list(set([tuple(sorted(t)) for t in tuples]))

        return unique_tuples
    
    def total_edge(self):
        total_list = []
        for lst in self.edge_list:
            temp_list = self.create_tuples(lst)
            total_list = total_list + temp_list
        
        return total_list
    
    def graph(self):
        # 튜플 빈도수 계산
        tuple_counts = Counter(self.total_list)

        # 그래프 생성
        G = nx.Graph()

        # 중복되는 튜플인 경우 가중치를 증가시키면서 엣지 추가
        for tuple_pair, count in tuple_counts.items():
            G.add_edge(tuple_pair[0], tuple_pair[1], weight=count)
            
        for key, value in self.mapping_dict.items():
            try:
                G.nodes[key]['Categories'] = value
            except:
                print(f"Wrong Key Error. {key} node doesn't exist")

        return G
