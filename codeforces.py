#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
from urllib.request import urlopen, Request
import os
import csv
import operator

codeforces = {}
req = Request(url="https://codeforces.com/api/problemset.problems", headers={'User-Agent': 'Mozilla/5.0'})
context = json.loads(urlopen(req).read())
for i, j in zip(context['result']['problems'], context['result']['problemStatistics']):
    contestId = i['contestId']
    index = i['index']
    name = i['name']
    # default rating is 1500
    rating = i['rating'] if 'rating' in i else 1500
    tags = i['tags']
    # skip Contest921
    if contestId == 921:
        continue
    problemId = str(contestId) + index
    codeforces[problemId] = {'title': name, 'tags': tags,
                             'rating': rating, 'solved': j['solvedCount'], 'accepted': 0, }

# 用户昵称根据需求进行更改，默认是托老爷的
req = Request(url="https://codeforces.com/api/user.status?handle=tourist", headers={'User-Agent': 'Mozilla/5.0'})
context = json.loads(urlopen(req).read())
for i in context['result']:
    if i['verdict'] == 'OK':
        contestId = i['problem']['contestId']
        index = i['problem']['index']
        problemId = str(contestId) + index
        # just choose the problems Accepted in problemset
        if problemId in codeforces:
            codeforces[problemId]['accepted'] = 1

# %% output the problemset to csv files
with open("./CodeForces_ProblemSet.csv", "w+", encoding="utf-8") as f_out:
    f_csv = csv.writer(f_out)
    f_csv.writerow(['ID', 'Title', 'Tags', 'Rating', 'Solved', 'Accepted'])
    for id in codeforces:
        title = codeforces[id]['title']
        tags = ', '.join(codeforces[id]['tags'])
        rating = codeforces[id]['rating']
        solved = codeforces[id]['solved']
        accepted = codeforces[id]['accepted']
        f_csv.writerow([id, title, tags, rating, solved, accepted])
    f_out.close()

# %% analyze the problem set
# initialize the difficult and tag list
difficult_level = {}
tags_level = {}
for id in codeforces:
    # difficult = re.findall('[A-Z]', id)[0]
    difficult = codeforces[id]['rating']
    tags = codeforces[id]['tags']
    difficult_level[difficult] = difficult_level.get(difficult, 0) + 1
    for tag in tags:
        tags_level[tag] = tags_level.get(tag, 0) + 1
tag_level = sorted(tags_level.items(), key=operator.itemgetter(1))[::-1]
tag_list = [foo[0] for foo in tag_level]
difficult_level = sorted(difficult_level.items(), key=operator.itemgetter(0))
difficult_list = [foo[0] for foo in difficult_level]

# initialize the 2D relationships matrix
# matrix_solved: the number of AC submission for each tag in each difficult level
# matrix_freq: the number of tag frequency for each diffiicult level
matrix_solved, matrix_freq = [
    [[0] * len(difficult_list) for _ in range(len(tag_list))] for _ in range(2)]

# construct the 2D relationships matrix
for id in codeforces:
    # difficult = re.findall('[A-Z]', id)[0]
    difficult = codeforces[id]['rating']
    difficult_id = difficult_list.index(difficult)
    tags = codeforces[id]['tags']
    solved = codeforces[id]['solved']
    for tag in tags:
        tag_id = tag_list.index(tag)
        matrix_solved[tag_id][difficult_id] += solved
        matrix_freq[tag_id][difficult_id] += 1

# %% visualization
def outputMatrix(name, data):
    with open('./'+name, "w+", encoding="utf-8") as f_out:
        f_csv = csv.writer(f_out)
        f_csv.writerow(['Tags/Difficult '] + difficult_list)
        for i in range(len(tag_list)):
            tag = tag_list[i]
            f_csv.writerow([tag]+data[i])
        f_out.close()
    return


outputMatrix('Matrix_AC_Tags.csv', matrix_solved)
outputMatrix('Matrix_Count_Tags.csv', matrix_freq)
