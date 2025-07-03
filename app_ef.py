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
    line = (
        Line()
        .add_xaxis(xaxis_data=df.iloc[:2,0][-5:].tolist())  # 第0列是时间
        .add_yaxis(series_name=line_name,
                y_axis=df.iloc[:2,n].tolist(),
                is_smooth=True,
                # markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min"),opts.MarkPointItem(type_="max")]),
                )
        .set_global_opts(
            legend_opts=opts.LegendOpts(
                pos_left="10%", 
                pos_top="5%",
                textstyle_opts=opts.TextStyleOpts(
                    color="#FFFFFF",   
                    font_size=10,     
                    font_weight="bold"  
                )
            ),
            # title_opts=opts.TitleOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(
                type_="value",
                name='迭代轮次',
                name_location='center',
                min_='dataMin',
                name_gap=25,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#FFFFFF", width=1)   
                )
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                min_='dataMin',
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#FFFFFF", width=1)  
                )
            )
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(
                color="#32CD32",  # 设置折线颜色为绿色
                width=3        
            )
        )
    )
    return line




display_df = pd.read_csv('files/echoflow.csv',header=None)

tps_idx=1
tps_l=[]
### tps
@bp.route("/ef_tps")
def ef_tps(): 
    global tps_idx 
    global tps_l
    reward_l = line_base(display_df,'交易吞吐量 Tps',1) #第2列是tps的值
    return reward_l.dump_options_with_quotes()

@bp.route('/ef_tps_dynamicdata')
def ef_tps_dynamicdata():
    global tps_idx
    global tps_l
    if tps_idx == display_df.shape[0]-1:
        return jsonify({"data": tps_l})
    else:
        tps_idx,x,y = next_xy(display_df,tps_idx,0,1)#第0列是时间，第2列是tps的值
        print("reward:x,y:",x,y)
        tps_l.append([x,y])
        return jsonify({"data": tps_l})

### BatchCreateTimeout
BatchCreateTimeout_idx=1
BatchCreateTimeout_l=[]
@bp.route("/ef_BatchCreateTimeout")
def ef_BatchCreateTimeout():
    global BatchCreateTimeout_idx     
    reward_l = line_base(display_df,'批次创建时间 BatchCreateTimeout (网络层)',2) 
    return reward_l.dump_options_with_quotes()

@bp.route('/ef_BatchCreateTimeout_dynamicdata')
def ef_BatchCreateTimeout_dynamicdata():
    global BatchCreateTimeout_idx
    if BatchCreateTimeout_idx == display_df.shape[0]-1:
        return jsonify({"data": BatchCreateTimeout_l})
    else:
        BatchCreateTimeout_idx,x,y = next_xy(display_df,BatchCreateTimeout_idx,0,2)
        print("reward:x,y:",x,y)
        BatchCreateTimeout_l.append([x,y])
        return jsonify({"data": BatchCreateTimeout_l})

### BatchMaxSize
BatchMaxSize_idx=1
BatchMaxSize_l=[]
@bp.route("/ef_BatchMaxSize")
def ef_BatchMaxSize():   
    global BatchMaxSize_idx  
    reward_l = line_base(display_df,'批次大小 BatchMaxSize (网络层)',3) 
    return reward_l.dump_options_with_quotes()

@bp.route('/ef_BatchMaxSize_dynamicdata')
def ef_BatchMaxSize_dynamicdata():
    global BatchMaxSize_idx
    if BatchMaxSize_idx == display_df.shape[0]-1:
        return jsonify({"data": BatchMaxSize_l})
    else:
        BatchMaxSize_idx,x,y = next_xy(display_df,BatchMaxSize_idx,0,3)
        print("reward:x,y:",x,y)
        BatchMaxSize_l.append([x,y])
        return jsonify({"data": BatchMaxSize_l})

