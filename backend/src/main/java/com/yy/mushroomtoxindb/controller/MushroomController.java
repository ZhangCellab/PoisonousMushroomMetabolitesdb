package com.yy.mushroomtoxindb.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
//import org.openscience.cdk.interfaces.IAtomContainer;
//import org.openscience.cdk.fingerprint.IBitFingerprint;
//import org.openscience.cdk.silent.SilentChemObjectBuilder;
//import org.openscience.cdk.smiles.SmilesParser;
//import org.openscience.cdk.fingerprint.MACCSFingerprinter;
import com.yy.mushroomtoxindb.dto.CompoundDetailDTO;
import com.yy.mushroomtoxindb.dto.FungusDetailDTO;
import com.yy.mushroomtoxindb.entity.*;
import com.yy.mushroomtoxindb.mapper.SubmissionMapper;
import com.yy.mushroomtoxindb.mapper.ToxicityMapper;
import com.yy.mushroomtoxindb.mapper.MolecularActivityMapper;
import com.yy.mushroomtoxindb.service.CompoundService;
import com.yy.mushroomtoxindb.service.FungusService;
import com.yy.mushroomtoxindb.service.chem.ChemSearchService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class MushroomController {

    @Autowired private CompoundService compoundService;
    @Autowired private FungusService fungusService;
    @Autowired private ChemSearchService chemSearchService;
    @Autowired private SubmissionMapper submissionMapper;
    @Autowired private ToxicityMapper toxicityMapper;
    @Autowired private MolecularActivityMapper activityMapper;

    // 1.1 化合物列表
//    @GetMapping("/compounds")
//    public Page<Compound> listCompounds(@RequestParam(defaultValue = "1") int page) {
//        return compoundService.page(new Page<>(page, 10),
//                new QueryWrapper<Compound>().orderByAsc("common_name"));
//    }
    @GetMapping("/compounds")
    public Page<Compound> listCompounds(@RequestParam(defaultValue = "1") int page,
                                       @RequestParam(defaultValue = "toxicity") String sortBy) {
        Page<Compound> resultPage = new Page<>(page, 10);

        if ("toxicity".equals(sortBy)) {
            // 按毒性数量倒序排序（默认）
            return compoundService.pageCompoundsWithToxicityCount(resultPage);
        } else {
            // 按名称升序排序
            return compoundService.page(resultPage,
                    new QueryWrapper<Compound>().orderByAsc("common_name"));
        }
    }


    // 1.2 蘑菇列表
    @GetMapping("/fungi")
    public Page<FungusInfo> listFungi(@RequestParam(defaultValue = "1") int page) {
        return fungusService.page(new Page<>(page, 10),
                new QueryWrapper<FungusInfo>().orderByAsc("fungus_name"));
    }

    // 1.3 & 1.4 按ID查看化合物/蘑菇详情

    @GetMapping("/compound/{id}")
    public CompoundDetailDTO getCompoundDetail(@PathVariable Integer id) {
        return compoundService.getCompoundDetail(id);
    }

    @GetMapping("/fungus/{id}")
    public FungusDetailDTO getFungusDetail(@PathVariable Integer id) {
        return fungusService.getFungusDetail(id);
    }

    // 2.1 化合物名称搜索
    @GetMapping("/search/compound/name")
    public List<Compound> searchCompoundByName(@RequestParam String name) {
        return compoundService.list(new QueryWrapper<Compound>()
                .like("common_name", name)
                .or().like("other_name", name));
    }

    // 2.2 SMILES 搜索保持不变（Service 内部处理）
    @GetMapping("/search/compound/smiles")
    public List<Map<String, Object>> searchBySmiles(@RequestParam String querySmiles) {
        // 复用之前的逻辑，略
        List<Compound> allCompounds = compoundService.list();
        List<Map<String, Object>> results = new ArrayList<>();
        for (Compound c : allCompounds) {
            if (c.getSmiles() == null) continue;
            double similarity = chemSearchService.calculateSimilarity(querySmiles, c.getSmiles());
            if (similarity > 0.70) {
                Map<String, Object> map = new HashMap<>();
                map.put("compoundId", c.getCompoundId());
                map.put("commonName", c.getCommonName()); // 这里用 Getter，不受列名影响
                map.put("molecularFormula", c.getMolecularFormula());
                map.put("cas", c.getCas());
                map.put("fileSource", c.getFileSource());
                map.put("similarity", String.format("%.2f", similarity));
                results.add(map);
            }
        }
        results.sort((a, b) -> Double.compare(
                Double.parseDouble((String) b.get("similarity")),
                Double.parseDouble((String) a.get("similarity"))));
        return results;
    }

    /*
    //  小孩子不懂事优化着玩的
    @GetMapping("/search/compound/smilesNew")
    public List<Map<String, Object>> searchBySmilesNew(@RequestParam String querySmiles) {
        // 预计算查询化合物的指纹
        IBitFingerprint queryFingerprint = null;
        try {
            SmilesParser sp = new SmilesParser(SilentChemObjectBuilder.getInstance());
            IAtomContainer queryMolecule = sp.parseSmiles(querySmiles);
            MACCSFingerprinter printer = new MACCSFingerprinter();
            queryFingerprint = printer.getBitFingerprint(queryMolecule);
        } catch (Exception e) {
            // 查询化合物解析失败，直接返回空列表
            return new ArrayList<>();
        }

        List<Compound> allCompounds = compoundService.list();
        List<Map<String, Object>> results = new ArrayList<>();

        for (Compound c : allCompounds) {
            if (c.getSmiles() == null) continue;

            // 使用优化后的相似度计算方法
            double similarity = chemSearchService.calculateSimilarityNew(queryFingerprint, c.getSmiles());

            if (similarity > 0.70) {
                Map<String, Object> map = new HashMap<>();
                map.put("compoundId", c.getCompoundId());
                map.put("commonName", c.getCommonName());
                map.put("molecularFormula", c.getMolecularFormula());
                map.put("cas", c.getCas());
                map.put("fileSource", c.getFileSource());
                map.put("similarity", String.format("%.2f", similarity));
                results.add(map);
            }
        }

        results.sort((a, b) -> Double.compare(
                Double.parseDouble((String) b.get("similarity")),
                Double.parseDouble((String) a.get("similarity"))));

        return results;
    }   */


    // 2.3 CAS号搜索
    @GetMapping("/search/compound/cas")
    public List<Compound> searchByCas(@RequestParam String cas) {
        // 【修改点】列名改为 "cas" (小写)
        return compoundService.list(new QueryWrapper<Compound>().eq("cas", cas));
    }

    // 2.4 蘑菇名称搜索
    @GetMapping("/search/fungus/name")
    public List<FungusDetailDTO> searchFungusByName(@RequestParam String name) {
        // 【修改点】列名改为 "fungus_name"
        List<FungusInfo> fungi = fungusService.list(
                new QueryWrapper<FungusInfo>().like("fungus_name", name));
        return fungi.stream()
                .map(f -> fungusService.getFungusDetail(f.getFungusId()))
                .collect(Collectors.toList());
    }

    // 2.5 蘑菇 Family 搜索
    @GetMapping("/search/fungus/family")
    public List<FungusInfo> searchFungusByFamily(@RequestParam String family) {
        return fungusService.list(new QueryWrapper<FungusInfo>()
                //.select("fungus_id", "fungus_name", "ncbi_taxonomy_id", "genus")
                .eq("family", family));
    }

    // 2.5 蘑菇 genus 搜索
    @GetMapping("/search/fungus/genus")
    public List<FungusInfo> searchFungusByGenus(@RequestParam String genus) {
        return fungusService.list(new QueryWrapper<FungusInfo>()
                //.select("fungus_id", "fungus_name", "ncbi_taxonomy_id", "genus")
                .eq("genus", genus));
    }

    // 3.1 提交
    @PostMapping("/submit")
    public String submitData(@RequestBody Submission submission) {
        submission.setSubmitTime(new Date());
        submissionMapper.insert(submission);
        return "Submission received";
    }

    // 4. 统计
    @GetMapping("/statistics")
    public Map<String, Long> getDatabaseStats() {
        Map<String, Long> stats = new HashMap<>();
        stats.put("totalCompounds", (long) compoundService.count());
        stats.put("totalFungi", (long) fungusService.count());
        stats.put("totalToxicityRecords", (long) toxicityMapper.selectCount(null));
        stats.put("totalActivityRecords", (long) activityMapper.selectCount(null));
        return stats;
    }
}