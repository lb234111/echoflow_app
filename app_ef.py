from flask import Blueprint, render_template
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line
from flask.json import jsonify
import pyecharts
print('pyecharts version in app2 :',pyecharts.__version__)

# 使用flask中的蓝图，每个.py文件对应一个html页面。分多个.py文件容易修改和扩展
bp = Blueprint('echoflow', __name__)

@bp.route("/echoflow")
def echoflow():
    return render_template('echoflow.html')

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
                         xaxis_opts=(opts.AxisOpts(type_="value",name='迭代轮次',name_location='center',min_='dataMin',name_gap=25)),
                         yaxis_opts=(opts.AxisOpts(type_="value",min_='dataMin')))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    return line

display_df = pd.read_csv('files/echoflow.csv',header=None)

### tps
@bp.route("/ef_tps")
def ef_tps():   
    reward_l = line_base(display_df,'Tps',1) #第2列是tps的值
    return reward_l.dump_options_with_quotes()

tps_idx=1
@bp.route('/ef_tps_dynamicdata')
def ef_tps_dynamicdata():
    global tps_idx
    if tps_idx == display_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        tps_idx,x,y = next_xy(display_df,tps_idx,0,1)#第0列是时间，第2列是tps的值
        print("reward:x,y:",x,y)
        return jsonify({"x_data": x, "y_data": y})

### BatchCreateTimeout
@bp.route("/ef_BatchCreateTimeout")
def ef_BatchCreateTimeout():   
    reward_l = line_base(display_df,'BatchCreateTimeout',2) 
    return reward_l.dump_options_with_quotes()

BatchCreateTimeout_idx=1
@bp.route('/ef_BatchCreateTimeout_dynamicdata')
def ef_BatchCreateTimeout_dynamicdata():
    global BatchCreateTimeout_idx
    if BatchCreateTimeout_idx == display_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        BatchCreateTimeout_idx,x,y = next_xy(display_df,BatchCreateTimeout_idx,0,2)
        print("reward:x,y:",x,y)
        return jsonify({"x_data": x, "y_data": y})

### BatchMaxSize
@bp.route("/ef_BatchMaxSize")
def ef_BatchMaxSize():   
    reward_l = line_base(display_df,'BatchMaxSize',3) 
    return reward_l.dump_options_with_quotes()

BatchMaxSize_idx=1
@bp.route('/ef_BatchMaxSize_dynamicdata')
def ef_BatchMaxSize_dynamicdata():
    global BatchMaxSize_idx
    if BatchMaxSize_idx == display_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        BatchMaxSize_idx,x,y = next_xy(display_df,BatchMaxSize_idx,0,3)
        print("reward:x,y:",x,y)
        return jsonify({"x_data": x, "y_data": y})

### Connectors
@bp.route("/ef_Connectors")
def ef_Connectors():   
    reward_l = line_base(display_df,'Connectors',4) 
    return reward_l.dump_options_with_quotes()

Connectors_idx=1
@bp.route('/ef_Connectors_dynamicdata')
def ef_Connectors_dynamicdata():
    global Connectors_idx
    if Connectors_idx == display_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        Connectors_idx,x,y = next_xy(display_df,Connectors_idx,0,4)
        print("reward:x,y:",x,y)
        return jsonify({"x_data": x, "y_data": y})

### GossipRetransmission
@bp.route("/ef_GossipRetransmission")
def ef_GossipRetransmission():   
    reward_l = line_base(display_df,'GossipRetransmission',7) 
    return reward_l.dump_options_with_quotes()

GossipRetransmission_idx=1
@bp.route('/ef_GossipRetransmission_dynamicdata')
def ef_GossipRetransmission_dynamicdata():
    global GossipRetransmission_idx
    if GossipRetransmission_idx == display_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        GossipRetransmission_idx,x,y = next_xy(display_df,GossipRetransmission_idx,0,7)
        print("reward:x,y:",x,y)
        return jsonify({"x_data": x, "y_data": y})

### HeartbeatInterval
@bp.route("/ef_HeartbeatInterval")
def ef_HeartbeatInterval():   
    reward_l = line_base(display_df,'HeartbeatInterval',8) 
    return reward_l.dump_options_with_quotes()

