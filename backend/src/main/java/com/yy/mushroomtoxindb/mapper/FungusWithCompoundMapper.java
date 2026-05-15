package com.yy.mushroomtoxindb.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.yy.mushroomtoxindb.entity.FungusWithCompound;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

@Mapper
public interface FungusWithCompoundMapper extends BaseMapper<FungusWithCompound> {

    /**
     * 需求 1.4: 获取该蘑菇已知的所有化合物信息
     * 修改点：
     * 1. 表名：compound, fungus_with_compound, admet_prediction
     * 2. 列名：compound_id, common_name, molecular_formula, physicochemical_property
     */
    @Select("SELECT c.compound_id, c.common_name, c.cas, c.molecular_formula, a.physicochemical_property " +
            "FROM compound c " +
            "JOIN fungus_with_compound fwc ON c.compound_id = fwc.compound_id " +
            "LEFT JOIN admet_prediction a ON c.compound_id = a.compound_id " +
            "WHERE fwc.fungus_id = #{fungusId}")
    List<Map<String, Object>> findCompoundsByFungusId(@Param("fungusId") Integer fungusId);
}