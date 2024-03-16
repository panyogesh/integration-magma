from pyroute2 import NDB

class NetlinkUtils:
    def __init(self):
        self.ndb = NDB(log='debug')
        self.if_list = ndb.interfaces.dump()
        self.bridge = None

    def interfaces_summary(self):
        for record in self.ndb.interfaces.summary():
            print(record.ifname, record.address, record.state)

    def interfaces_dump(self):
        self.if_list = ndb.interfaces.dump()
        self.if_list.select_records(state='up')
        self.if_list.select_fields('index', 'ifname', 'kind')
        for line in if_dump.format('json'):
            print(line)
   
    def create_bridge(self, brname=str):

