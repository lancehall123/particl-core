#!/usr/bin/env python3
# Copyright (c) 2017 The Particl Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_framework.test_particl import ParticlTestFramework
from test_framework.util import *

import decimal

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    a = decimal.Decimal(a)
    b = decimal.Decimal(b)
    return abs(a-b) <= max(decimal.Decimal(rel_tol) * decimal.Decimal(max(abs(a), abs(b))), abs_tol)

class ForkTest(ParticlTestFramework):

    def __init__(self):
        super().__init__()
        self.setup_clean_chain = True
        self.num_nodes = 6
        self.extra_args = [ ['-debug',] for i in range(self.num_nodes)]

    def setup_network(self, split=False):
        self.nodes = start_nodes(self.num_nodes, self.options.tmpdir, self.extra_args, genfirstkey=False)
        
        connect_nodes_bi(self.nodes, 0, 1)
        connect_nodes_bi(self.nodes, 0, 2)
        connect_nodes_bi(self.nodes, 1, 2)
        
        connect_nodes_bi(self.nodes, 3, 4)
        connect_nodes_bi(self.nodes, 3, 5)
        connect_nodes_bi(self.nodes, 4, 5)
        
        
        self.is_network_split = False
        self.sync_all()

    def run_test(self):
        nodes = self.nodes
        
        #ro = nodes[0].extkeyimportmaster("abandon baby cabbage dad eager fabric gadget habit ice kangaroo lab absorb")
        #assert(ro['account_id'] == 'aaaZf2qnNr5T7PWRmqgmusuu5ACnBcX2ev')
        
        ro = nodes[0].extkeyimportmaster("pact mammal barrel matrix local final lecture chunk wasp survey bid various book strong spread fall ozone daring like topple door fatigue limb olympic", "", "true")
        ro = nodes[0].getnewextaddress("lblExtTest")
        assert(ro == "pparszNetDqyrvZksLHJkwJGwJ1r9JCcEyLeHatLjerxRuD3qhdTdrdo2mE6e1ewfd25EtiwzsECooU5YwhAzRN63iFid6v5AQn9N5oE9wfBYehn")
        
        ro = nodes[0].scanchain()
        ro = nodes[0].getinfo()
        assert(ro['balance'] == 25000)
        
        
        ro = nodes[3].extkeyimportmaster("abandon baby cabbage dad eager fabric gadget habit ice kangaroo lab absorb")
        assert(ro['account_id'] == 'aaaZf2qnNr5T7PWRmqgmusuu5ACnBcX2ev')
        
        ro = nodes[3].getinfo()
        assert(ro['balance'] == 100000)
        
        
        
        self.wait_for_height(nodes[0], 2, 1000)
        
        # stop group1 from staking
        ro = nodes[0].reservebalance(True, 10000000)
        
        
        self.wait_for_height(nodes[3], 5, 2000)
        
        # stop group2 from staking
        ro = nodes[3].reservebalance(True, 10000000)
        
        node0_chain = []
        for k in range(1, 6):
            try:
                ro = nodes[0].getblockhash(k)
            except JSONRPCException as e:
                assert("Block height out of range" in e.error['message'])
                ro = ""
            node0_chain.append(ro)
            print("node0 ",k, " - ", ro)
        
        node3_chain = []
        for k in range(1, 6):
            ro = nodes[3].getblockhash(k)
            node3_chain.append(ro)
            print("node3 ",k, " - ", ro)
        
        
        # connect groups
        connect_nodes_bi(self.nodes, 0, 3)
        
        fPass = False
        for i in range(15):
            time.sleep(2)
            
            fPass = True
            for k in range(1, 6):
                try:
                    ro = nodes[0].getblockhash(k)
                except JSONRPCException as e:
                    assert("Block height out of range" in e.error['message'])
                    ro = ""
                if not ro == node3_chain[k]:
                    fPass = False
                    break
            if fPass:
                break
        #assert(fPass)
        
        
        node0_chain = []
        for k in range(1, 6):
            try:
                ro = nodes[0].getblockhash(k)
            except JSONRPCException as e:
                assert("Block height out of range" in e.error['message'])
                ro = ""
            node0_chain.append(ro)
            print("node0 ",k, " - ", ro)
        
        
        ro = nodes[0].getinfo()
        print("\n\nnodes[0].getinfo ", ro)
        
        ro = nodes[3].getinfo()
        print("\n\nnodes[3].getinfo ", ro)
        
        #assert(False)
        #print(json.dumps(ro, indent=4))
        

if __name__ == '__main__':
    ForkTest().main()
