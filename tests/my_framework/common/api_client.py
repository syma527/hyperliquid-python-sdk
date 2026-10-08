import requests
import urllib3
from requests import session
# 优雅地关闭未验证 HTTPS 请求的黄色警告（大厂必备小细节）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from tests.my_framework.tools.my_log import log
class ApiClient:
    """
    大厂级统一请求客户端封装
    职责：不管什么接口，只要业务层把路由和参数交给我，我就负责在底层加壳、配代理、发出去并拿回响应。
    """
    def __init__(self,base_url):
        self.base_url = base_url
        # 1. 统一管理基础域名（环境开关）
        # 2. 初始化 Session，大厂规范中它可以自动帮我们保持连接和 Cookie 状态
        self.session = session()
        self.session.headers.update({
                "Content-Type":"application/json",
                "Accept":"*/*"
            })

    def post(self,endpoint,json_data = None):
        """统一封装的 POST 安全请求方法"""
        # 拼接url
        url  = f"{self.base_url}{endpoint}"
        try:
            response =  self.session.post(url,json=json_data,timeout=10)
        except requests.exceptions.RequestException as e:
            log.error(f"错误,通信异常| {e}")
            raise
        log.info(f"←{response.status_code}{endpoint}")
        return response




