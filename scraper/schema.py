"""
手机规格字段标准 Schema

所有采集数据必须按此结构输出。
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class PhoneSpecs(BaseModel):
    """手机规格模型"""
    # 基本信息
    id: str                          # 唯一标识: brand_model (如 apple_iphone16)
    brand: str                       # 品牌: Apple, Samsung, Xiaomi...
    model: str                       # 型号: iPhone 16 Pro
    model_name: str                  # 完整名称: iPhone 16 Pro Max 256GB
    
    # 显示屏
    screen_size: Optional[str]       # 屏幕尺寸: 6.1英寸
    screen_type: Optional[str]       # 屏幕类型: OLED, AMOLED, LCD
    resolution: Optional[str]        # 分辨率: 2556x1179
    refresh_rate: Optional[str]      # 刷新率: 120Hz
    
    # 处理器
    chipset: Optional[str]           # 芯片: A18 Pro, Snapdragon 8 Gen 3
    cpu_cores: Optional[str]         # CPU核心数
    gpu: Optional[str]               # GPU
    
    # 内存与存储
    ram: Optional[str]               # 运行内存: 8GB
    storage: Optional[str]           # 存储: 256GB
    storage_expandable: Optional[bool]  # 是否支持扩展
    
    # 摄像头
    rear_camera_main: Optional[str]  # 后置主摄: 48MP
    rear_camera_count: Optional[int] # 后置摄像头数量
    rear_camera_specs: Optional[str] # 后置详细: 48MP主摄+12MP超广角+12MP长焦
    front_camera: Optional[str]      # 前置: 12MP
    video: Optional[str]             # 视频拍摄: 4K@60fps
    
    # 电池与充电
    battery_capacity: Optional[str]  # 电池容量: 4500mAh
    charging_wired: Optional[str]    # 有线充电: 45W
    charging_wireless: Optional[str] # 无线充电: 25W MagSafe
    fast_charging: Optional[bool]    # 是否支持快充
    
    # 系统与连接
    os: Optional[str]                # 操作系统: iOS 18, Android 14, HarmonyOS 5
    network_5g: Optional[bool]       # 是否支持5G
    sim_type: Optional[str]          # SIM类型: Nano-SIM, eSIM
    
    # 物理参数
    weight: Optional[str]            # 重量: 170g
    dimensions: Optional[str]        # 尺寸: 146.7x71.5x7.8mm
    water_resistance: Optional[str]  # 防水: IP68
    material: Optional[str]          # 机身材质: 钛金属, 玻璃, 塑料
    
    # 其他特性
    fingerprint: Optional[str]       # 指纹: 屏下, 侧边, 背面
    face_unlock: Optional[bool]      # 人脸解锁
    nfc: Optional[bool]              # NFC
    infrared: Optional[bool]         # 红外遥控
    headphone_jack: Optional[bool]   # 3.5mm耳机孔
    
    # 元数据
    launch_date: Optional[str]       # 上市日期: 2024-09-20
    source: str                      # 数据来源: jd.com
    source_url: Optional[str]        # 来源URL
    fetched_at: str                  # 采集时间: ISO 8601


# API 接口字段说明
RAPIDAPI_FIELDS_DESC = {
    "search": "按关键词搜索手机型号，返回匹配列表",
    "specs": "按 ID 查询完整规格参数",
    "compare": "对比两款手机规格（Phase 2）",
    "brands": "列出所有品牌",
    "latest": "最新上市机型列表"
}
