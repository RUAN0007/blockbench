TXRATES=[5]
BOOTSTRAP_HOSTNO=50     # <-- where there server (running HL) is
HOST="slave-{}"

HL_FILESYSTEMPATH="/data/ruanpc/hyperledger"   # <-- where the HL is store (for rocksdb)
                                          # for UStore, data is store in
                                          # $HL/fabric/build/bin/ustore_data
USTORE_DATAPATH="/data/ruanpc/ustore_data"

CLIENT_EXE="/users/ruanpc/blockbench/src/macro/smallbank/driver"   # <-- where this current directory is
PEER_EXE="/users/ruanpc/gopath/src/github.com/hyperledger/fabric/build/bin/peer"

PEER_LOG_PATH = "/data/ruanpc/hl_log_{}nodes_{}"
CLI_LOG_PATH = "/data/ruanpc/cli_log_{}nodes_{}rate_{}threads_{}"

LOGGING_LEVEL = "warning:consensus/pbft,consensus/executor,ledger,db,buckettree,state,consensus/statetransfer=info"

ENV_TEMPLATE = ("CORE_PEER_ID=vp{} CORE_PEER_ADDRESSAUTODETECT=true "
                "CORE_PEER_NETWORK=blockbench "
                "CORE_PEER_VALIDATOR_CONSENSUS_PLUGIN=pbft "
                "CORE_PEER_FILESYSTEMPATH="+HL_FILESYSTEMPATH+" "
                "CORE_VM_ENDPOINT=http://localhost:2375 "
                "CORE_PBFT_GENERAL_MODE=batch "
                "CORE_PBFT_GENERAL_TIMEOUT_REQUEST=100s "
                "CORE_PBFT_GENERAL_TIMEOUT_VIEWCHANGE=10s "
                "CORE_PBFT_GENERAL_TIMEOUT_RESENDVIEWCHANGE=10s "
                "CORE_PBFT_GENERAL_N={} "
                "CORE_PBFT_GENERAL_F=0 "
                "LEDGER_SAMPLE_INTERVAL=127 "
                "CORE_EXECUTION_SAMPLE_INTERVAL=127 "
                "CORE_PBFT_GENERAL_BATCHSIZE={} "
                "CORE_PEER_DB_DBTYPE={} "
                "CORE_PEER_DB_COMPRESSION=false")

ENV_EXTRA = "CORE_PEER_DISCOVERY_ROOTNODE={}:7051"


CMD="\" removeUnwantedImages; rm -rf {};  {} nohup " + PEER_EXE + " node start --logging-level= " + LOGGING_LEVEL + " > {} 2>&1 &\""
KILL_SERVER_CMD = "pkill -TERM peer"

CLIENT_CMD = CLIENT_EXE + " {} {} {} 100 {} github.com/smallbank > {} 2>&1"
