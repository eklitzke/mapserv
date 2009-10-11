import thrift
import thrift.transport
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from mapserv.interfaces.query import QueryService

def new_client(host='127.0.0.1', port=9090):
    socket = TSocket.TSocket(host, port)
    transport = TTransport.TBufferedTransport(socket)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = QueryService.Client(protocol)
    transport.open()
    return client
