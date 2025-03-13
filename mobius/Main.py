# -*- coding = utf-8 -*-
from PBFT.PBFT_Event import *
from HotStuff.HotStuff_Event import *
from TBFT.TBFT_Event import *
from POW.POW_Event import *
import random
import config
import matplotlib.pyplot as plt
from PStatistics import PStatistics
from Net import Network
import os
import json


def random_generate_tx(node_num, tx_num, tx_rate):
    tx_list = []
    time = 0
    time_list = []
    for i in range(tx_num):
        time = time + (1 / float(tx_rate))
        time_list.append(time)
        sender = random.randint(0, node_num - 1)
        receiver = random.randint(0, node_num - 1)
        # size = random.randint(1, 10)
        # 单位字节，一般默认为512
        size = config.tx_size
        tx = Transaction(i, sender, receiver, size, time)
        tx_list.append(tx)
    return tx_list, time_list


def add_node_event(network, node_id, event):
    network.node[node_id].add_event(event)


def main():
    config_json = True
    if config_json:
        with open('./mobius/config.json','r',encoding='utf8')as fp:
            json_data = json.load(fp)
        
        config.tx_size = json_data['tx_size']
        config.tx_pool_size = json_data['tx_pool_size']
        config.node_num = json_data['node_num']
        config.network_flag = json_data['network_flag']
        config.bandwidth = json_data['bandwidth']
        config.tx_flag = json_data['tx_flag']
        config.tx_num = json_data['tx_num']
        config.tx_rate = json_data['tx_rate']
        config.random_topology_flag = json_data['random_topology_flag']
        config.network_topology = json_data['network_topology']
        config.protocol = json_data['protocol']
        config.fan_out = json_data['fan_out']
        config.heartbeat_interval = json_data['heartbeat_interval']
        config.bucket_size = json_data['bucket_size']
        config.block_size_limit = json_data['block_size_limit']
        config.hash_sig_size = json_data['hash_sig_size']
        config.start_time = json_data['start_time']
        config.over_time = json_data['over_time']
        config.consensus = json_data['consensus']
        config.process_cost = json_data['process_cost']
        config.log_flag = json_data['log_flag']
        config.timeout_propose = json_data['timeout_propose']
        config.timeout_propose_delta = json_data['timeout_propose_delta']
        config.timeout_pre_vote = json_data['timeout_pre_vote']
        config.timeout_pre_vote_delta = json_data['timeout_pre_vote_delta']
        config.timeout_pre_commit = json_data['timeout_pre_commit']
        config.timeout_pre_commit_delta = json_data['timeout_pre_commit_delta']
        fp.close()
    if config.random_topology_flag == 0 and len(config.network_topology) != config.node_num:
        print("ERROR:network_topology: len(network_topology) != node_num")
        return -1,-1,-1
    if config.protocol == "gossip" and config.fan_out >=config.node_num:
        print("ERROR:fan_out: fan_out >= node_num")
    path = "./mobius/log/"
    files = os.listdir(path=path)
    # for file in files:
        # os.remove(path=path+file)
    network = Network()
    network.reset()
    Block.block_size_limit = config.block_size_limit
    if config.protocol == "gossip":
        network.init(config.node_num, config.consensus, config.protocol, fan_out=config.fan_out)
    elif config.protocol == "kad":
        network.init(config.node_num, config.consensus, config.protocol, bucket_size=config.bucket_size)
    queue = EventQueue()
    # logger = log.Log()
    # logger.file_handle()
    # print("num:",config.node_num)
    if config.tx_flag == 0:
        tx_list, time_list = random_generate_tx(network.node_num, config.tx_num, config.tx_rate)
        network.transaction_list += tx_list
    for i in range(config.tx_num):
        event = Event("send_trans", time_list[i])
        # if protocol == "kad":
        #     event.set_dis(0)
        event.set_node_id(tx_list[i].sender)
        event.set_tx_id(i)
        # add_node_event(network, tx_list[i].sender, event)
        queue.add_event(event)
    # 第一个区块的共识开始时间设定
    if Network.consensus == "TBFT" or Network.consensus == "POW":
        new_event = Event("start", config.start_time)
        queue.add_event(new_event)
    else:
        new_event = Event("gen_block", config.start_time)
        new_event.set_node_id(0)
        # add_node_event(network, 0, new_event)
        queue.add_event(new_event)
    while not queue.is_empty():
        event = queue.get_next_event()
        if network.consensus == "PBFT":
            DoPBFTEvent.handle_event(event)
        elif network.consensus == "HotStuff":
            DoHotStuffEvent.handle_event(event)
        elif network.consensus == "TBFT":
            DoTBFTEvent.handle_event(event)
        elif network.consensus == "POW":
            DoPOWEvent.handle_event(event)

    statics = PStatistics(network)

    return statics.getTPS(), statics.getTxLatency(), statics.getAvgLatency()
    # print("--------------over--------------")
    # print(network.block_num)
    # for item in Network.node:
    #     print("node:%d, block_num:%d" % (item.id, len(item.blockchain_timestamp)))
    #     for i in range(len(item.blockchain_timestamp)):
    #         print("block:%d,time:%f" % (i, item.blockchain_timestamp[i]))


if __name__ == '__main__':
    tps_list = []
    tx_latency_list = []
    avg_latency_list = []
    block_size_list = []
    for i in range(4):
        # print(i)
        block_size_list.append(50*(i+1))
        config.block_size_limit = 100*512*(i+1)
        tps, tx_latency, avg_latency = main()
        tps_list.append(tps)
        tx_latency_list.append(tx_latency)
        avg_latency_list.append(avg_latency)
    print(tps_list)
    print(tx_latency_list)
    print(avg_latency_list)
    print(block_size_list)
    # plt.figure(1)
    # plt.subplot(1,3,1)
    # plt.title("tps--blockSize")
    # plt.xlabel("blockSize")
    # plt.ylabel("tps")
    # plt.grid(True,c="k",axis="both",linestyle="--",linewidth=0.3)
    # plt.plot(block_size_list,tps_list,c="r",lw=1,marker="o",ms=4,mfc="r")
    # plt.subplot(1,3,2)
    # plt.title("txLatency---blockSize")
    # plt.xlabel("blockSize")
    # plt.ylabel("txLatency")
    # plt.grid(True,c="k",axis="both",linestyle="--",linewidth=0.3)
    # plt.plot(block_size_list,tx_latency_list,c="r",lw=1,marker="o",ms=4,mfc="r")
    # plt.subplot(1,3,3)
    # plt.title("blockLatency---blockSize")
    # plt.xlabel("blockSize")
    # plt.ylabel("blockLatency")
    # plt.grid(True, c="k", axis="both", linestyle="--", linewidth=0.3)
    # plt.plot(block_size_list, avg_latency_list, c="r", lw=1, marker="o", ms=4, mfc="r")
    # plt.show()
    tps, tx_latency, block_latency = main()
    print('tps:', tps)
    print('tx_latency:', tx_latency)
    print('block_latency:', block_latency)
