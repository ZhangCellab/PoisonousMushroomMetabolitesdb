package com.yy.mushroomtoxindb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("mechanism")
public class Mechanism {
    @TableId(value = "mechanism_id", type = IdType.AUTO)
    private Integer mechanismId;

    private Integer compoundId;
    private String description;
    private String reference;
    private String externalLink;
}