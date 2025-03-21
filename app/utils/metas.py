"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-25
__version__ = 0.0.1
__description__ = schema 与model 的处理工具
"""

from typing import Any, Callable, Optional, Set, Type, Union, get_args, get_origin

from pydantic import BaseModel, create_model, field_validator
from pydantic.alias_generators import to_snake
from pydantic.fields import FieldInfo
from sqlalchemy import inspect as sa_inspect
from sqlalchemy.orm import InstrumentedAttribute

from app.ctx import T_TABLE
from app.model import BaseTable
from app.schema import BaseSchema
from app.utils.serials import dumps_json


def schema_to_dict(
    schema: BaseSchema,
    table_cls: Type[BaseTable],
    /,
    exclude_none: bool = True,
    exclude: Set[str] | None = None,
    include: Set[str] | None = None,
    extra: dict[str, Any] = None,
    mapping: dict[str, Callable[[Any], Any]] = None,
) -> dict[str, Any]:
    """
        将schema 的入参转换为table 实例匹配的字典项. 如果schema中的某些字段(包括extra中) 在table 中不存在,会自动被忽略掉
        默认情况下schema 使用的是小驼峰形式,而table 使用的是下划线格式.
    :param schema: 表单实例
    :param table_cls: 数据库表类型
    :param exclude_none: 是否排除none值(默认排除)
    :param exclude: 需要排除的字段
    :param include: 需要包含的字段
    :param extra: 附加的其它数据
    :param mapping: 对指定的key进行映射转换
    :return:　匹配table 类型的 dict
    """
    schema_data = schema.model_dump(exclude_none=exclude_none, exclude=exclude, include=include)
    if extra and any(extra):
        schema_data.update(extra)
    if mapping is None:
        mapping = {}

    table_cols = [col.name for col in sa_inspect(table_cls).columns]
    table_data = {
        to_snake(k): mapping.get(k, mapping.get(to_snake(k)))(v) if (k in mapping or to_snake(k) in mapping) else v
        for k, v in schema_data.items()
        if to_snake(k) in table_cols
    }

    return table_data


def table_to_schema(
    instance: BaseTable,
    schema: Type[BaseModel],
    /,
    exclude_none: bool = True,
    exclude: list[str | InstrumentedAttribute] = None,
    include: list[str | InstrumentedAttribute] = None,
    extra: dict[str, Any] = None,
) -> BaseModel:
    """
        转换model数据到指定的schema类型
    :param instance: 数据库模型实体
    :param schema: pydantic 模型
    :param exclude_none:是否去除none
    :param exclude: 排除字段
    :param include: 包含字段
    :param extra: 附加数据(key必须是schema已有的字段,否则会报错)
    :return:
    """
    data = {}
    for field in schema.model_fields:
        if hasattr(instance, field):
            value = getattr(instance, field)
            if exclude_none and value is None:
                continue
            data[field] = value

    if exclude and any(exclude):
        exclude = list(map(lambda f: f.name if isinstance(f, InstrumentedAttribute) else f, exclude))
        data = dict(filter(lambda item: item[0] not in exclude, data.items()))

    if include and any(include):
        include = list(map(lambda f: f.name if isinstance(f, InstrumentedAttribute) else f, include))
        data = dict(filter(lambda item: item[0] in include, data.items()))

    if extra:
        data.update(extra)

    return schema.model_validate_json(dumps_json(data))


def create_schema(
    cls_table: Type[T_TABLE],
    *,
    include: list[str | InstrumentedAttribute] = None,
    exclude: list[str | InstrumentedAttribute] = None,
    validators: dict[str | InstrumentedAttribute, Callable] = None,
    other_schemas: list[Type[BaseModel]] = None,
) -> Type[BaseModel]:
    """
        根据sqlalchemy模型动态创建pydantic模型
    :param cls_table: 数据库模型
    :param include: 包含哪些字段(如果同时出现在排除列表中, 就不会被包含到最终结果)
    :param exclude: 排除哪些字段(先排除再包含)
    :param validators: 对实体的校验函数
    :param other_schemas: 与自定义的schema进行合并
    :return:
    """
    model_columns = sa_inspect(cls_table).columns
    # 去除数据库模型命名的前缀tab
    model_name = cls_table.__name__
    if model_name[0:3] == "Tab":
        model_name = model_name[3:]

    if exclude and any(exclude):
        exclude_cols = list(map(lambda f: f.name if isinstance(f, InstrumentedAttribute) else f, exclude))
        model_columns = list(filter(lambda c: c.name not in exclude_cols, model_columns))

    if include and any(include):
        include_cols = list(map(lambda f: f.name if isinstance(f, InstrumentedAttribute) else f, include))
        model_columns = list(filter(lambda c: c.name in include_cols, model_columns))

    # 构建每个字段的FieldInfo数据
    schema_fields = {}
    for col in model_columns:
        # 是否为必填项取决于table 是否可空 或 没有默认值
        py_type = Optional[col.type.python_type] if (col.nullable or col.default is not None) else col.type.python_type
        default = None if is_optional_type(py_type) else ...
        desc = col.comment if col.comment else None
        schema_fields[col.name] = (py_type, FieldInfo(default=default, description=desc))

    # 继承扩展的baseModel类
    _base_cols, _base_validators = {}, {}
    if other_schemas:
        # for scm in merge_schemas:
        # merge_schemas 中无法附加到当前动态创建的validator中, 暂时使用  validators 参数处理
        # _scm_validators = scm.__pydantic_decorators__.field_validators
        # if _scm_validators and any(_scm_validators):
        #     _base_validators.update({
        #         name: field_validator(*decor.info.fields, check_fields=False)(decor.func)
        #         for name, decor in _scm_validators.items()
        #     })

        # 合并基类的字段, 否则会在model_dump时不输出
        _base_cols = {
            field_name: (field_info.annotation, field_info)
            for scm in other_schemas
            for field_name, field_info in scm.model_fields.items()
        }
        schema_fields.update(_base_cols)

    # 添加校验规则
    base_validators = {}
    if validators and any(validators):
        for field_name, validator_func in validators.items():
            _name = field_name
            if isinstance(field_name, InstrumentedAttribute):
                _name = field_name.name

            if _name not in schema_fields:
                continue

            base_validators[validator_func.__name__] = field_validator(_name)(validator_func)

    # 动态创建模型
    schema_model = create_model(
        f"{model_name}Schema", __base__=BaseSchema, __validators__=base_validators, **schema_fields
    )
    return schema_model


def is_optional_type(type_hint) -> bool:
    """判断给定的类型是否为可选类型（即选填）"""
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    # 检查是否为 Optional 或 Union，并且包含 None
    return origin is Union and type(None) in args


# ============================================EXAMPLE================================================
# 数据库模型
# class TabUser(BaseTable):
#     __tablename__ = 'user_demo'
#
#     username = mapped_column(String, nullable=False, index=True, unique=True, comment="用户名")
#     age = mapped_column(Integer, comment="年龄")
#     asserts = mapped_column(DECIMAL(10, 2), comment="资产")
#     owner_address = mapped_column(String, comment="地址")
#     create_time = mapped_column(TIMESTAMP, nullable=False, comment="创建时间", server_default=func.now())
#
#
# # 年龄的校验器
# def validate_age(cls, value):
#     assert 18 <= value < 90, f"年龄不对!!! {value}"
#     return value
#
#
# class CustomModel1(BaseModel):
#     # test1: str | None = Body()
#     # test2_aa: int = Query(default=99, gt=0)
#     test3_cca: float = Field(default=22)
#
#
# def validate_test3_cca(cls, v):
#     print("v3")
#     assert v > 200, "要大于200"
#     return v
#
#
# class CustomModel2(BaseModel):
#     test1: str | None = Body(default=None)
#     test2_aa: int = Query(default=99, gt=0)
#     test4_cca: float = Field(default=22, gt=200)
#
#
# #
# # def validate_date(cls, value):
# #     assert value, "日期不能为空!"
# #     return str_to_dt(value)
# #
# #
# UserCreator = create_dynamic_schema(
#     TabUser,
#     exclude=['id'],
#     validators={"age": validate_age, "test3_cca": validate_test3_cca},
#     merge_schemas=[CustomModel1, CustomModel2],
# )
#
# # UserEditor = create_dynamic_schema(
# #     TabUser,
# #     exclude=[TabUser.id, TabUser.username]
# # )
#
# if __name__ == '__main__':
#     print(UserCreator)
#     creator = UserCreator(
#         username="李四", age=22,
#         asserts=Decimal("22.2"), ownerAddress="测试地址",
#         create_time="2024-09-22 10:22:33",
#         test3Cca=255,
#         test4_cca=266,
#     )
#
#     # 使用model_dump导出字典, 直接使用dumps_json统一处理日期与decimal类型
#     src_json = dumps_json(creator.model_dump(by_alias=True))
#     print(src_json)
#     # print(UserSchemaEditor)
#
#     print(UserCreator(**loads_json(src_json)).model_dump(by_alias=True))

# if __name__ == '__main__':
#     user = TabUser(id=1, username="张三", create_time=datetime.now(), age=33)
#     user_editor = convert_model_to_schema(
#         user, UserCreator,
#         exclude=[TabUser.age],
#         ext_data={"asserts": Decimal(12.34567)}
#     )
#     # editor = UserCreator.model_validate(user, strict=True)
#     print(user_editor.model_dump_json(exclude_defaults=True))
