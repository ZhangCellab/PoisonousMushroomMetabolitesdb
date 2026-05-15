package com.yy.mushroomtoxindb.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.yy.mushroomtoxindb.entity.FungusInfo;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface FungusMapper extends BaseMapper<FungusInfo> {

    /**
     * 需求 1.3: 根据化合物 ID 查询包含它的所有真菌
     * 修改点：表名改为 fungus_info, fungus_with_compound
     * 修改点：列名改为 fungus_id, compound_id
     */
    @Select("SELECT f.* FROM fungus_info f " +
            "JOIN fungus_with_compound fwc ON f.fungus_id = fwc.fungus_id " +
            "WHERE fwc.compound_id = #{compoundId}")
    List<FungusInfo> findFungiByCompoundId(@Param("compoundId") Integer compoundId);
}