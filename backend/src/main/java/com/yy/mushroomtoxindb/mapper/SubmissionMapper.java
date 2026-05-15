package com.yy.mushroomtoxindb.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.yy.mushroomtoxindb.entity.Submission;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface SubmissionMapper extends BaseMapper<Submission> {
}