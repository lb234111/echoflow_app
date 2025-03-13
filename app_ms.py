from flask import Blueprint, render_template, Flask, request, jsonify
from flask import send_file
import json
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.charts import HeatMap
import numpy as np
from flask.json import jsonify
import pyecharts

print('pyecharts version in app2 :',pyecharts.__version__)

# 使用flask中的蓝图，每个.py文件对应一个html页面。分多个.py文件容易修改和扩展
bp = Blueprint('mitosis', __name__)


def create_heatmap(data):
    x_axis = sorted(set(key.split('->')[0] for key in data.keys()))  
    y_axis = sorted(set(key.split('->')[1] for key in data.keys()))  
    x_labels = [f"分片{int(num) - 1000}" for num in x_axis]  
    y_labels = [f"分片{int(num) - 1000}" for num in y_axis]
    values = [
        [x_axis.index(key.split('->')[0]), y_axis.index(key.split('->')[1]), round(data[key], 2)]  
        for key in data.keys()
    ]

    heatmap = (
        HeatMap()
        .add_xaxis(x_labels)
        .add_yaxis('',y_labels, values)
        
        .set_global_opts(title_opts=opts.TitleOpts(title="跨片时延热力图(单位s)",title_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF")),
                        xaxis_opts=opts.AxisOpts(name="源分片",axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#FFFFFF", width=3))),  
                        yaxis_opts=opts.AxisOpts(name="目的分片",axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#FFFFFF", width=3))),
                        visualmap_opts=opts.VisualMapOpts(max_=1, min_=0, is_show=True,
                                                            range_color=["#00ff80","#42C090","#69c0ff","#0050b3"] )
                        )
    ) 

    return json.loads(heatmap.dump_options()) 

def create_heatmap2():
    x_axis = [f"分片{i+1}" for i in range(1000)]
    y_axis = [f"分片{i+1}" for i in range(1000)]

    # 生成所需的数据格式
    values = [[i, j, 1] for i in range(1000) for j in range(1000) if i!=j]

    # 创建热力图
    heatmap = (
        HeatMap()
        .add_xaxis(x_axis)
        .add_yaxis("", y_axis, values)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="1000个分片相互连通图",title_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF")),
            xaxis_opts=opts.AxisOpts(name="源分片", is_show=True,axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#FFFFFF", width=3))),
            yaxis_opts=opts.AxisOpts(name="目的分片", is_show=True,axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#FFFFFF", width=3))),
            visualmap_opts=opts.VisualMapOpts(
                max_=1,
                min_=0,
                is_show=True,
                range_color=[ "#ff4500", "#ffd700", "#42C090"]  
            ),
            datazoom_opts=[
                opts.DataZoomOpts(type_="slider", xaxis_index=0,  is_show=True, range_start=0, range_end=2, pos_top="95%",), 
                opts.DataZoomOpts(type_="slider", yaxis_index=0,  is_show=True, range_start=0, range_end=2, pos_top="93%",)  
            ]
        )
    )

    return json.loads(heatmap.dump_options())


@bp.route("/mitosis")
def mitosis():
    return render_template('mitosis.html')

@bp.route('/show_image')
def show_image():
    image_path = './files/ms2.png'
    return send_file(image_path, mimetype='image/png')

@bp.route("/ms_heatmap")
def heatmap_data():
    with open('./files/Mitosis_data.json', 'r') as f:
        data = json.load(f)
    chart_options = create_heatmap(data)
    return jsonify(chart_options)  

@bp.route("/ms_heatmap2")
def heatmap_data2():
    chart_options = create_heatmap2()
    return jsonify(chart_options)  

@bp.route("/ms_bar1")
def bar_chart_data1():
    option = {
        "title": {"text": "负载均衡协议的总体通量对比图",
                  "textStyle": {
                       "color": "#FFFFFF",  
                       "fontSize": 20     
        }},
        "tooltip": {},
        "legend": {  
            "data": ["现有状态分片方案（账户模型）", "高可扩展动态多中继分片系统"],  
            "orient": "horizontal",
            "textStyle": {
                "color": "#FFFFFF"  
            },
            "top": "5%"
        },
        "xAxis": {
            "data": ["平均吞吐量"],
            "axisLabel": {
                "align": "center",
                "fontSize": 18,
                "color": "#FFFFFF" 
            },
            "boundaryGap": True  
        },
        "yAxis": {"axisLabel": {
                "color": "#FFFFFF" 
        }},
        "series": [
            {
                "name": "现有状态分片方案（账户模型）",
                "type": "bar",
                "data": [1363.67],  
                "itemStyle": {
                    "color": "#69c0ff"  
                },
                "barWidth": "20%",  
                "label": {  
                    "show": True,
                    "position": "top",
                    "formatter": "{c}txs/sec"   
                }
            },
            {
                "name": "高可扩展动态多中继分片系统",
                "type": "bar",
                "data": [2284.01],  
                "itemStyle": {
                    "color": "#19A576"  
                },
                "barWidth": "20%",  
                "label": {  
                    "show": True,
                    "position": "top",
                    "formatter": "{c}txs/sec"   
                }
            }
        ],
        "barCategoryGap": "30%",
        "graphic": [ 
            {
                "type": "text",
                "style": {
                    "text": "总体通量提升67.49%", 
                    "textAlign": "center",
                    "fill": "#FFFFFF",
                    "fontSize": 24  
                },
                "left": "center",
                "top": "55%",
                "z": 10
            }
        ]
    }
    return jsonify(option)

@bp.route("/ms_bar2")
def bar_chart_data2():
    option = {
        "title": {"text": "交易社区的聚类后链间交易占比对比图",
                  "textStyle": {
                       "color": "#FFFFFF",  
                       "fontSize": 20      
        }},
        "tooltip": {},
        "legend": { 
            "data": ["现有状态分片方案（账户模型）", "高可扩展动态多中继分片系统"],  
            "orient": "horizontal",
            "textStyle": {
                "color": "#FFFFFF"  
            },
            "top": "5%"
        },
        "xAxis": {
            "data": ["链间交易占比"],
            "axisLabel": {
                "align": "center",
                "fontSize": 18,
                "color": "#FFFFFF" 
            },
            "boundaryGap": True  
        },
        "yAxis": {"axisLabel": {
                "color": "#FFFFFF" 
        }},
        "series": [
            {
                "name": "现有状态分片方案（账户模型）",
                "type": "bar",
                "data": [93.82], 
                "itemStyle": {
                    "color": "#69c0ff"  
                },
                "barWidth": "20%",  
                "label": {  
                    "show": True,
                    "position": "top",
                    "formatter": "{c}%"  
                }
            },
            {
                "name": "高可扩展动态多中继分片系统",
                "type": "bar",
                "data": [10.79],  
                "itemStyle": {
                    "color": "#19A576"  
                },
                "barWidth": "20%",  
                "label": {  
                    "show": True,
                    "position": "top",
                    "formatter": "{c}%"  
                }
            }
        ],
        "barCategoryGap": "30%",
        "graphic": [ 
            {
                "type": "text",
                "style": {
                    "text": "链间交易占比降低83.03%", 
                    "textAlign": "center",
                    "fill": "#FFFFFF", 
                    "fontSize": 24  
                },
                "left": "center",
                "top": "55%",
                "z": 10
            }
        ]  
    }
    return jsonify(option)











