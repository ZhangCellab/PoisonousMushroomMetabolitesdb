package com.yy.mushroomtoxindb.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.yy.mushroomtoxindb.entity.MolecularActivity;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface MolecularActivityMapper extends BaseMapper<MolecularActivity> {

    /**
     * 更新为小写下划线字段名
     */
    @Select("SELECT * FROM molecular_activity WHERE compound_id = #{compoundId}")
    List<MolecularActivity> findActivitiesByCompoundId(@Param("compoundId") Integer compoundId);
}