import pandas as pd

entropy_df = pd.read_csv('files/res0.csv')

print(entropy_df)
print(entropy_df.iloc[0,1])

print('############')
print(entropy_df.iloc[1,1])
print('############')

print(entropy_df.iloc[:3,0])



from pyecharts import options as opts
from pyecharts.charts import Line
# from pyecharts.components import TimeAxisComponent
 
# 假设有一组时间戳数据和对应的值
timestamps =  entropy_df.iloc[:4,0].tolist()
values = [10, 20, 30, 40]
 
# 将时间戳转换为 pyecharts 需要的格式
# timestamps = [TimeAxisComponent.parse_time(ts) for ts in timestamps]
 
# 创建折线图
line = (
    Line()
    .add_xaxis(timestamps)  # 设置横轴为时间轴
    .add_yaxis("系列名称", values)  # 添加数据系列
    .set_global_opts(
        title_opts=opts.TitleOpts(title="时间轴折线图示例"),  # 设置标题
        xaxis_opts=opts.AxisOpts(is_scale=True),  # 设置时间轴支持缩放
    )
    .render("time_line_example.html")  # 渲染图表到HTML文件
)