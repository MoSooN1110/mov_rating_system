import json
import random
import datetime
import math

def calc_rating(scores):
    num = len(scores)
    scores_vec = []
    for score in scores:
        scores_vec.append(score["score"])

    param = 0.8
    for i in range(0, num):
        scores_vec[i] = scores_vec[i]*param

    # print(scores_vec)
    # print(num)
    scores_vec.reverse()
    # print(scores_vec)

    rating = 0.0
    for i in range(0, num):
        rating += scores_vec[i] * (0.9 ** i)
    denomi = 0.0
    for i in range(0, num):
        denomi += 0.9 ** i
    rating /= denomi
    rating -= rating/(math.sqrt(num+3))
    rating = int(rating)
    return rating


def get_color(rating):
    if rating >= 3200:
        return "red"
    elif rating >= 2800:
        return "red"
    elif rating >= 2400:
        return "orange"
    elif rating >= 2000:
        return "yellow"
    elif rating >= 1600:
        return "blue"
    elif rating >= 1200:
        return "cyan"
    elif rating >= 800:
        return "green"
    elif rating >= 400:
        return "brown"
    else:
        return "gray"

def get_diff(current_rating, prev_rating):
    val = current_rating - prev_rating
    if val > 0:
        return "+" + str(val)
    else:
        return str(val)
def main():
    # メインの処理をここに書く
    print("Run Rating Reloader")

    with open('../data/data.json', 'r') as file:
        data1 = json.load(file)

    with open('../data/get_data.json', 'r') as file:
        data2 = json.load(file)
    # print(data2)
    # dict1 = dict()
    # for x in range(0, len(data1)):
    #     dict1[data1[x]["username"]] = data1[x]

    # print(dict1)
    # data1 = dict1
    contest_hash  = random.getrandbits(256)
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H%M%S")
    print(now)
    print(contest_hash)
    #json sample

    
    for key in data2:
        if data1.get(key) == None:
            data1[key] = {
                "username": key,
                "rating": 0,
                "participation_count": 0,
                "prev_rating": 0,
                "latest_score" : 0,
                "diff": 0,
                "color": "gray",
                "scores":[]
            }
        data1[key]["scores"].append({
            "score": data2[key],
            "contest_hash": contest_hash,
            "date": now.strftime("%Y-%m-%d")
        })
        data1[key]["latest_score"] = data2[key]
    # reload rating
    print(data1)
    for key in data2:
        data1[key]["prev_rating"] = data1[key]["rating"]
        data1[key]["rating"] = calc_rating(data1[key]["scores"])
        data1[key]["diff"] = get_diff(data1[key]["rating"], data1[key]["prev_rating"])
        data1[key]["color"] = get_color(data1[key]["rating"])
        data1[key]["participation_count"] += 1
        
    
    for key in data1:
        if data2.get(key) == None:
            data1[key]["diff"] = '0'
            data1[key]["latest_score"] = 0
    

    with open('../data/data.json', 'w') as json_file:
        json.dump(data1, json_file, indent=4)
    with open('../log/data'+timestamp+'.json', 'w') as json_file:
        json.dump(data1, json_file, indent=4)

    present_data = []
    for key in data1:
        if key == "tmp":
            continue
        present_data.append(data1[key])
    
    present_data.sort(key=lambda x: x["rating"], reverse=True)
    for i in range(0, len(present_data)):
        present_data[i]["rank"] = i + 1
    with open('../data/present_data.json', 'w') as json_file:
        json.dump(present_data, json_file, indent=4)



if __name__ == "__main__":
    main()