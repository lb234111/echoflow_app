from flask import Blueprint, render_template
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line
from flask.json import jsonify
import pyecharts
print('pyecharts version in app2 :',pyecharts.__version__)

# 使用flask中的蓝图，每个.py文件对应一个html页面。分多个.py文件容易修改和扩展
bp = Blueprint('entropy', __name__)

# #################################   熵的曲线 ############################
@bp.route("/changanlian_metric_2")
def changanlian_metric_2():
    return render_template('changanlian_metric_2.html')


entropy_df = pd.read_csv('files/entropy_list.txt',header=None)

@bp.route("/entropy")
def entropy():   
    line = (
            Line()
            .add_xaxis(xaxis_data=entropy_df.iloc[0,:3].tolist())
            .add_yaxis(series_name='entropy value',
                    y_axis=entropy_df.iloc[1,:3].tolist(),
                    is_smooth=True, 
                    # markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min"),opts.MarkPointItem(type_="max")]),
                    )
            .set_global_opts(legend_opts=opts.LegendOpts(pos_left="10%",pos_top="10%"),
                            xaxis_opts=(opts.AxisOpts(type_="value",name='时间戳',name_location='center',min_='dataMin',name_gap=25)),
                            yaxis_opts=(opts.AxisOpts(type_="value",min_='dataMin')))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        )

    return line.dump_options_with_quotes()

@bp.route("/entropy_line_all")
def entropy_line_all():
    line = (
            Line()
            .add_xaxis(xaxis_data=entropy_df.iloc[0,:entropy_idx].tolist())
            .add_yaxis(series_name='entropy value',
                    y_axis=entropy_df.iloc[1,:entropy_idx].tolist(),
                    is_smooth=True,
                    markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min"),opts.MarkPointItem(type_="max")]),
                    )
            .set_global_opts(legend_opts=opts.LegendOpts(pos_left="10%",pos_top="10%"),
                            xaxis_opts=(opts.AxisOpts(type_="value",name='时间戳',name_location='center',min_='dataMin',name_gap=25)),
                            yaxis_opts=(opts.AxisOpts(type_="value",min_='dataMin')))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        )
    return line.dump_options_with_quotes()


entropy_idx = 1
@bp.route("/entropy_dynamicdata")
def entropy_dynamicdata():
    global entropy_idx
    print('entropy_idx:',entropy_idx)
    if entropy_idx == entropy_df.shape[1]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        x=entropy_df.iloc[0,entropy_idx+1]
        y=entropy_df.iloc[1,entropy_idx+1]
        entropy_idx = entropy_idx + 1
        # print('xy:',x,y)

        return jsonify({"x_data": x, "y_data": y,"entropy_idx":entropy_idx})
