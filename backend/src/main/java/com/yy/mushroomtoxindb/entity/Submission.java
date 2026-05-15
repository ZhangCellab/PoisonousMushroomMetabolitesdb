package com.yy.mushroomtoxindb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.util.Date;

@Data
@TableName("submissions")
public class Submission {
    @TableId(value = "submit_id", type = IdType.AUTO)
    private Integer submitId;

    private String familyName;
    private String yourFirstName;
    private String yourEmail;
    private String compoundName;
    private String casNumber;
    private String description;
    private String toxicityData;
    private String sourceMushroom;
    private String reference;

    private Date submitTime;
}