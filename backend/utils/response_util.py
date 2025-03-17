from flask import jsonify

class ResponseUtil:
    """
    统一响应工具类
    用于生成标准格式的API响应
    """
    
    @staticmethod
    def success(data=None, message="success"):
        """
        成功响应
        
        Args:
            data: 响应数据
            message (str): 响应消息
            
        Returns:
            dict: 标准格式的成功响应
        """
        return jsonify({
            "code": 0,
            "message": message,
            "data": data
        })
    
    @staticmethod
    def error(code=400, message="error", data=None):
        """
        错误响应
        
        Args:
            code (int): 错误码
            message (str): 错误消息
            data: 额外的错误数据
            
        Returns:
            dict: 标准格式的错误响应
        """
        return jsonify({
            "code": code,
            "message": message,
            "data": data
        }), code
    
    @staticmethod
    def params_error(message="参数错误"):
        """
        参数错误响应
        
        Args:
            message (str): 错误消息
            
        Returns:
            dict: 参数错误的标准响应
        """
        return ResponseUtil.error(422, message)
    
    @staticmethod
    def unauthorized(message="未授权"):
        """
        未授权响应
        
        Args:
            message (str): 错误消息
            
        Returns:
            dict: 未授权的标准响应
        """
        return ResponseUtil.error(401, message)
    
    @staticmethod
    def forbidden(message="禁止访问"):
        """
        禁止访问响应
        
        Args:
            message (str): 错误消息
            
        Returns:
            dict: 禁止访问的标准响应
        """
        return ResponseUtil.error(403, message)
    
    @staticmethod
    def not_found(message="资源不存在"):
        """
        资源不存在响应
        
        Args:
            message (str): 错误消息
            
        Returns:
            dict: 资源不存在的标准响应
        """
        return ResponseUtil.error(404, message)
    
    @staticmethod
    def server_error(message="服务器内部错误"):
        """
        服务器内部错误响应
        
        Args:
            message (str): 错误消息
            
        Returns:
            dict: 服务器内部错误的标准响应
        """
        return ResponseUtil.error(500, message) 