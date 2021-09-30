#print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
from connection import rest_api_client


t = rest_api_client.RestApiClient("192.168.0.100", "1234")