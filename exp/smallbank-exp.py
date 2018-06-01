# args: <workload file> <batchsize> <sample rate (ledger)> <sample rate (commit)>
# sample rate: 0 -> get data every sample
#             ~(1<<x) -> get data every 2^x samples
# outputs:
  #
import sys
import os
import time
from config import *

usage = '''Usage:
    smallbank-exp.py <db> <num-node> <num-txn> <num-threads> <txn-rate> <batch size>

      db:                       either original, ustore or rocksdb
      num-node:                 total number of nodes
      num-txn:                  total number of txns
      num-threads:              total number of client threads
      txn-rate:                 txn rate
      batch size:               block size
    '''

def run_servers(nodes, cmds):
  for i in range(len(nodes)):
    cmd="ssh {} {}".format(nodes[i], cmds[i])
    print cmd
    os.system(cmd)

def run_client(server, num_node, num_txn, num_thread, txrate, db_type):
  print "==========================================================="
  client_log_path = CLI_LOG_PATH.format(num_node, txrate, num_thread, db_type)
  endpoint = server + ":7051/chaincode/"
  client_cmd = CLIENT_CMD.format(num_txn, num_thread, txrate, endpoint, client_log_path)
  print client_cmd
  os.system(client_cmd)

def stop(servers):
  for s in servers:
    kill_server = "ssh {} {}".format(s, KILL_SERVER_CMD)
    print kill_server
    os.system(kill_server)

def run_exp(num_node, num_txn, num_thread, txrate, batch_size, db_type):
  print "Start to run experiment. \n"
  N = num_node

  nodes=[]
  nodes.append(HOST.format(BOOTSTRAP_HOSTNO))
  for i in range(1,N):
    nodes.append(HOST.format(BOOTSTRAP_HOSTNO+i))

  cmds =[] # list of commands
  for i in range(N):
    env = ENV_TEMPLATE.format(i, N, batch_size, db_type)
    if i > 0:
      # add discoverynode
      env = "{} {}".format(env, ENV_EXTRA.format(nodes[0]))

    peer_log_path = PEER_LOG_PATH.format(num_node, db_type)
    if db_type == "rocksdb" or db_type == "original":
        cmds.append(CMD.format(HL_FILESYSTEMPATH, env, peer_log_path))
    elif db_type == "ustore":
        cmds.append(CMD.format(USTORE_DATAPATH, env, peer_log_path))
    else:
        print "Unrecognized DB", db_type
        sys.exit(0)


  run_servers(nodes, cmds)
  time.sleep(10)
  print "Network Setup"

  run_client(nodes[0], num_node, num_txn, num_thread, txrate,db_type)

  # time.sleep(SLEEP_TIME)

  # stop(CLIENT_NODE, NODES)
  # time.sleep(5)
  # return "{}/client_{}_{}_{}".format(CLIENT_LOG_DIR, NODES[0], thread, txrate)

def get_db_size(path):
  size = 0
  for dirpath, dirname, filenames in os.walk(path):
    for f in filenames:
      fp = os.path.join(dirpath, f)
      size += os.path.getsize(fp)
  return size


if __name__ == "__main__":
  if len(sys.argv) != 7 :
    print usage
    sys.exit(1)

  db_type = sys.argv[1]
  num_node = int(sys.argv[2])
  num_txn = int(sys.argv[3])
  num_thread = int(sys.argv[4])
  txrate = int(sys.argv[5])
  batch_size = int(sys.argv[6])
  run_exp(num_node, num_txn, num_thread, txrate, batch_size, db_type)
  print "Finish Experiment with {} num_node {} num_txn {} num_thread {} txrate {} batch_size {} dbtype".format(num_node, num_txn, num_thread, txrate, batch_size, db_type)

  # raw_input("End the servers and Query the size for DB??")
  # nodes=[]
  # nodes.append(HOST.format(BOOTSTRAP_HOSTNO))
  # for i in range(1,num_node):
  #   nodes.append(HOST.format(BOOTSTRAP_HOSTNO+i))

  # stop([], nodes)
  # # This python script must run at a hl node.
  # db_size = 0
  # if db_type == "rocksdb" or db_type == "original":
  #   db_size = get_db_size(HL_FILESYSTEMPATH)
  # elif db_type == "ustore":
  #   db_size = get_db_size(USTORE_DATAPATH)
  # else:
  #   print "Unrecognized DB", db_type
  #   sys.exit(0)
  # print("db size: {}".format(db_size))

