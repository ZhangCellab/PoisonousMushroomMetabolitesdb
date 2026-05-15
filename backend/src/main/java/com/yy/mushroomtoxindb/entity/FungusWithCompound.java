package com.yy.mushroomtoxindb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("fungus_with_compound")
public class FungusWithCompound {
    @TableId(value = "fungus_with_compound_id", type = IdType.AUTO)
    private Integer fungusWithCompoundId;

    private Integer fungusId;
    private Integer compoundId;
}