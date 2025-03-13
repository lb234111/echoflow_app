from flask import Flask, render_template, request
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Grid, Pie, Tab
from flask.json import jsonify
from random import randrange
from pyecharts.commons.utils import JsCode
import pyecharts
print('pyecharts version in app1 :',pyecharts.__version__)

import app2 as a2

app = Flask(__name__, template_folder="templates",static_folder="resource")
app.register_blueprint(a2.bp)

# 强化学习
import app_rl as a_rl
app.register_blueprint(a_rl.bp)

# 性能框架
import app_ef as a_ef
app.register_blueprint(a_ef.bp)

# 模拟器
import app_mb as a_mb
app.register_blueprint(a_mb.bp)

# 1000分片
import app_ms as a_ms
app.register_blueprint(a_ms.bp)



@app.route("/")
def index():
  return render_template("main_content.html")


# 返回dataframe的下一行的第m、n列数据
def next_xy(df,i,m,n):
    x = df.iloc[i+1,m]
    y = df.iloc[i+1,n]
    i = i+1
    return i,x,y
    
# 根据all_df的第0列和第n列的前2行数据，初始化一条line，
def line_base(df,line_name,n):
    # print('rows data:',df.iloc[:,0])
    line = (
        Line()
        .add_xaxis(xaxis_data=df.iloc[:2,0][-5:].tolist())#第0列是时间
        .add_yaxis(series_name=line_name,
                   y_axis=df.iloc[:2,n].tolist(),
                   is_smooth=True, 
                #    markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min"),opts.MarkPointItem(type_="max")]),
                   )
        .set_global_opts(legend_opts=opts.LegendOpts(pos_left="10%",pos_top="10%"),
                         xaxis_opts=(opts.AxisOpts(type_="time",name='时间戳',name_location='center',min_='dataMin',name_gap=25)),
                         yaxis_opts=(opts.AxisOpts(type_="value",min_='dataMin')))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    return line


all_df = pd.read_csv('files/res0.csv') #包含微观指标的文件


# ################################# cpu_use_rate的曲线 ############################
@app.route("/cpu_use_rate")
def cpu_use_rate():
    cpu_l = line_base(all_df,'CPU利用率',1) #第1列是CPU利用率的值
    return cpu_l.dump_options_with_quotes()

cpu_use_rate_idx=3
@app.route('/cpu_use_rate_dynamicdata')
def cpu_use_rate_dynamicdata():
    global cpu_use_rate_idx
    if cpu_use_rate_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        cpu_use_rate_idx,x,y = next_xy(all_df,cpu_use_rate_idx,0,1) #第0列是时间，第1列是CPU利用率的值
        # x=all_df.iloc[cpu_use_rate_idx+1,0]
        # y=all_df.iloc[cpu_use_rate_idx+1,1]
        # cpu_use_rate_idx = cpu_use_rate_idx + 1
        # print("cpu_use_rate:x,y:",x,y)
        return jsonify({"x_data": x, "y_data": y})




# ################################# memory_use_rate的曲线 ############################
@app.route("/memory_use_rate")
def memory_use_rate():
    l = line_base(all_df,'内存利用率',2)#第2列是CPU利用率的值
    return l.dump_options_with_quotes()

memory_use_rate_idx=3
@app.route("/memory_use_rate_dynamicdata")
def memory_use_rate_dynamicdata():
    global memory_use_rate_idx
    print('memory_use_rate_idx:',memory_use_rate_idx)
    if memory_use_rate_idx == all_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        memory_use_rate_idx,x,y = next_xy(all_df,memory_use_rate_idx,0,2) #第0列是时间，第2列是 memory 利用率的值
        # print("memory_use_rate_idx,x,y:",memory_use_rate_idx,x,y)
        return jsonify({"x_data": x, "y_data": y})












if __name__=='__main__':
    app.run(debug=True)