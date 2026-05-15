package com.yy.mushroomtoxindb.dto;

import com.yy.mushroomtoxindb.entity.FungusInfo;
import lombok.Data;
import java.util.List;
import java.util.Map;

@Data
public class FungusDetailDTO {
    private FungusInfo fungusInfo;
    private List<Map<String, Object>> compounds; // 包含基本信息和解析后的 MW
}