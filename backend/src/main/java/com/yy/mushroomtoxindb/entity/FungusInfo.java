package com.yy.mushroomtoxindb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.fasterxml.jackson.annotation.JsonRawValue;
import lombok.Data;

@Data
@TableName("fungus_info")
public class FungusInfo {
    @TableId(value = "fungus_id", type = IdType.AUTO)
    private Integer fungusId;

    //@JsonRawValue
    private String fungusName;
    private String ncbiTaxonomyId;
    private String phylum;

    @TableField("class") // 数据库列名为 class (Java关键字冲突)
    private String clazz;

    @TableField(value = "`order`")
    private String orderName;

    private String family;
    private String genus;
    private String reference;
}