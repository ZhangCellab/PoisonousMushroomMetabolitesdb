package com.yy.mushroomtoxindb.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yy.mushroomtoxindb.entity.Compound;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface CompoundMapper extends BaseMapper<Compound> {

    //按毒性数据排序
    @Select("SELECT c.*, COUNT(t.toxicity_id) as toxicity_count " +
            "FROM compound c " +
            "LEFT JOIN toxicity t ON c.compound_id = t.compound_id " +
            "GROUP BY c.compound_id " +
            "ORDER BY toxicity_count DESC, c.common_name ASC")
    Page<Compound> selectCompoundsWithToxicityCount(Page<Compound> page);

}