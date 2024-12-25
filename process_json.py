import os
import json
import pandas as pd
from glob import glob
from const import JSON_PATH, OUTPUT_PATH

def process_zhihu_json_files():
    # 获取所有符合格式的JSON文件
    json_pattern = os.path.join(JSON_PATH, "*-*-*-zhihu.json")
    json_files = glob(json_pattern)
    print(json_files)
    
    # 存储所有数据的列表
    all_data = []
    
    # 读取每个JSON文件
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 确保数据是列表格式
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {str(e)}")
    
    # 转换为DataFrame
    df = pd.DataFrame(all_data)
    
    # 根据标题去重
    df_unique = df.drop_duplicates(subset=['标题'])
    
    # 确保输出目录存在
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    
    # 保存到CSV文件
    output_file = os.path.join(OUTPUT_PATH, 'zhihu_data_combined.csv')
    df_unique.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"处理完成！")
    print(f"原始数据条数: {len(df)}")
    print(f"去重后数据条数: {len(df_unique)}")

if __name__ == "__main__":
    process_zhihu_json_files() 