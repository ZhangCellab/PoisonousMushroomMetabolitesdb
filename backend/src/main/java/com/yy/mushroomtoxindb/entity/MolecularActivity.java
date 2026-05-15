package com.yy.mushroomtoxindb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("molecular_activity")
public class MolecularActivity {
    @TableId(value = "activity_id", type = IdType.AUTO)
    private Integer activityId;

    private Integer compoundId;
    private String target;
    private String function;
    private String parameter;
    private String value;
    private String organism;
    private String source;
}