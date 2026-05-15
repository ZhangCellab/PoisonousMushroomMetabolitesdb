package com.yy.mushroomtoxindb.service;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.yy.mushroomtoxindb.dto.CompoundDetailDTO;
import com.yy.mushroomtoxindb.entity.*;
import com.yy.mushroomtoxindb.mapper.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class CompoundService extends ServiceImpl<CompoundMapper, Compound> {

    @Autowired private ToxicityMapper toxicityMapper;
    @Autowired private AdmetMapper admetMapper;
    @Autowired private FungusMapper fungusMapper;
    @Autowired private MolecularActivityMapper activityMapper;

    public CompoundDetailDTO getCompoundDetail(Integer compoundId) {
        CompoundDetailDTO dto = new CompoundDetailDTO();

        // 1. 基础信息
        dto.setInfo(this.getById(compoundId));

        // 2. 毒性与活性板块
        CompoundDetailDTO.ToxicitySection toxSection = new CompoundDetailDTO.ToxicitySection();


        toxSection.setGeneralToxicity(toxicityMapper.selectList(
                new QueryWrapper<Toxicity>().eq("compound_id", compoundId)));

        toxSection.setMolecularActivities(activityMapper.selectList(
                new QueryWrapper<MolecularActivity>().eq("compound_id", compoundId)));

        dto.setToxicitySection(toxSection);

        // 3. ADMET
        dto.setAdmet(admetMapper.selectById(compoundId));

        // 4. 真菌关联
        dto.setFungi(fungusMapper.findFungiByCompoundId(compoundId));

        return dto;
    }

    // 按毒性数据量进行排序
    public Page<Compound> pageCompoundsWithToxicityCount(Page<Compound> page) {
        return this.baseMapper.selectCompoundsWithToxicityCount(page);
    }

}