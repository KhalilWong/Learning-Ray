import requests
import time
import hmac
import base64
import ray
from ray import serve
'''
serve.start()
################################################################################
@serve.deployment(ray_actor_options = {'num_gpus': 1})
class Counter:
  def __init__(self):
      self.count = 0

  def __call__(self, request):
      self.count += 1
      return {"count": self.count}

################################################################################
@serve.deployment(name = "http_deployment", route_prefix = "/api")
class HTTPDeployment:
  def __call__(self, request):
      return "Hello world!"
'''
################################################################################
def elogin(spath, data):
    check = ['app_id', 'access_token', 'username']
    for c in check:
        if c not in data:
            print('elogin Data Error!')
            return
    #
    path = spath + '/api/v1/user/auth/eaccess_token_login/'
    r = requests.post(path, data = data)
    dict = r.json()
    return (dict['user_id'], dict['key'])
    #return dict

################################################################################
def open(spath, data):
    check = ['user_id', 'key', 'secret_id']
    for c in check:
        if c not in data:
            print('open Data Error!')
            return
    #
    path = spath + '/api/v1/dmp/ttsa/open/'
    r = requests.post(path, data = data)
    dict = r.json()
    return dict

################################################################################
def chat(spath, data, query_text):
    check = ['user_id', 'key', 'secret_id']
    for c in check:
        if c not in data:
            print('chat Data Error!')
            return
    #
    path = spath + '/api/v1/dmp/ttsa/chat/'
    data.update({'query_text': query_text})
    r = requests.post(path, data = data)
    dict = r.json()
    return dict

################################################################################
def get_access_token(app_id, app_secret, username):
    ts = str(int(time.time())).encode('utf-8')  # 时间戳
    key = ''.join([app_id, app_secret, username]).encode('utf-8')
    token = hmac.new(key, ts, 'MD5').hexdigest().encode('utf-8')
    access_token = base64.b64encode(token).decode('utf-8')
    return access_token

################################################################################
'''
Counter.deploy()

#assert requests.get("http://127.0.0.1:8000/Counter").json() == {"count": 1}
print(requests.get("http://127.0.0.1:8000/Counter").json())
#assert ray.get(Counter.get_handle().remote()) == {"count": 2}
print(ray.get(Counter.get_handle().remote(...)))
################################################################################
HTTPDeployment.deploy()
print(requests.get("http://127.0.0.1:8000/api").text)
handle = serve.get_deployment("http_deployment").get_handle()
print(ray.get(handle.remote(...)))
################################################################################
print(serve.list_deployments())
print(ray.get_gpu_ids())
print(ray.available_resources())
'''
app_id = '&^RhBB7y@cR1xSt!SYCuXGBQ'#'C8Dk6aAfhiWQp8s*lrDljAvg'
app_secret = 'NL5xWEEDtKz0l0$G#hsfGdU#W$Sq75'#'PPWxM@1@(ZbC$Fh^FUoT8LP240Jk9C'
username = 'CCB'#'jiansheyinhang'
secret_id = '43d1334265ba4236862dc607b7a39b3d'#'5799ec91404d4c4994a293d83fe7760e'
server_path = 'http://120.92.212.177:1700'#'http://vhop.xmov.ai'
data = {
    'app_id': app_id,
    'access_token': get_access_token(app_id, app_secret, username),
    'username': username,
    'secret_id': secret_id
}
#
uid, key = elogin(server_path, data)
print('USER_ID: ', uid)
print('KEY: ', key)
data.update({'user_id': uid, 'key': key})
tmp = open(server_path, data)
print(tmp)
tmp = chat(server_path, data, '你好')
print(tmp)
r = requests.get(
    server_path + '/api/v1/dmp/digital/resp/offline_video_task_status/',
    headers = {'Content-Type': 'application/json'},
    params = {'digital_id': '1'}
)
print(r.text)
r = requests.get(server_path + '/api/v1/dmp/digital/')
print(r.text)
