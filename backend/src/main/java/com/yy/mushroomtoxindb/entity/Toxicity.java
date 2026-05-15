package com.yy.mushroomtoxindb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("toxicity")
public class Toxicity {
    @TableId(value = "toxicity_id", type = IdType.AUTO)
    private Integer toxicityId;

    private Integer compoundId;
    private String toxicityType;
    private String toxicityValue;
    private String reference;
}