package com.yy.mushroomtoxindb.dto;

import com.yy.mushroomtoxindb.entity.*;
import lombok.Data;
import java.util.List;

@Data
public class CompoundDetailDTO {
    private Compound info;
    // 毒性板块：包含宏观毒性数据和微观分子活性数据
    private ToxicitySection toxicitySection;
    private AdmetPrediction admet;
    private List<FungusInfo> fungi;

    @Data
    public static class ToxicitySection {
        private List<Toxicity> generalToxicity;   // 宏观毒性记录
        private List<MolecularActivity> molecularActivities; // 分子靶点活性（子分块）
    }
}