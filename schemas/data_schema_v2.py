
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class FieldType(str, Enum):
    string = "string"
    number = "number"
    boolean = "boolean"
    date = "date"
    datetime = "datetime"
    text = "text"
    enum = "enum"
    json = "json"


class RelationType(str, Enum):
    hasMany = "hasMany"
    belongsTo = "belongsTo"
    hasOne = "hasOne"


class FieldSchema(BaseModel):
    name: str
    type: FieldType
    nullable: bool = False
    isRelation: bool = False
    isPrimary: bool = False
    isUnique: bool = False


class RelationSchema(BaseModel):
    type: RelationType
    target: str
    foreignKey: str
    onDelete: str = "cascade"


class EntitySchema(BaseModel):
    name: str
    tableName: str
    fields: List[FieldSchema]
    relations: List[RelationSchema] = []


class DataSchema(BaseModel):
    entities: List[EntitySchema]