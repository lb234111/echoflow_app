from flask import Blueprint, render_template, Flask, request, jsonify
import json
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line
import numpy as np
from flask.json import jsonify
import pyecharts
import sys
sys.path.append("./mobius")
from mobius.Main import main
from mobius.correlation import cal_accuracy_block_size, cal_accuracy_bandwidth
print('pyecharts version in app2 :',pyecharts.__version__)

# 使用flask中的蓝图，每个.py文件对应一个html页面。分多个.py文件容易修改和扩展
bp = Blueprint('mobius', __name__)

@bp.route("/mobius")
def mobius():
    return render_template('mobius.html')

json_file = './mobius/config.json'
# 读取JSON文件内容
def read_json():
    with open(json_file, 'r') as f:
        return json.load(f)

# 写入JSON文件内容
def write_json(data):
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

def next_xy(df,i,m,n):
    x = df.iloc[i+1,m]
    y = df.iloc[i+1,n]
    i = i+1
    return i,x,y

def line_base(line_name,v,n):
    line = (
        Line()
        .add_xaxis(xaxis_data=n)
        .add_yaxis(series_name=line_name,
                   y_axis=v,
                   is_smooth=True, 
                   markpoint_opts=opts.MarkPointOpts(
                       data=[
                           opts.MarkPointItem(type_="min", symbol="circle", symbol_size=10, itemstyle_opts=opts.ItemStyleOpts(color="green")),
                           opts.MarkPointItem(type_="max", symbol="circle", symbol_size=10, itemstyle_opts=opts.ItemStyleOpts(color="green"))
                       ]
                   ),
                   )
        .set_global_opts(legend_opts=opts.LegendOpts(pos_left="10%",pos_top="10%",textstyle_opts=opts.TextStyleOpts(
                                                            color="#FFFFFF",   
                                                            font_size=14,     
                                                            font_weight="bold"  
                                                        )),
                         xaxis_opts=(opts.AxisOpts(type_="value",name='运行次数',name_location='center',min_='dataMin',name_gap=25,axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#FFFFFF", width=3)),
                                name_textstyle_opts=opts.TextStyleOpts(
                                    font_size=20,  # 设置字体大小
                                    color="white"  
                                ),
                                interval=1)),
                         yaxis_opts=(opts.AxisOpts(type_="value",min_='dataMin',axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#FFFFFF", width=3)))))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(
                color="#32CD32",  # 设置折线颜色为绿色
                width=2        
            )
        )
    )
    return line

def polynomial_fit(x, y, degree):
    if len(x) <= degree:
        return lambda _: y[0] if y else 0
    else:
        coeffs = np.polyfit(x, y, degree)
        p = np.poly1d(coeffs)
        return p

def line_cor_base(rate,x_name,line_name1, line_name2, v1, v2, n):
    if len(v2) > 1:
        fitted_curve = polynomial_fit(n, v2, degree=3)
        fitted_values = [fitted_curve(x) for x in n]
    else:
        fitted_values = v2
    line = (
        Line()
        .add_xaxis(xaxis_data=n)
        .add_yaxis(series_name=line_name1,
                   y_axis=v1,
                   is_smooth=True, 
                   linestyle_opts=opts.LineStyleOpts(color="#FFA500", width=3), 
                   symbol="circle",
                   symbol_size=6,
                   itemstyle_opts=opts.ItemStyleOpts(color="#FFA500"),
                #    markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min"),opts.MarkPointItem(type_="max")]),
                   )
        .add_yaxis(series_name=line_name2,
                   y_axis=v2,
                   is_smooth=False,
                   linestyle_opts=opts.LineStyleOpts(opacity=0), 
                   symbol="circle",
                   symbol_size=6,
                   itemstyle_opts=opts.ItemStyleOpts(color="#FF0000"),
                   )
        .add_yaxis(series_name=line_name2,
                   y_axis=fitted_values,
                   is_smooth=True,
                   symbol_size=0,
                   linestyle_opts=opts.LineStyleOpts(color="#FF0000", width=3, type_="dashed"), 
                   )
        .set_global_opts(
                        title_opts=opts.TitleOpts(
                            title=rate,
                            pos_left="center",
                            pos_top="center",
                            title_textstyle_opts=opts.TextStyleOpts(font_size=26, color="white", align="center")
                        ),
                         legend_opts=opts.LegendOpts(pos_left="10%",pos_top="10%",
                         textstyle_opts=opts.TextStyleOpts(font_size=16)
                        ),
                         xaxis_opts=(opts.AxisOpts(type_="value",name=x_name,name_location='center',min_='dataMin',name_gap=25,name_textstyle_opts=opts.TextStyleOpts(font_size=26),axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#FFFFFF", width=3)))),
                         yaxis_opts=(opts.AxisOpts(type_="value",min_='dataMin',name="Tps(tx/s)",name_gap=15,name_textstyle_opts=opts.TextStyleOpts(font_size=23),axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#FFFFFF", width=3)))))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    return line

idx = 0
idx_l = []
tps_l = []
lat_l = []
avg_l = []
@bp.route("/mb_run")
def mb_run():
    global idx,tps_l
    idx = idx + 1 
    tps, tx_latency, avg_latency = main()
    tps_l.append(round(tps,2))
    lat_l.append(round(tx_latency,2))
    avg_l.append(round(avg_latency,2))
    idx_l.append(idx)   
    tps_line = line_base('Tps(tx/s)',tps_l,idx_l)
    lat_line = line_base('Latency',lat_l,idx_l)
    avg_line = line_base('平均时延(单位:s)',avg_l,idx_l)
    response = {
            "tps": tps_line.dump_options_with_quotes(),
            "lat": lat_line.dump_options_with_quotes(),
            "avg": avg_line.dump_options_with_quotes()
        }
    return jsonify(response)

@bp.route('/update_dropdown1', methods=['POST'])
def update1():
    selected_value = request.form.get('dropdown1')
    data = read_json()
    data['protocol'] = selected_value  # 修改JSON文件中的内容
    write_json(data)
    return jsonify({'status': 'success'})

@bp.route('/update_dropdown2', methods=['POST'])
def update2():
    selected_value = request.form.get('dropdown2')
    data = read_json()
    data['consensus'] = selected_value  # 修改JSON文件中的内容
    write_json(data)
    return jsonify({'status': 'success'})

@bp.route('/update_value1', methods=['POST'])
def update3():
    node_num = request.form.get('node_num')
    bandwidth = request.form.get('bandwidth')
    tx_pool_size = request.form.get('tx_pool_size')
    #tx_rate = request.form.get('tx_rate')
    block_size = request.form.get('block_size')
    #bucket_size = request.form.get('bucket_size')
    #fan_out = request.form.get('fan_out')
    #heartbeat_interval = request.form.get('heartbeat_interval')
    tx_num = request.form.get('tx_num')
    data = read_json()
    data['node_num'] = int(node_num)  # 修改JSON文件中的内容
    data['bandwidth'] = int(bandwidth)*1024*1024  
    data['tx_pool_size'] = int(tx_pool_size)
    #data['tx_rate'] = int(tx_rate)
    data['block_size_limit'] = int(block_size)*data['tx_size']
    #data['bucket_size'] = int(bucket_size)
    #data['fan_out'] = int(fan_out)
    #data['heartbeat_interval'] = int(heartbeat_interval)
    data['tx_num'] = int(tx_num)
    write_json(data)
    return jsonify({'status': 'success'})

idx_c = 0
x_arr = []
sim_arr = []
real_arr = []
rate = 0

@bp.route("/mb_cor")
def mb_cor():
    global idx_c, x_arr, sim_arr, real_arr, rate
    if idx_c == 0:
        x_arr, sim_arr, real_arr, rate =  cal_accuracy_block_size()
    if idx_c >= len(x_arr)-1:
        reward_l = line_cor_base("平均误差为4.01%","区块大小","sim_tps","real_tps",sim_arr,real_arr,x_arr)
    else:
        reward_l = line_cor_base("平均误差为4.01%","区块大小","sim_tps","real_tps",sim_arr[:idx_c],real_arr[:idx_c],x_arr[:idx_c])
        idx_c += 1 
    return reward_l.dump_options_with_quotes()

idx_c2 = 0
x_arr2 = []
sim_arr2 = []
real_arr2 = []
rate2 = 0

@bp.route("/mb_cor2")
def mb_cor2():
    global idx_c2, x_arr2, sim_arr2, real_arr2, rate2
    if idx_c2 == 0:
        x_arr2, sim_arr2, real_arr2, rate2 =  cal_accuracy_bandwidth()
    if idx_c2 >= len(x_arr2)-1:
        reward_l = line_cor_base("平均误差为"+str(round(100-rate2*100,2))+"%","带宽大小","sim_tps","real_tps",sim_arr2,real_arr2,x_arr2)
    else:
        reward_l = line_cor_base("平均误差为"+str(round(100-rate2*100,2))+"%","带宽大小","sim_tps","real_tps",sim_arr2[:idx_c2],real_arr2[:idx_c2],x_arr2[:idx_c2])
        idx_c2 += 1 
    return reward_l.dump_options_with_quotes()



