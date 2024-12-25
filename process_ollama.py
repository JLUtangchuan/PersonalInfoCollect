import pandas as pd
import requests
import json
import time
from const import OUTPUT_PATH
import os

def call_ollama(prompt, model="qwen2.5"):
    """调用 Ollama API"""
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()['response']
    except Exception as e:
        print(f"调用 Ollama 时出错: {str(e)}")
        return None

def process_data_with_ollama():
    # 读取CSV文件
    csv_path = os.path.join(OUTPUT_PATH, 'zhihu_data_combined.csv')
    df = pd.read_csv(csv_path)
    
    # 创建新列来存储 Ollama 的响应
    df['ollama_response'] = None
    
    # 处理每一行数据
    for index, row in df.iterrows():
        # 构建提示词
        prompt = f"请简要总结这个问题的要点：{row['标题']}"
        
        # 调用 Ollama
        response = call_ollama(prompt)
        
        if response:
            df.at[index, 'ollama_response'] = response
            print(f"处理完成 {index + 1}/{len(df)} : {row['标题']}")
        
        # 添加延时以避免请求过快
        time.sleep(1)
    
    # 保存结果
    output_file = os.path.join(OUTPUT_PATH, 'zhihu_data_with_ollama.csv')
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"处理完成！结果已保存到: {output_file}")

if __name__ == "__main__":
    process_data_with_ollama() 