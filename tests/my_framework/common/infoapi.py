"""第10课：接口封装层——把裸 HTTP 调用升级成业务语义方法"""


class InfoApi:
    """Hyperliquid /info 端点的业务语义封装（薄封装，单一职责）"""

    def __init__(self, client):
        self._client = client

    def _query(self, payload: dict) -> dict:
        """所有 /info 查询共用的底层：发请求 + 统一状态校验"""
        resp = self._client.post(endpoint="/info", json_data=payload)
        assert resp.status_code == 200, f"/info 查询失败: {payload}"
        return resp.json()

    def meta(self) -> dict:
        """查询永续合约元数据"""
        return self._query({"type": "meta"})

    def all_mids(self) -> dict:
        """查询全部中间价（含现货 #id / @index）"""
        return self._query({"type": "allMids"})

    def perp_mids(self) -> dict:
        """只返回永续合约报价：过滤掉现货的 #id / @index key（领域知识集中在此）"""
        return {
            k: v
            for k, v in self.all_mids().items()
            if not k.startswith(("#", "@"))
        }

    def clearinghouse_state(self, address: str) -> dict:
        """查询用户账户状态"""
        return self._query({"type": "clearinghouseState", "user": address})

