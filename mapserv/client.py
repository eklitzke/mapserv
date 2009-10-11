import thrift
import thrift.transport
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
import mapserv.config
from mapserv.interfaces.query import QueryService

def new_client(host=None, port=None):
    cfg = mapserv.config.load()
    host = host if host is not None else cfg['iface']
    port = port if port is not None else cfg['port']
    socket = TSocket.TSocket(host, port)
    transport = TTransport.TBufferedTransport(socket)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = QueryService.Client(protocol)
    transport.open()
    return client
