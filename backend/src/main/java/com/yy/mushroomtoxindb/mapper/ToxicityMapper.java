package com.yy.mushroomtoxindb.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.yy.mushroomtoxindb.entity.Toxicity;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface ToxicityMapper extends BaseMapper<Toxicity> {
}