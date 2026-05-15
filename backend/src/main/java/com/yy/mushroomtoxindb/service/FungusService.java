package com.yy.mushroomtoxindb.service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.yy.mushroomtoxindb.dto.FungusDetailDTO;
import com.yy.mushroomtoxindb.entity.FungusInfo;
import com.yy.mushroomtoxindb.mapper.FungusMapper;
import com.yy.mushroomtoxindb.mapper.FungusWithCompoundMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.*;

@Service
public class FungusService extends ServiceImpl<FungusMapper, FungusInfo> {

    @Autowired private FungusWithCompoundMapper fwcMapper;
    private final ObjectMapper objectMapper = new ObjectMapper();

    /**
     * 需求 1.4: 获取真菌详情及关联化合物（含 MW 解析）
     */
    public FungusDetailDTO getFungusDetail(Integer fungusId) {
        FungusDetailDTO dto = new FungusDetailDTO();
        dto.setFungusInfo(this.getById(fungusId));

        List<Map<String, Object>> rawCompounds = fwcMapper.findCompoundsByFungusId(fungusId);

        // 解析 ADMET JSON 中的 MW (分子量)
        for (Map<String, Object> item : rawCompounds) {
            String jsonStr = (String) item.get("physicochemical_property");
            if (jsonStr != null) {
                try {
                    JsonNode node = objectMapper.readTree(jsonStr);
                    item.put("molecularWeight", node.get("MW").asText());
                } catch (Exception e) {
                    item.put("molecularWeight", "N/A");
                }
            }
            item.remove("physicochemical_property"); // 移除冗余的长字符串
        }

        dto.setCompounds(rawCompounds);
        return dto;
    }
}