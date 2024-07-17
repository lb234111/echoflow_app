from flask import Blueprint, render_template
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line
from flask.json import jsonify
import pyecharts
print('pyecharts version in app2 :',pyecharts.__version__)

# 使用flask中的蓝图，每个.py文件对应一个html页面。分多个.py文件容易修改和扩展
bp = Blueprint('rl', __name__)

# #################################   强化学习的曲线 ############################
@bp.route("/reinforcement_learning")
def reinforcement_learning():
    return render_template('reinforcement_learning.html')

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
                         xaxis_opts=(opts.AxisOpts(type_="value",name='时间戳',name_location='center',min_='dataMin',name_gap=25)),
                         yaxis_opts=(opts.AxisOpts(type_="value",min_='dataMin')))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    return line

display_df = pd.read_csv('files/res10.csv',header=None)



### reward
@bp.route("/rl_reward")
def rl_reward():   
    reward_l = line_base(display_df,'Reward',1) #第1列是reward的值
    return reward_l.dump_options_with_quotes()

reward_idx=3
@bp.route('/rl_reward_dynamicdata')
def rl_reward_dynamicdata():
    global reward_idx
    if reward_idx == display_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        reward_idx,x,y = next_xy(display_df,reward_idx,0,1)#第0列是时间，第1列是reward的值
        print("reward:x,y:",x,y)
        return jsonify({"x_data": x, "y_data": y})


### TPS
@bp.route("/rl_tps")
def rl_tps():   
    tps_l = line_base(display_df,'TPS',2)
    return tps_l.dump_options_with_quotes()

tps_idx=3
@bp.route('/rl_tps_dynamicdata')
def rl_tps_dynamicdata():
    global tps_idx
    if tps_idx == display_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        tps_idx,x,y = next_xy(display_df,tps_idx,0,2)#第0列是时间，第2列是TPS的值
        print("tps:x,y:",x,y)
        return jsonify({"x_data": x, "y_data": y})


### NTL
@bp.route("/rl_ntl")
def rl_ntl():   
    ntl_l = line_base(display_df,'NTL',3)
    return ntl_l.dump_options_with_quotes()

ntl_idx=3
@bp.route('/rl_ntl_dynamicdata')
def rl_ntl_dynamicdata():
    global ntl_idx
    if ntl_idx == display_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        ntl_idx,x,y = next_xy(display_df,ntl_idx,0,3)#第0列是时间，第3列是NTL的值



### C1
@bp.route("/rl_c1")
def rl_c1():   
    c1_l = line_base(display_df, 'C1', 4)  # 第4列是C1的值
    return c1_l.dump_options_with_quotes()

c1_idx = 3
@bp.route('/rl_c1_dynamicdata')
def rl_c1_dynamicdata():
    global c1_idx
    if c1_idx == display_df.shape[0] - 1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        c1_idx, x, y = next_xy(display_df, c1_idx, 0, 4)  # 第0列是时间，第4列是C1的值
        print("c1:x,y:", x, y)
        return jsonify({"x_data": x, "y_data": y})

### C2
@bp.route("/rl_c2")
def rl_c2():   
    c2_l = line_base(display_df, 'C2', 5)  # 第5列是C2的值
    return c2_l.dump_options_with_quotes()

c2_idx = 3
@bp.route('/rl_c2_dynamicdata')
def rl_c2_dynamicdata():
    global c2_idx
    if c2_idx == display_df.shape[0] - 1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        c2_idx, x, y = next_xy(display_df, c2_idx, 0, 5)  # 第0列是时间，第5列是C2的值
        print("c2:x,y:", x, y)
        return jsonify({"x_data": x, "y_data": y})


### C3
@bp.route("/rl_c3")
def rl_c3():   
    c3_l = line_base(display_df, 'C3', 6)  # 第6列是C3的值
    return c3_l.dump_options_with_quotes()

c3_idx = 3
@bp.route('/rl_c3_dynamicdata')
def rl_c3_dynamicdata():
    global c3_idx
    if c3_idx == display_df.shape[0] - 1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        c3_idx, x, y = next_xy(display_df, c3_idx, 0, 6)  # 第0列是时间，第6列是C3的值
        print("c3:x,y:", x, y)
        return jsonify({"x_data": x, "y_data": y})

### C4
@bp.route("/rl_c4")
def rl_c4():   
    c4_l = line_base(display_df, 'C4', 7)  # 第7列是C4的值
    return c4_l.dump_options_with_quotes()

c4_idx = 3
@bp.route('/rl_c4_dynamicdata')
def rl_c4_dynamicdata():
    global c4_idx
    if c4_idx == display_df.shape[0] - 1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        c4_idx, x, y = next_xy(display_df, c4_idx, 0, 7)  # 第0列是时间，第7列是C4的值
        print("c4:x,y:", x, y)
        return jsonify({"x_data": x, "y_data": y})



### C5
@bp.route("/rl_c5")
def rl_c5():   
    c5_l = line_base(display_df, 'C5', 8)  # 第8列是C5的值
    return c5_l.dump_options_with_quotes()

c5_idx = 3
@bp.route('/rl_c5_dynamicdata')
def rl_c5_dynamicdata():
    global c5_idx
    if c5_idx == display_df.shape[0] - 1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        c5_idx, x, y = next_xy(display_df, c5_idx, 0, 8)  # 第0列是时间，第8列是C5的值
        print("c5:x,y:", x, y)
        return jsonify({"x_data": x, "y_data": y})


### C6
@bp.route("/rl_c6")
def rl_c6():   
    c6_l = line_base(display_df, 'C6', 9)  # 第9列是C6的值
    return c6_l.dump_options_with_quotes()

c6_idx = 3
@bp.route('/rl_c6_dynamicdata')
def rl_c6_dynamicdata():
    global c6_idx
    if c6_idx == display_df.shape[0] - 1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        c6_idx, x, y = next_xy(display_df, c6_idx, 0, 9)  # 第0列是时间，第9列是C6的值
        print("c6:x,y:", x, y)
        return jsonify({"x_data": x, "y_data": y})

### C7
@bp.route("/rl_c7")
def rl_c7():   
    c7_l = line_base(display_df, 'C7', 10)  # 第9列是C6的值
    return c7_l.dump_options_with_quotes()

c7_idx = 3
@bp.route('/rl_c7_dynamicdata')
def rl_c7_dynamicdata():
    global c7_idx
    if c7_idx == display_df.shape[0] - 1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        c7_idx, x, y = next_xy(display_df, c7_idx, 0, 10)  # 第0列是时间，第10列是C7的值
        print("c7:x,y:", x, y)
        return jsonify({"x_data": x, "y_data": y})


### C8
@bp.route("/rl_c8")
def rl_c8():   
    c8_l = line_base(display_df, 'C8', 11)  # 第11列是C8的值
    return c8_l.dump_options_with_quotes()

c8_idx = 3
@bp.route('/rl_c8_dynamicdata')
def rl_c8_dynamicdata():
    global c8_idx
    if c8_idx == display_df.shape[0] - 1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        c8_idx, x, y = next_xy(display_df, c8_idx, 0, 11)  # 第0列是时间，第11列是C8的值
        print("c8:x,y:", x, y)
        return jsonify({"x_data": x, "y_data": y})

