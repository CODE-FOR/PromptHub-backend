from django.utils import timezone
import nltk as nltk
import math as math
import json
import os
import re
from core.models.prompt import Prompt
from tqdm import tqdm


def init_recommand_prompts(prompt_list: list[Prompt]):
    recommand_prompts = {}
    for prompt in tqdm(prompt_list):
        recommand_top_prompts = get_recommand_top_prompts(prompt, prompt_list)
        recommand_prompts[int(prompt.id)] = recommand_top_prompts
    # write to file
    json_object = json.dumps(recommand_prompts)
    with open("recommend_prompt.json", "w") as output_file:
        output_file.write(json_object)

def get_recommand_prompt_dict():
    # read from file
    with open('recommend_prompt.json', 'r') as openfile:
        recommand_prompts = json.load(openfile)
    return recommand_prompts

def check_recommand_prompts_exists():
    return os.path.exists("recommend_prompt.json")

def get_recommand_top_prompts(base_prompt: Prompt, prompt_list: list[Prompt], top=10):
    prompt_scores = {}
    for prompt in prompt_list:
        if base_prompt == prompt:
            continue
        hot_score = cal_score1(prompt.collection_count, (timezone.now() - prompt.created_at).total_seconds()/3600.0, 1.8)
        input1 = re.sub('[\W]+', ' ', base_prompt.prompt)
        input2 = re.sub('[\W]+', ' ', prompt.prompt)
        similarty_score = get_sentence_similarity(input1, input2)
        prompt_scores[prompt] = hot_score * similarty_score**2
    top_prompt_scores = sorted(prompt_scores.items(), key=lambda t: t[1], reverse=True)[:top]
    return [prompt.id for (prompt, _) in top_prompt_scores]

'''
* 优先推荐用户关注的人发布的新作品（按时间顺序，最新发布的在最前面）
* 热度和内容联合：
  * 先按热度排序：
    * score1 = P / (T+2) ^G^ 
    * P : 热度(点赞数) ； T：时间，+2防止除数太小；G：决定得分随时间下降的速度快慢，G通常取1.5,1.8,2

  * 再按内容相似度：
    * 根据用户收藏的prompt，与当前图像进行相似度计算. NLP
    * 相似度得分 = score2

  * score = score1 * score2**2
  * 按score降序进行推荐

* 改进：对于一些热度很高，但和用户收藏的prompt相关性很小的图像
  * 为score1设置一个阈值，超过阈值则直接推荐。
'''
# 构建词袋模型计算相似度算法部分

# 对两个句子的单词列表进行分词获取词袋
def get_bags_of_word(word_lists):
    bags_of_word = set()
    # 将两个句子中出现过的单词不重复地添加到一个集合中，构成词袋
    for word in word_lists:
        bags_of_word.update(word)
    # 去掉词袋中的标点符号
    bags_of_word = bags_of_word - {',', '.', '，', '。', ':', '!'}
    return bags_of_word

# 处理词袋获得字典
def get_dictionary(bags_of_word):
    dictionary = dict()
    # 每个在句子对中出现过的单词对应一个数字
    for num, word in enumerate(bags_of_word):
        dictionary[word] = num
    return dictionary

# 根据词语出现频率TF值，处理单词列表和字典获取词袋模型向量
def get_TFvector(word_list, dictionary):
    TFvector = list()
    # 根据字典的关键字在单词列表中出现的频次计算次数
    for key in dictionary.keys():
        TFvector.append((dictionary[key], word_list.count(key)))
    return TFvector

# 计算两个向量的余弦相似度
def get_cos_similarity(TFvector1, TFvector2):
    # 数量积
    scalar_product = 0
    TFvector1_length = 0
    TFvector2_length = 0
    for i in range(len(TFvector1)):
        scalar_product += TFvector1[i][1] * TFvector2[i][1]
        TFvector1_length += TFvector1[i][1] * TFvector1[i][1]
        TFvector2_length += TFvector2[i][1] * TFvector2[i][1]

    # 两个向量长度的乘积
    length_product = math.sqrt(TFvector1_length * TFvector2_length)
    return (scalar_product / length_product)

# 计算两个句子的相似度
def get_sentence_similarity(input1, input2):
    # 将两个句子合并为句子对
    sentences = [input1, input2]
    # 将句子对进行分词，分成两个单词列表
    word_lists = [[word for word in nltk.word_tokenize(sentence)] for sentence in sentences]

    # 根据单词列表获取词袋
    bags_of_word = get_bags_of_word(word_lists)

    # 根据词袋获取字典
    dictionary = get_dictionary(bags_of_word)

    # 根据词频计数获取词袋模型向量
    TFvector1 = get_TFvector(word_lists[0], dictionary)
    TFvector2 = get_TFvector(word_lists[1], dictionary)

    # 计算句子对的余弦相似度
    cos_similarity = get_cos_similarity(TFvector1, TFvector2)
    # 打印计算过程
    return cos_similarity


def cal_score1(p,t,g):
    return  (p + 1) / (pow(t+2, g))



