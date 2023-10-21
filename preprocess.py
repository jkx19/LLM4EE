import json
import random

def gettrain():
    f = open("ED/train.json")
    train = json.load(f)
    f.close()

    trainsample = []

    train = train["request_states"]

    for ist in train:
        text = ist["instance"]["input"]["text"]
        result = ist["instance"]["references"][0]["output"]["text"]
        label = []
        
        if result != "":
            pairs = result.split(";")
            for pair in pairs:
                pair = pair.split(":")
                pair = [t.strip() for t in pair]
                label.append(pair)
                    
        
        trainsample.append({
            "text": text,
            "label": label,
        })

    f = open("ED/dev.json")
    dev = json.load(f)
    f.close()

    dev = dev["request_states"]

    for ist in dev:
        text = ist["instance"]["input"]["text"]
        result = ist["instance"]["references"][0]["output"]["text"]
        label = []
        
        if result != "":
            pairs = result.split(";")
            for pair in pairs:
                pair = pair.split(":")
                pair = [t.strip() for t in pair]
                label.append(pair)
                    
        
        trainsample.append({
            "text": text,
            "label": label,
        })

    print(len(trainsample))
    f = open("train/train.json", "w")
    json.dump(trainsample, f)
    f.close()

def gettest():
    f = open("ED/test.json")
    test = json.load(f)
    f.close()

    testsample = []

    test = test["request_states"]

    for ist in test:
        text = ist["instance"]["input"]["text"]
        result = ist["instance"]["references"][0]["output"]["text"]
        label = []
        
        if result != "":
            pairs = result.split(";")
            for pair in pairs:
                pair = pair.split(":")
                pair = [t.strip() for t in pair]
                label.append(pair)
                    
        
        testsample.append({
            "text": text,
            "label": label,
        })

    testsample = random.sample(testsample, 500)
    print(len(testsample))
    f = open("test/test.json", "w")
    json.dump(testsample, f)
    f.close()


f = open("train/train.json")
train = json.load(f)
f.close()
train = [x["text"] for x in train]
f = open("train/train_sent.json", "w")
json.dump(train, f)
f.close()

f = open("test/test.json")
test = json.load(f)
f.close()
test = [x["text"] for x in test]
f = open("test/test_sent.json", "w")
json.dump(test, f)
f.close()


random.seed(42)
# gettrain()
# gettest()

# f = open("ace2005-en/test.json")
# data = json.load(f)
# f.close()
# print(len(data))

