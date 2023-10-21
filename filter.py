import json
import numpy as np
import random
from tqdm import tqdm


def complete(demolist:list, shot):
    # print(demolist)
    demoset = set(demolist)
    while len(demoset) < shot:
        demoset.add(random.randint(1, 15000))
    return list(demoset)
            

def find_idx(sample=1000, shot=30):
    f = open(f"mutual/openie_{sample}.json")
    distances = json.load(f)
    f.close()

    demo_set = []

    # shot = 30
    # sample = 20000

    random.seed(42)


    for sidx, disttup in tqdm(enumerate(distances), total=len(distances)):
        disttup.sort(key=lambda a: a[0])
        bestlist = disttup[-shot:]
        # exit()
        bestlist = [a[1] for a in bestlist]
        if len(bestlist) < shot:
            bestlist = complete(bestlist, shot)
        demo_set.append(bestlist)
        
    f = open(f"mutual/demo_oie_{sample}.json", "w")
    json.dump(demo_set, f)
    f.close()


ee_instruction = "Please identify the words that indicating events in the text and classify them into appropriate categories; The collection of categories is [Conflict.Attack, Movement.Transport, Life.Die, Contact.Phone-Write, Life.Injure, Contact.Meet, Transaction.Transfer-Ownership, Personnel.End-Position, Justice.Arrest-Jail, Conflict.Demonstrate, Life.Marry, Personnel.Elect, Personnel.Start-Position, Personnel.Nominate, Business.End-Org, Justice.Execute, Business.Start-Org, Justice.Fine, Transaction.Transfer-Money, Justice.Trial-Hearing, Justice.Sue, Justice.Charge-Indict, Justice.Sentence, Life.Be-Born, Justice.Extradite, Business.Declare-Bankruptcy, Justice.Convict, Justice.Release-Parole, Business.Merge-Org, Justice.Appeal, Justice.Pardon, Life.Divorce, Justice.Acquit]. Here are several examples. "


def build_prompt_llama(sample, sub=500):
    train_data = json.load(open("train/train.json"))
    examples = []
    for instance in train_data:
        examples.append({
            "input": instance["text"],
            "output": instance["label"]
        })

    f = open(f"mutual/demo_oie_{sample}.json")
    demos_idx = json.load(f)
    f.close()

    test_json = json.load(open("test/test.json"))
    test_sentences = [x["text"] for x in test_json]

    messages = []
    for idx, data in enumerate(test_sentences[:sub]):
        message = ee_instruction
        demos = [examples[j] for j in demos_idx[idx]]
        random.shuffle(demos)
        for demo in demos:
            label = demo["output"]
            pairs = ["(" + ", ".join(pair) + ")" for pair in label]
            labelstr = ";".join(pairs)
            input = demo["input"]
            # if labelstr == "":
            #     labelstr = "(None, None)"
            message += f"Sentence: {input} Answer: {labelstr}. "
            # print(f"Sentence: {input}. Answer: {labelstr}. ")
            # exit()
        message += f"Now please identify the words that indicate events in the following Sentence assign them a label? Please output your result in the format of (words, event type) and use ';' to separate the tuples. The sentence is {data}. Answer: "
        # print(message)
        # exit()
        messages.append(message)

    # print(len(messages))
    f = open(f"prompt/prompt_llama_{sample}.json", "w")
    json.dump(messages, f)
    f.close()


def build_prompt(sample, sub=500):
    train_data = json.load(open("train/train.json"))
    examples = []
    for instance in train_data:
        examples.append({
            "input": instance["text"],
            "output": instance["label"]
        })

    f = open(f"mutual/demo_hw_{sample}.json")
    demos_idx = json.load(f)
    f.close()

    test_json = json.load(open("test/test.json"))
    test_sentences = [x["text"] for x in test_json]

    messages = []
    for idx, data in enumerate(test_sentences[:sub]):
        message = [
            {"role": "system", "content": "You are a helpful, pattern-following assistant."}
        ]
        message.append({
            "role": "user",
            "content": ee_instruction
        })
        demos = [examples[j] for j in demos_idx[idx]]
        random.shuffle(demos)
        for demo in demos:
            message.append({
                "role": "user", "content": "Text: " + demo["input"] + "\n"
            })
            label = demo["output"]
            pairs = ["(" + ", ".join(pair) + ")" for pair in label]
            labelstr = ";".join(pairs)
            message.append({
                "role": "assistant","content": labelstr + "\n"
            })
            # print(labelstr)
        message.append({"role": "user", "content": data})
        messages.append(message)

    # print(len(messages))
    f = open(f"prompt/prompt_hw_{sample}.json", "w")
    json.dump(messages, f)
    f.close()


for sample in [50, 500, 1500, 5000, 15000]: 
    find_idx(sample=sample, shot=20)
    build_prompt_llama(sample)


