import json
import copy

def getpred(fname):

    f = open(fname)
    lines = f.readlines()
    f.close()

    f = open("ace2005-en/label2id.json")
    label2id = json.load(f)
    f.close()
    labelset = label2id.keys()

    tuplelines = [""]

    for line in lines:
        if line.startswith("~~~~"):
            tuplelines.append("")
        else:
            line = line.strip() + " "
            tuplelines[-1] += line

    tuplelines.pop(-1)
    # print(tuplelines)

    predict = []

    for idx, tupstr in enumerate(tuplelines):
        # print(tupstr)
        tuplist = tupstr.split(";")
        predlist = []
        for tup in tuplist:
            tup = tup.strip()
            if tup == "":
                continue
            if tup[0] != '(' or tup[-1] != ')':
                s = tup.find("(")
                e = tup.rfind(")")
                if s == -1 or e == -1:
                    continue
                else:
                    tup = tup[s:e+1]
            tup = tup[1:-1].split(",")
            if len(tup) != 2:
                continue
            tup = [x.strip() for x in tup]
            if tup[1] not in labelset:
                continue

            predlist.append(":".join(tup))
        # print(predlist)
        predstr = ";".join(predlist)
        predict.append(predstr)
    
    return predict

def getgold():
    f = open("test/test.json")
    testset = json.load(f)
    f.close()

    testlabel = [test["label"] for test in testset]
    goldlist = []
    for label in testlabel:
        pairlist = []
        for pair in label:
            pairlist.append(":".join(pair))
        goldlist.append(";".join(pairlist))
    return goldlist

def computef1(predlist, goldlist):
    tp = 0
    n_gold = 0
    n_pred = 0

    for idx in range(len(predlist)):
        gold_text = goldlist[idx]
        gold_label = []
        for label in gold_text.split(';'):
            if label:
                gold_label.append(label)
        # pred triple
        pred_text = predlist[idx]
        pred_label = []
        for label in pred_text.split(';'):
            label = label.strip()
            if label and 'NA' not in label and ":" in label:
                pred_label.append(':'.join([l.strip() for l in label.split(':')]))
        label_stack = copy.deepcopy(gold_label)
        for label in pred_label:
            if label in label_stack:
                tp += 1
                label_stack.remove(label)
        n_gold += len(gold_label)
        n_pred += len(pred_label)

    precision = tp / (n_pred + 1e-10)
    recall = tp / (n_gold + 1e-10)
    f1 = 2 * precision * recall / (precision + recall + 1e-10)
    print({
        "precision": precision,
        "recall": recall,
        "f1": f1
    })


predlist = getpred("answer/answer_15000.txt")
goldlist = getgold()
computef1(predlist, goldlist)