HeartbeatInterval_idx=1
@bp.route('/ef_HeartbeatInterval_dynamicdata')
def ef_HeartbeatInterval_dynamicdata():
    global HeartbeatInterval_idx
    if HeartbeatInterval_idx == display_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        HeartbeatInterval_idx,x,y = next_xy(display_df,HeartbeatInterval_idx,0,8)
        print("reward:x,y:",x,y)
        return jsonify({"x_data": x, "y_data": y})

### MaxPeerCountAllow
@bp.route("/ef_MaxPeerCountAllow")
def ef_MaxPeerCountAllow():   
    reward_l = line_base(display_df,'MaxPeerCountAllow',9) 
    return reward_l.dump_options_with_quotes()

MaxPeerCountAllow_idx=1
@bp.route('/ef_MaxPeerCountAllow_dynamicdata')
def ef_MaxPeerCountAllow_dynamicdata():
    global MaxPeerCountAllow_idx
    if MaxPeerCountAllow_idx == display_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        MaxPeerCountAllow_idx,x,y = next_xy(display_df,MaxPeerCountAllow_idx,0,9)
        print("reward:x,y:",x,y)
        return jsonify({"x_data": x, "y_data": y})

### OpportunisticGraftPeers
@bp.route("/ef_OpportunisticGraftPeers")
def ef_OpportunisticGraftPeers():   
    reward_l = line_base(display_df,'OpportunisticGraftPeers',10) 
    return reward_l.dump_options_with_quotes()

OpportunisticGraftPeers_idx=1
@bp.route('/ef_OpportunisticGraftPeers_dynamicdata')
def ef_OpportunisticGraftPeers_dynamicdata():
    global OpportunisticGraftPeers_idx
    if OpportunisticGraftPeers_idx == display_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        OpportunisticGraftPeers_idx,x,y = next_xy(display_df,OpportunisticGraftPeers_idx,0,10)
        print("reward:x,y:",x,y)
        return jsonify({"x_data": x, "y_data": y})

### TBFT_propose_delta_timeout
@bp.route("/ef_TBFT_propose_delta_timeout")
def ef_TBFT_propose_delta_timeout():   
    reward_l = line_base(display_df,'TBFT_propose_delta_timeout',11) 
    return reward_l.dump_options_with_quotes()

TBFT_propose_delta_timeout_idx=1
@bp.route('/ef_TBFT_propose_delta_timeout_dynamicdata')
def ef_TBFT_propose_delta_timeout_dynamicdata():
    global TBFT_propose_delta_timeout_idx
    if TBFT_propose_delta_timeout_idx == display_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        TBFT_propose_delta_timeout_idx,x,y = next_xy(display_df,TBFT_propose_delta_timeout_idx,0,11)
        print("reward:x,y:",x,y)
        return jsonify({"x_data": x, "y_data": y})

### TBFT_propose_timeout
@bp.route("/ef_TBFT_propose_timeout")
def ef_TBFT_propose_timeout():   
    reward_l = line_base(display_df,'TBFT_propose_timeout',12) 
    return reward_l.dump_options_with_quotes()

TBFT_propose_timeout_idx=1
@bp.route('/ef_TBFT_propose_timeout_dynamicdata')
def ef_TBFT_propose_timeout_dynamicdata():
    global TBFT_propose_timeout_idx
    if TBFT_propose_timeout_idx == display_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        TBFT_propose_timeout_idx,x,y = next_xy(display_df,TBFT_propose_timeout_idx,0,12)
        print("reward:x,y:",x,y)
        return jsonify({"x_data": x, "y_data": y})

### block_tx_capacity
@bp.route("/ef_block_tx_capacity")
def ef_block_tx_capacity():   
    reward_l = line_base(display_df,'block_tx_capacity',13) 
    return reward_l.dump_options_with_quotes()

block_tx_capacity_idx=1
@bp.route('/ef_block_tx_capacity_dynamicdata')
def ef_block_tx_capacity_dynamicdata():
    global block_tx_capacity_idx
    if block_tx_capacity_idx == display_df.shape[0]-1:
        return jsonify({"x_data": '', "y_data": ''})
    else:
        block_tx_capacity_idx,x,y = next_xy(display_df,block_tx_capacity_idx,0,13)
        print("reward:x,y:",x,y)
        return jsonify({"x_data": x, "y_data": y})