import json


def convert_sharegpt(path, out_path):
    data = list(map(json.loads, open(path)))
    json_data = []
    for d in data:
        temp = {"messages": [], "images":[]}
        for message in d["messages"]:
            item = {"role": message["role"], "content": ""}
            for content in message["content"]:
                if content["type"] == "text":
                    item["content"] += content["text"]
                elif content["type"] == "image":
                    for url in content["urls"]:
                        temp["images"].append(url["path"])
                        item["content"] += "<image>"
            temp["messages"].append(item)
        json_data.append(temp)
    
    with open(out_path, "w") as fp:
        json.dump(json_data, fp, indent=2, ensure_ascii=False)

convert_sharegpt("/global_data/mllm/liulijun/data/medical/medical_report_anno1206.jsonl", "/global_data/mllm/liulijun/data/medical/gpt_medical_report_anno1206.json")
        
                