### Connectors
Connectors_idx=1
Connectors_l=[]
@bp.route("/ef_Connectors")
def ef_Connectors(): 
    global Connectors_idx   
    reward_l = line_base(display_df,'活跃连接数 Connectors (网络层)',4) 
    return reward_l.dump_options_with_quotes()

@bp.route('/ef_Connectors_dynamicdata')
def ef_Connectors_dynamicdata():
    global Connectors_idx
    if Connectors_idx == display_df.shape[0]-1:
        return jsonify({"data": Connectors_l})
    else:
        Connectors_idx,x,y = next_xy(display_df,Connectors_idx,0,4)
        print("reward:x,y:",x,y)
        Connectors_l.append([x,y])
        return jsonify({"data": Connectors_l})

### GossipRetransmission
GossipRetransmission_idx=1
GossipRetransmission_l=[]
@bp.route("/ef_GossipRetransmission")
def ef_GossipRetransmission():  
    global GossipRetransmission_idx   
    reward_l = line_base(display_df,'消息重传次数 GossipRetransmission (网络层)',7) 
    return reward_l.dump_options_with_quotes()

@bp.route('/ef_GossipRetransmission_dynamicdata')
def ef_GossipRetransmission_dynamicdata():
    global GossipRetransmission_idx
    if GossipRetransmission_idx == display_df.shape[0]-1:
        return jsonify({"data": GossipRetransmission_l})
    else:
        GossipRetransmission_idx,x,y = next_xy(display_df,GossipRetransmission_idx,0,7)
        print("reward:x,y:",x,y)
        GossipRetransmission_l.append([x,y])
        return jsonify({"data": GossipRetransmission_l})

### HeartbeatInterval
HeartbeatInterval_idx=1
HeartbeatInterval_l=[]
@bp.route("/ef_HeartbeatInterval")
def ef_HeartbeatInterval():  
    global HeartbeatInterval_idx 
    reward_l = line_base(display_df,'心跳间隔 HeartbeatInterval (网络层)',8) 
    return reward_l.dump_options_with_quotes()

@bp.route('/ef_HeartbeatInterval_dynamicdata')
def ef_HeartbeatInterval_dynamicdata():
    global HeartbeatInterval_idx
    if HeartbeatInterval_idx == display_df.shape[0]-1:
        return jsonify({"data": HeartbeatInterval_l})
    else:
        HeartbeatInterval_idx,x,y = next_xy(display_df,HeartbeatInterval_idx,0,8)
        print("reward:x,y:",x,y)
        HeartbeatInterval_l.append([x,y])
        return jsonify({"data": HeartbeatInterval_l})

### MaxPeerCountAllow
MaxPeerCountAllow_idx=1
MaxPeerCountAllow_l=[]


@bp.route("/ef_MaxPeerCountAllow")
def ef_MaxPeerCountAllow(): 
    global MaxPeerCountAllow_idx 
    reward_l = line_base(display_df,'最大邻居节点数 MaxPeerCountAllow (网络层)',9) 
    return reward_l.dump_options_with_quotes()

@bp.route('/ef_MaxPeerCountAllow_dynamicdata')
def ef_MaxPeerCountAllow_dynamicdata():
    global MaxPeerCountAllow_idx
    if MaxPeerCountAllow_idx == display_df.shape[0]-1:
        return jsonify({"data": MaxPeerCountAllow_l})
    else:
        MaxPeerCountAllow_idx,x,y = next_xy(display_df,MaxPeerCountAllow_idx,0,9)
        print("reward:x,y:",x,y)
        MaxPeerCountAllow_l.append([x,y])
        return jsonify({"data": MaxPeerCountAllow_l})

### OpportunisticGraftPeers
OpportunisticGraftPeers_idx=1
OpportunisticGraftPeers_l=[]
@bp.route("/ef_OpportunisticGraftPeers")
def ef_OpportunisticGraftPeers(): 
    global OpportunisticGraftPeers_idx   
    reward_l = line_base(display_df,'提议者提出区块数 OpportunisticGraftPeers (网络层)',10) 
    return reward_l.dump_options_with_quotes()

