class StatusCode:
    def __init__(self):
        self.init()

    def init(self):
        self._data = {"msg": "成功", "data": [], "code": 0, "total": 0}

    def success(self, data=None, total=0, msg=None):
        self.init()
        self._data["data"] = data or []
        self._data["total"] = total
        self._data["msg"] = msg if msg is not None else "Success"  # 成功
        self._data["code"] = 0

        return self._data

    @property
    def data(self):
        return self._data

    @property
    def args_missing(self):
        self.init()
        self._data["code"] = 1001
        self._data["msg"] = "Parameter Missing"  # 参数缺失

        return self._data

    @property
    def file_validated_erroe(self):

        self.init()
        self._data["code"] = 1002
        self._data["msg"] = "Wrong File Verification"  # 文件校验错误

        return self._data

    @property
    def method_error(self):

        self.init()
        self._data["code"] = 1003
        self._data["msg"] = "Wrong Request Function"  # 请求方法错误

        return self._data

    @property
    def save_data_fail(self):

        self.init()
        self._data["code"] = 1004
        self._data["msg"] = "Wrong File Saving"  # 数据保存出错

        return self._data

    @property
    def not_found(self):

        self.init()
        self._data["code"] = 1005
        self._data["msg"] = "Data Cannot Found"  # 数据未找到

        return self._data

    @property
    def args_valid_error(self):

        self.init()
        self._data["code"] = 1006
        self._data["msg"] = "Wrong Parameter Verification"  # 参数校验错误

        return self._data

    @property
    def operate_error(self):

        self.init()
        self._data["code"] = 1007
        self._data["msg"] = "Wrong Operation"  # 操作出错

        return self._data

    @property
    def system_inner_error(self):

        self.init()
        self._data["code"] = 1008
        self._data["msg"] = "System busy, try later"  # 系统繁忙，请稍后重试

        return self._data

    @property
    def args_type_error(self):
        self.init()
        self._data["code"] = 1009
        self._data["msg"] = "Parameter Type Error"  # 参数类型出错
        return self._data

    def custom_error(self, msg, data=None):
        self.init()
        self._data["code"] = 1010
        self._data["msg"] = msg
        self._data["data"] = data
        return self._data

    @property
    def args_error(self):
        self.init()
        self._data["code"] = 1011
        self._data["msg"] = "Wrong parameter"  # 参数错误
        return self._data
