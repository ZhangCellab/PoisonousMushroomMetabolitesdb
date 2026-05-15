package com.yy.mushroomtoxindb.service.chem;

import org.openscience.cdk.interfaces.IAtomContainer;
//import org.openscience.cdk.interfaces.IBitFingerprint;
import org.openscience.cdk.fingerprint.IBitFingerprint;
import org.openscience.cdk.silent.SilentChemObjectBuilder;
import org.openscience.cdk.smiles.SmilesParser;
import org.openscience.cdk.fingerprint.MACCSFingerprinter;
import org.openscience.cdk.similarity.Tanimoto;
import org.springframework.stereotype.Service;

@Service
public class ChemSearchService {

    /**
     * 需求 2.2: 使用 Tanimoto 系数计算 MACCS 指纹相似度
     */
    public double calculateSimilarity(String querySmiles, String targetSmiles) {
        try {
            SmilesParser sp = new SmilesParser(SilentChemObjectBuilder.getInstance());
            IAtomContainer m1 = sp.parseSmiles(querySmiles);
            IAtomContainer m2 = sp.parseSmiles(targetSmiles);

            MACCSFingerprinter printer = new MACCSFingerprinter();
            IBitFingerprint fp1 = printer.getBitFingerprint(m1);
            IBitFingerprint fp2 = printer.getBitFingerprint(m2);

            return Tanimoto.calculate(fp1, fp2);
        } catch (Exception e) {
            // 解析失败（如 SMILES 格式错误）返回 0
            return 0.0;
        }
    }

//    小孩子不懂事优化着玩的
//    public double calculateSimilarityNew(IBitFingerprint queryFingerprint, String targetSmiles) {
//        try {
//            SmilesParser sp = new SmilesParser(SilentChemObjectBuilder.getInstance());
//            IAtomContainer targetMolecule = sp.parseSmiles(targetSmiles);
//            MACCSFingerprinter printer = new MACCSFingerprinter();
//            IBitFingerprint targetFingerprint = printer.getBitFingerprint(targetMolecule);
//
//            return Tanimoto.calculate(queryFingerprint, targetFingerprint);
//        } catch (Exception e) {
//            // 目标化合物解析失败返回 0
//            return 0.0;
//        }
//    }
}