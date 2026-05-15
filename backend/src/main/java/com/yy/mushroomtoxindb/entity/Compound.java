package com.yy.mushroomtoxindb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("compound")
public class Compound {
    @TableId(value = "compound_id", type = IdType.AUTO)
    private Integer compoundId;

    private String commonName;
    private String otherName;
    private String chemicalTaxonomy;
    private String pubchemCid;
    private String chebiId;
    private String cas;
    private String fileSource;
    private String molecularFormula;
    private String smiles;
    private String inchi;

    @TableField(value = "inchi_key")
    private String inchikey; // 数据库列名为 inchikey (无下划线)
}