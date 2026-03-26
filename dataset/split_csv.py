import pandas as pd
import os

# 文件路径
input_file = "e:/项目/cccc/dataset/智联招聘人岗匹配/train_data/table2_jd.csv"
output_dir = "e:/项目/cccc/dataset/智联招聘人岗匹配/train_data/"

# 读取CSV（Tab分隔）
print("正在读取文件...")
df = pd.read_csv(input_file, sep='\t', on_bad_lines='skip')
total_rows = len(df)
print(f"总行数: {total_rows}")

# 计算分割点
part_size = total_rows // 3
remainder = total_rows % 3

# 分割数据
print("正在分割文件...")
for i in range(3):
    start_idx = i * part_size
    # 最后一部分包含余数
    end_idx = start_idx + part_size + (1 if i == 2 and remainder > 0 else 0)

    part_df = df.iloc[start_idx:end_idx]
    output_file = os.path.join(output_dir, f"table2_jd_part{i+1}.csv")

    part_df.to_csv(output_file, index=False)
    print(f"Part {i+1}: {len(part_df)} 行 -> {output_file}")

print("分割完成!")