@bp.route('/ef_OpportunisticGraftPeers_dynamicdata')
def ef_OpportunisticGraftPeers_dynamicdata():
    global OpportunisticGraftPeers_idx
    if OpportunisticGraftPeers_idx == display_df.shape[0]-1:
        return jsonify({"data": OpportunisticGraftPeers_l})
    else:
        OpportunisticGraftPeers_idx,x,y = next_xy(display_df,OpportunisticGraftPeers_idx,0,10)
        print("reward:x,y:",x,y)
        OpportunisticGraftPeers_l.append([x,y])
        return jsonify({"data": OpportunisticGraftPeers_l})

### TBFT_propose_delta_timeout
TBFT_propose_delta_timeout_idx=1
TBFT_propose_delta_timeout_l=[]
@bp.route("/ef_TBFT_propose_delta_timeout")
def ef_TBFT_propose_delta_timeout():   
    global TBFT_propose_delta_timeout_idx 
    reward_l = line_base(display_df,'propose超时调整值 TBFT_propose_delta_timeout (共识层)',11) 
    return reward_l.dump_options_with_quotes()

@bp.route('/ef_TBFT_propose_delta_timeout_dynamicdata')
def ef_TBFT_propose_delta_timeout_dynamicdata():
    global TBFT_propose_delta_timeout_idx
    if TBFT_propose_delta_timeout_idx == display_df.shape[0]-1:
        return jsonify({"data": TBFT_propose_delta_timeout_l})
    else:
        TBFT_propose_delta_timeout_idx,x,y = next_xy(display_df,TBFT_propose_delta_timeout_idx,0,11)
        print("reward:x,y:",x,y)
        TBFT_propose_delta_timeout_l.append([x,y])
        return jsonify({"data": TBFT_propose_delta_timeout_l})

### TBFT_propose_timeout
TBFT_propose_timeout_idx=1
TBFT_propose_timeout_l=[]
@bp.route("/ef_TBFT_propose_timeout")
def ef_TBFT_propose_timeout():
    global TBFT_propose_timeout_idx   
    reward_l = line_base(display_df,'propose超时时间 TBFT_propose_timeout (共识层)',12) 
    return reward_l.dump_options_with_quotes()

@bp.route('/ef_TBFT_propose_timeout_dynamicdata')
def ef_TBFT_propose_timeout_dynamicdata():
    global TBFT_propose_timeout_idx
    if TBFT_propose_timeout_idx == display_df.shape[0]-1:
        return jsonify({"data": TBFT_propose_timeout_l})
    else:
        TBFT_propose_timeout_idx,x,y = next_xy(display_df,TBFT_propose_timeout_idx,0,12)
        print("reward:x,y:",x,y)
        TBFT_propose_timeout_l.append([x,y])
        return jsonify({"data": TBFT_propose_timeout_l})

### block_tx_capacity
block_tx_capacity_idx=1
block_tx_capacity_l=[]
@bp.route("/ef_block_tx_capacity")
def ef_block_tx_capacity(): 
    global block_tx_capacity_idx 
    reward_l = line_base(display_df,'区块大小 block_tx_capacity (存储层)',13) 
    return reward_l.dump_options_with_quotes()

@bp.route('/ef_block_tx_capacity_dynamicdata')
def ef_block_tx_capacity_dynamicdata():
    global block_tx_capacity_idx
    if block_tx_capacity_idx == display_df.shape[0]-1:
        return jsonify({"data": block_tx_capacity_l})
    else:
        block_tx_capacity_idx,x,y = next_xy(display_df,block_tx_capacity_idx,0,13)
        print("reward:x,y:",x,y)
        block_tx_capacity_l.append([x,y])
        return jsonify({"data": block_tx_capacity_l})