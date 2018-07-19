import sys
import json
import requests


if __name__ == '__main__':
    host_type = sys.argv[1]

    url = 'http://172.25.52.7:8888/getGPUClients?type=%s' % host_type
    resp = requests.get(url)
    assert resp.status_code == 200, resp.text
    hosts = json.loads(resp.text)
    print(' '.join(hosts))
