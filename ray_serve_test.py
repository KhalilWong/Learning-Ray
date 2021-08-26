import requests
import ray
from ray import serve

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

################################################################################
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
