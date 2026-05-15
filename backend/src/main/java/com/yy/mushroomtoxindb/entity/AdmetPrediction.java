package com.yy.mushroomtoxindb.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler;
import com.fasterxml.jackson.core.type.TypeReference;
import lombok.Data;

import java.util.Map;

@Data
@TableName(value = "admet_prediction", autoResultMap = true)
public class AdmetPrediction {
    @TableId(value = "compound_id")
    private Integer compoundId;

    @TableField(value = "toxicology", typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> toxicology;

    @TableField(value = "physicochemical_property", typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> physicochemicalProperty;

    @TableField(value = "metabolism", typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> metabolism;

    @TableField(value = "excretion", typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> excretion;

    @TableField(value = "distribution", typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> distribution;

    @TableField(value = "absorption", typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> absorption;
}