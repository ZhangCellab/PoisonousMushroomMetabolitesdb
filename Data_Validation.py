import os
import re
import sys
import csv
import json
import argparse
import unicodedata
import traceback
import datetime
import collections
import pandas as pd

EXIT_OK, EXIT_FAIL, EXIT_ABORT = 0, 1, 2

ENCODINGS = ['utf-8-sig', 'utf-8', 'gbk', 'gb2312', 'latin-1']

NULL_TOKENS = {'-', '', 'na', 'n/a', 'null', 'none', 'nan', 'nd'}

DEFAULT_DIR = os.path.dirname(os.path.abspath(__file__))

MW_ABS_TOL = 0.05

ADMET_ENDPOINTS = [
    'physchem_mw', 'physchem_vol', 'physchem_dense', 'physchem_nha',
    'physchem_nhd', 'physchem_tpsa', 'physchem_nrot', 'physchem_nring',
    'physchem_max_ring', 'physchem_nhet', 'physchem_fchar', 'physchem_nrig',
    'physchem_flex', 'physchem_nstereo', 'physchem_logs', 'physchem_logd',
    'physchem_logp', 'physchem_mp', 'physchem_bp', 'physchem_pka_acidic',
    'physchem_pka_basic',
    'abs_caco2', 'abs_mdck', 'abs_f20', 'abs_f30', 'abs_f50', 'abs_hia',
    'abs_pgp_inh', 'abs_pgp_sub', 'abs_pampa',
    'dist_logvdss', 'dist_fu', 'dist_ppb', 'dist_mrp1', 'dist_oatp1b1',
    'dist_oatp1b3', 'dist_bcrp', 'dist_bsep', 'dist_bbb',
    'met_cyp1a2_inh', 'met_cyp1a2_sub', 'met_cyp2c19_inh', 'met_cyp2c19_sub',
    'met_cyp2c9_inh', 'met_cyp2c9_sub', 'met_cyp2d6_inh', 'met_cyp2d6_sub',
    'met_cyp3a4_inh', 'met_cyp3a4_sub', 'met_cyp2b6_inh', 'met_cyp2b6_sub',
    'met_cyp2c8_inh', 'met_lm_human',
    'exc_t_half', 'exc_cl_plasma',
    'tox_a549', 'tox_ames', 'tox_carcinogenicity', 'tox_dili', 'tox_ec',
    'tox_ei', 'tox_fdamdd', 'tox_genotoxicity', 'tox_h_ht', 'tox_hek293',
    'tox_hematotoxicity', 'tox_herg_10um', 'tox_herg',
    'tox_nephrotoxicity_di', 'tox_neurotoxicity_di', 'tox_ototoxicity',
    'tox_respiratory', 'tox_roa', 'tox_rpmi_8226', 'tox_skin_sen',
]

SCHEMA = {
    'Compounds': {
        'file': 'Compounds.tsv',
        'cols': ['compound_id', 'common_name', 'synonyms', 'compound_class',
                 'pubchem_cid', 'chebi_id', 'cas_no', 'molecular_formula',
                 'smiles', 'inchi', 'inchi_key'],
    },
    'Taxa': {
        'file': 'Taxa.tsv',
        'cols': ['taxon_id', 'scientific_name', 'ncbi_taxonomy_id',
                 'phylum_name', 'class_name', 'order_name', 'family_name',
                 'genus_name'],
    },
    'ADMET_Predictions': {
        'file': 'ADMET_Predictions.tsv',
        'cols': ['compound_id'] + ADMET_ENDPOINTS,
    },
    'Toxicity': {
        'file': 'Toxicity.tsv',
        'cols': ['toxicity_id', 'compound_id', 'toxicity_type', 'result_type',
                 'toxicity_endpoint', 'comparator', 'toxicity_value',
                 'toxicity_value_min', 'toxicity_value_max', 'variability_value',
                 'variability_type', 'toxicity_unit', 'exposure_duration_h',
                 'exposure_value', 'exposure_unit', 'administration_route',
                 'assay_method', 'test_system', 'effect_description',
                 'reported_result', 'toxicity_mechanism_id', 'reference_id'],
    },
    'Toxicity_Mechanism': {
        'file': 'Toxicity_Mechanism.tsv',
        'cols': ['toxicity_mechanism_id', 'compound_id', 'description',
                 'reference_id_1', 'reference_id_2'],
    },
    'Bioactivity_Target': {
        'file': 'Bioactivity_Target.tsv',
        'cols': ['bioactivity_id', 'compound_id', 'target_name', 'action_mode',
                 'activity_metric', 'result_type', 'value_relation',
                 'activity_value', 'activity_unit', 'activity_result',
                 'target_species', 'reported_result', 'reference_id'],
    },
    'Compound_Species_Evidence': {
        'file': 'Compound_Species_Evidence.tsv',
        'cols': ['evidence_id', 'compound_id', 'taxon_id', 'reference_id'],
    },
    'Referrences': {
        'file': 'Referrences.tsv',
        'cols': ['reference_id', 'reference_type', 'reference_identifier',
                 'reference_url'],
    },
}

PK = {'Compounds': 'compound_id', 'Taxa': 'taxon_id',
      'Toxicity': 'toxicity_id', 'Toxicity_Mechanism': 'toxicity_mechanism_id',
      'Bioactivity_Target': 'bioactivity_id',
      'Compound_Species_Evidence': 'evidence_id',
      'ADMET_Predictions': 'compound_id', 'Referrences': 'reference_id'}

PK_RE = {'compound_id': r'^COM\d{6}$', 'taxon_id': r'^TAX\d{6}$',
         'toxicity_id': r'^TOX\d{8}$',
         'toxicity_mechanism_id': r'^MECH\d{6}$',
         'bioactivity_id': r'^BAT\d{6}$', 'evidence_id': r'^EVI\d{6}$',
         'reference_id': r'^REF\d{6}$'}

PROBABILITY_ENDPOINTS = {
    'abs_f20', 'abs_f30', 'abs_f50', 'abs_hia', 'abs_pgp_inh', 'abs_pgp_sub',
    'abs_pampa',
    'dist_mrp1', 'dist_oatp1b1', 'dist_oatp1b3', 'dist_bcrp', 'dist_bsep',
    'dist_bbb',
    'met_cyp1a2_inh', 'met_cyp1a2_sub', 'met_cyp2c19_inh', 'met_cyp2c19_sub',
    'met_cyp2c9_inh', 'met_cyp2c9_sub', 'met_cyp2d6_inh', 'met_cyp2d6_sub',
    'met_cyp3a4_inh', 'met_cyp3a4_sub', 'met_cyp2b6_inh', 'met_cyp2b6_sub',
    'met_cyp2c8_inh', 'met_lm_human',
    'tox_a549', 'tox_ames', 'tox_carcinogenicity', 'tox_dili', 'tox_ec',
    'tox_ei', 'tox_fdamdd', 'tox_genotoxicity', 'tox_h_ht', 'tox_hek293',
    'tox_hematotoxicity', 'tox_herg_10um', 'tox_herg',
    'tox_nephrotoxicity_di', 'tox_neurotoxicity_di', 'tox_ototoxicity',
    'tox_respiratory', 'tox_roa', 'tox_rpmi_8226', 'tox_skin_sen',
}

REFERENCE_COLUMNS = [
    ('Toxicity', 'reference_id'),
    ('Bioactivity_Target', 'reference_id'),
    ('Compound_Species_Evidence', 'reference_id'),
    ('Toxicity_Mechanism', 'reference_id_1'),
    ('Toxicity_Mechanism', 'reference_id_2'),
]

EXPECTED_ROWS = {'Compounds': 674, 'Taxa': 235}

def setup_stdout():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

def print_section(title):
    print(f"\n=== {title} ===")

def norm(value):
    s = unicodedata.normalize('NFKC', '' if value is None else str(value))
    for ch in ('\xa0', '\u2009', '\u202f'):
        s = s.replace(ch, ' ')
    return re.sub(r'\s+', ' ', s).strip()

def is_null(value):
    return norm(value).lower() in NULL_TOKENS

def rate(a, b):
    return (a / b * 100) if b else None

def fmt_rate(a, b):
    r = rate(a, b)
    return 'n/a' if r is None else f'{r:.2f}%'

def read_table(base_dir, name, schema_issues):
    spec = SCHEMA[name]
    path = os.path.join(base_dir, spec['file'])
    if not os.path.exists(path):
        print(f"  error: file not found: {path}")
        schema_issues.append({'table': name, 'issue': 'file_missing',
                              'detail': path})
        return None, None
    for encoding in ENCODINGS:
        try:
            with open(path, encoding=encoding, newline='') as fh:
                rows = list(csv.reader(fh, delimiter='\t'))
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"  read failed {path}: {e}")
            traceback.print_exc()
            schema_issues.append({'table': name, 'issue': 'unreadable',
                                  'detail': str(e)})
            return None, None
    else:
        print(f"  cannot read (all encodings failed): {path}")
        schema_issues.append({'table': name, 'issue': 'unreadable',
                              'detail': 'all encodings failed'})
        return None, None
    if not rows:
        print(f"  error: file is empty: {path}")
        schema_issues.append({'table': name, 'issue': 'empty', 'detail': ''})
        return None, None
    cols = spec['cols']
    header = [norm(c) for c in rows[0]]
    data = rows[1:]
    missing = [c for c in cols if c not in header]
    extra = [c for c in header if c not in cols]
    if missing or extra:
        schema_issues.append({
            'table': name, 'issue': 'column_mismatch',
            'detail': f'missing {missing} / extra {extra}',
        })
        print(f"  ✗ {spec['file']}: header does not match the declaration")
        if missing:
            print(f"      missing columns: {missing}")
        if extra:
            print(f"      extra columns: {extra}")
    elif header != cols:
        schema_issues.append({
            'table': name, 'issue': 'column_order',
            'detail': 'same column names in a different order; reordered to the declared order',
        })
        print(f"  ⚠ {spec['file']}: same column names, different order; reordered to the declared order")
    idx = {c: i for i, c in enumerate(header)}
    out = []
    for r in data:
        out.append([r[idx[c]] if (c in idx and idx[c] < len(r)) else '-'
                    for c in cols])
    short = sum(1 for r in data if len(r) != len(header))
    if short:
        schema_issues.append({
            'table': name, 'issue': 'ragged_rows',
            'detail': f'{short} rows have a column count different from the header ({len(header)})',
        })
        print(f"  ⚠ {spec['file']}: {short} rows have a column count different from the header")
    return pd.DataFrame(out, columns=cols), cols

def write_csv(rows, path):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or '.', exist_ok=True)
    if not rows:
        rows = [{'info': 'no issues found'}]
    if isinstance(rows[0], dict):
        pd.DataFrame(rows).to_csv(path, index=False, encoding='utf-8-sig')
    else:
        pd.DataFrame(rows).to_csv(path, index=False, header=False,
                                  encoding='utf-8-sig')
    print(f"    written: {path}  ({len(rows)} rows)")

class Summary:
    def __init__(self):
        self.rows = []
    def add(self, section, metric, value, numerator=None, denominator=None,
            status='INFO', note=''):
        self.rows.append({
            'section': section,
            'metric': metric,
            'value': value,
            'numerator': '' if numerator is None else numerator,
            'denominator': '' if denominator is None else denominator,
            'rate_pct': fmt_rate(numerator, denominator) if denominator else '',
            'status': status,
            'note': note,
        })
        mark = {'PASS': '✓', 'FAIL': '✗', 'REVIEW': '⚠', 'N/A': '-', 'INFO': 'ℹ'}[status]
        extra = ''
        if denominator:
            extra = f'   ({numerator}/{denominator} = {fmt_rate(numerator, denominator)})'
        print(f"  {mark} {metric}: {value}{extra}")
        if note:
            print(f"      {note}")
    def to_frame(self):
        return pd.DataFrame(self.rows)

def count_status(s, kind):
    return sum(1 for r in s.rows if r['status'] == kind)

def check_compounds(c, s, details):
    from rdkit import Chem, RDLogger
    from rdkit.Chem.Descriptors import ExactMolWt
    from rdkit.Chem.rdMolDescriptors import CalcMolFormula
    RDLogger.DisableLog('rdApp.*')
    SEC = 'Compound level'
    df = c['Compounds']
    n = len(df)
    exp = EXPECTED_ROWS.get('Compounds')
    s.add(SEC, 'compounds', n,
          status='PASS' if n == exp else 'FAIL',
          note=f'expected {exp}' + ('' if n == exp else ' (row count drifted; confirm)'))
    issues = []
    non_standard = []
    ok_smiles = ok_inchi_col = ok_inchikey = ok_formula = ok_mw = 0
    inchi_conn = inchi_stereo = inchi_compared = 0
    conn_diff = stereo_diff = 0
    assigned = unassigned_any = 0
    multi_component = 0
    smokeys = collections.defaultdict(set)
    admet = c['ADMET_Predictions']
    for _, r in df.iterrows():
        cid = norm(r['compound_id'])
        smi = norm(r['smiles'])
        inchi_col = norm(r['inchi'])
        ik_col = norm(r['inchi_key'])
        form_col = norm(r['molecular_formula'])
        mol = None
        if is_null(smi):
            issues.append({'compound_id': cid, 'check': 'smiles_parse',
                           'detail': 'empty SMILES', 'value': smi})
        else:
            try:
                mol = Chem.MolFromSmiles(smi)
            except Exception as e:
                mol = None
                issues.append({'compound_id': cid, 'check': 'smiles_parse',
                               'detail': f'parse raised: {type(e).__name__}',
                               'value': smi[:80]})
            if mol is None:
                if not any(i['compound_id'] == cid and i['check'] == 'smiles_parse'
                           for i in issues):
                    issues.append({'compound_id': cid, 'check': 'smiles_parse',
                                   'detail': 'RDKit could not parse', 'value': smi[:80]})
            else:
                ok_smiles += 1
        mol_from_inchi = None
        if is_null(inchi_col):
            issues.append({'compound_id': cid, 'check': 'inchi_parse',
                           'detail': 'empty InChI column', 'value': ''})
        else:
            if not inchi_col.startswith('InChI=1S/'):
                non_standard.append(
                    {'compound_id': cid, 'check': 'inchi_not_standard',
                     'detail': 'non-standard InChI (missing the /S flag)',
                     'value': inchi_col[:60] + '...'})
            try:
                mol_from_inchi = Chem.MolFromInchi(inchi_col)
            except Exception as e:
                mol_from_inchi = None
                issues.append({'compound_id': cid, 'check': 'inchi_parse',
                               'detail': f'parse raised: {type(e).__name__}',
                               'value': inchi_col[:80]})
            if mol_from_inchi is not None:
                ok_inchi_col += 1
            elif not any(i['compound_id'] == cid and i['check'] == 'inchi_parse'
                         for i in issues):
                tail = inchi_col[-20:]
                issues.append({'compound_id': cid, 'check': 'inchi_parse',
                               'detail': f'RDKit could not parse the InChI column '
                                         f'({len(inchi_col)} chars, ends with {tail!r})',
                               'value': inchi_col[:80]})
        if mol is None:
            continue
        calc_ik = Chem.MolToInchiKey(mol)
        if is_null(ik_col):
            issues.append({'compound_id': cid, 'check': 'inchikey_consistency',
                           'detail': 'empty InChIKey column', 'value': ''})
        elif calc_ik != ik_col:
            a, b = calc_ik.split('-'), ik_col.split('-')
            if a[0] != b[0]:
                conn_diff += 1
                issues.append({'compound_id': cid, 'check': 'inchikey_backbone',
                               'detail': 'backbone layer mismatch (severe)',
                               'value': f'{ik_col} vs {calc_ik}'})
            else:
                stereo_diff += 1
                issues.append({'compound_id': cid, 'check': 'inchikey_stereo',
                               'detail': 'stereo layer mismatch (same backbone)',
                               'value': f'{ik_col} vs {calc_ik}'})
        else:
            ok_inchikey += 1
        if mol_from_inchi is not None:
            inchi_compared += 1
            try:
                k_inchi = Chem.MolToInchiKey(mol_from_inchi)
                k_smi = Chem.MolToInchiKey(mol)
                if k_inchi != k_smi:
                    a, b = k_inchi.split('-'), k_smi.split('-')
                    kind = 'inchi_backbone' if a[0] != b[0] else 'inchi_stereo'
                    if a[0] != b[0]:
                        inchi_conn += 1
                    else:
                        inchi_stereo += 1
                    detail = ('InChI column and SMILES differ in the backbone layer (severe)'
                              if a[0] != b[0] else
                              'InChI column and SMILES differ in the stereo layer (same backbone)')
                    issues.append({'compound_id': cid, 'check': kind,
                                   'detail': detail,
                                   'value': f'InChI column {k_inchi} vs SMILES {k_smi}'})
            except Exception:
                pass
        calc_form = CalcMolFormula(mol)
        def strip_charge(f):
            return re.sub(r'[+-]\d*$', '', f.replace(' ', ''))
        if is_null(form_col):
            issues.append({'compound_id': cid, 'check': 'formula',
                           'detail': 'empty molecular formula', 'value': ''})
        elif strip_charge(form_col) == strip_charge(calc_form):
            ok_formula += 1
            if form_col.replace(' ', '') != calc_form:
                issues.append({'compound_id': cid, 'check': 'formula_charge_notation',
                               'detail': 'same elemental composition, different charge notation',
                               'value': f'table {form_col} vs computed {calc_form}'})
        else:
            issues.append({'compound_id': cid, 'check': 'formula',
                           'detail': 'molecular formula mismatch',
                           'value': f'table {form_col} vs computed {calc_form}'})
        if admet is not None and 'physchem_mw' in admet.columns:
            sub = admet[admet['compound_id'] == cid]
            if len(sub) == 0:
                issues.append({'compound_id': cid, 'check': 'mw',
                               'detail': 'no corresponding row in the ADMET table', 'value': ''})
            else:
                v = norm(sub.iloc[0]['physchem_mw'])
                try:
                    mw = float(v)
                    d = ExactMolWt(mol) - mw
                    if abs(d) > MW_ABS_TOL:
                        issues.append({'compound_id': cid, 'check': 'mw',
                                       'detail': 'monoisotopic mass mismatch',
                                       'value': f'table {mw:.2f} vs computed {ExactMolWt(mol):.4f} (delta {d:+.4f})'})
                    else:
                        ok_mw += 1
                except ValueError:
                    issues.append({'compound_id': cid, 'check': 'mw',
                                   'detail': f'MW is not numeric: {v!r}', 'value': v})
        try:
            centres = Chem.FindMolChiralCenters(
                mol, includeUnassigned=True, useLegacyImplementation=False)
        except Exception:
            centres = []
        na = sum(1 for _, t in centres if t == '?')
        assigned += len(centres) - na
        if na:
            unassigned_any += 1
        if '.' in smi or len(Chem.GetMolFrags(mol)) > 1:
            multi_component += 1
        try:
            smokeys[Chem.MolToSmiles(mol)].add(cid)
        except Exception:
            pass
        if not is_null(ik_col):
            smokeys[ik_col].add(cid)
    s.add(SEC, 'SMILES parse success', f'{ok_smiles}/{n}', ok_smiles, n,
          'PASS' if ok_smiles == n else 'FAIL',
          'RDKit MolFromSmiles')
    s.add(SEC, 'InChI parse success', f'{ok_inchi_col}/{n}', ok_inchi_col, n,
          'PASS' if ok_inchi_col == n else 'FAIL',
          'RDKit MolFromInchi (the InChI column itself parses)')
    s.add(SEC, 'InChI standard notation', f'{n - len(non_standard)}/{n}',
          n - len(non_standard), n,
          'PASS' if not non_standard else 'REVIEW',
          'InChI should use standard notation InChI=1S/; non-standard InChI=1/ cannot be string-compared with standard notation')
    for x in non_standard:
        issues.append(x)
    s.add(SEC, 'SMILES ↔ InChI column consistency (backbone)',
          f'{inchi_compared - inchi_conn}/{inchi_compared}',
          inchi_compared - inchi_conn, inchi_compared,
          'PASS' if inchi_conn == 0 else 'FAIL',
          f'Compared via canonical InChIKey (independent of InChI notation); a '
          f'backbone mismatch is a severe error. {n - inchi_compared} more could not be compared (broken InChI column)')
    s.add(SEC, 'SMILES ↔ InChI column stereo differences', inchi_stereo,
          inchi_stereo, inchi_compared, 'REVIEW' if inchi_stereo else 'PASS',
          'InChI column and SMILES share a backbone but differ in stereo')
    s.add(SEC, 'SDF structure parse success', 'N/A',
          status='N/A',
          note='this release contains no SDF file; supply *.sdf and it will be validated automatically')
    s.add(SEC, 'SMILES ↔ InChIKey backbone consistency',
          f'{n - conn_diff}/{n}', n - conn_diff, n,
          'PASS' if conn_diff == 0 else 'FAIL',
          'connectivity (backbone) layer comparison; a mismatch is a severe error')
    s.add(SEC, 'SMILES ↔ InChIKey full consistency',
          f'{ok_inchikey}/{n}', ok_inchikey, n,
          'PASS' if ok_inchikey == n else 'REVIEW',
          f'includes the stereo layer; {stereo_diff} share a backbone but differ in stereo (review items, not errors)')
    s.add(SEC, 'molecular formula agreement', f'{ok_formula}/{n}', ok_formula, n,
          'PASS' if ok_formula == n else 'FAIL',
          'CalcMolFormula(SMILES) vs Compounds.molecular_formula')
    mw_denom = int((~df['compound_id'].isin([])).sum())
    s.add(SEC, 'MW agreement', f'{ok_mw}/{n}', ok_mw, n,
          'PASS' if ok_mw == n else 'FAIL',
          f'physchem_mw vs ExactMolWt, tolerance {MW_ABS_TOL} Da. '
          'Note this field stores the monoisotopic mass, not the average molecular weight')
    for label, col in [('PubChem CID coverage', 'pubchem_cid'),
                       ('ChEBI ID coverage', 'chebi_id'),
                       ('CAS coverage', 'cas_no')]:
        have = int((~df[col].map(is_null)).sum())
        s.add(SEC, label, f'{have}/{n}', have, n,
              'PASS' if have else 'REVIEW',
              'identifier coverage (informational; absence is not an error)')
    dup_groups = {k: sorted(v) for k, v in smokeys.items() if len(v) > 1}
    dup_ids = sorted({i for v in dup_groups.values() for i in v})
    s.add(SEC, 'duplicate structure count', len(dup_ids),
          len(dup_ids), n,
          'PASS' if not dup_ids else 'REVIEW',
          'determined by canonical SMILES / InChIKey; the same molecule appears more than once')
    for k, v in dup_groups.items():
        details['duplicate_structures'].append(
            {'key': k, 'compound_ids': ', '.join(v), 'count': len(v)})
    s.add(SEC, 'stereocentres defined', assigned,
          status='INFO', note='total stereocentres with an assigned configuration')
    s.add(SEC, 'compounds with undefined stereocentres', unassigned_any,
          unassigned_any, n,
          'INFO', 'compounds with at least one unassigned stereocentre (data completeness info)')
    s.add(SEC, 'multi-component / salt SMILES', multi_component,
          multi_component, n,
          'PASS' if multi_component == 0 else 'REVIEW',
          "SMILES contains '.' or the molecule has multiple fragments")
    details['compound_issues'] = issues
    return issues

def check_taxonomy(c, s, details, base_dir, online, cache_path):
    SEC = 'Taxonomy level'
    df = c['Taxa']
    n = len(df)
    exp = EXPECTED_ROWS.get('Taxa')
    s.add(SEC, 'taxa', n, status='PASS' if n == exp else 'FAIL',
          note=f'expected {exp}' + ('' if n == exp else ' (row count drifted; confirm)'))
    issues = []
    have_id = invalid_fmt = 0
    taxids = []
    for _, r in df.iterrows():
        tid = norm(r['taxon_id'])
        v = norm(r['ncbi_taxonomy_id'])
        if is_null(v):
            issues.append({'taxon_id': tid, 'check': 'ncbi_taxonomy_id',
                           'detail': 'missing', 'value': v})
            continue
        if not re.fullmatch(r'\d+', v):
            invalid_fmt += 1
            issues.append({'taxon_id': tid, 'check': 'ncbi_taxonomy_id',
                           'detail': 'not a plain integer', 'value': v})
            continue
        have_id += 1
        taxids.append((tid, v))
    s.add(SEC, 'NCBI Taxonomy ID coverage', f'{have_id}/{n}', have_id, n,
          'PASS' if have_id == n else 'REVIEW',
          'coverage of valid (plain integer) taxids')
    unresolved = [i for i in issues]
    cache = {}
    if cache_path and os.path.exists(cache_path):
        try:
            with open(cache_path, encoding='utf-8') as fh:
                cache = json.load(fh).get('records', {})
        except Exception as e:
            print(f"  ⚠ NCBI cache unreadable ({type(e).__name__}); skipping the existence check")
    if online:
        try:
            import urllib.request
            for tid, v in taxids:
                url = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
                       f'esummary.fcgi?db=taxonomy&retmode=json&id={v}')
                with urllib.request.urlopen(url, timeout=20) as resp:
                    res = json.loads(resp.read().decode('utf-8')).get('result', {})
                if v not in res:
                    unresolved.append({'taxon_id': tid, 'check': 'ncbi_exists',
                                       'detail': 'taxid not found at NCBI', 'value': v})
            print("  (taxid existence checked online)")
        except Exception as e:
            print(f"  ⚠ online check failed ({type(e).__name__}); using cache/offline results only")
            online = False
    elif cache:
        nf = [{'taxon_id': tid, 'check': 'ncbi_exists',
               'detail': 'taxid absent from the NCBI cache (may be merged or deleted)', 'value': v}
              for tid, v in taxids if v not in cache]
        unresolved += nf
        print(f"  (offline: existence checked against the cache, {len(cache)} entries)")
    un_taxa = sorted({i['taxon_id'] for i in unresolved})
    s.add(SEC, 'unresolved taxa', len(un_taxa), len(un_taxa), n,
          'PASS' if not un_taxa else 'REVIEW',
          'missing / malformed' + (' / not found at NCBI' if (online or cache) else ''))
    syn = 0
    for _, r in df.iterrows():
        name = norm(r['scientific_name'])
        if re.search(r'[\(\[]\s*=', name) or re.search(r'\]\s*=', name):
            syn += 1
    s.add(SEC, 'taxa with synonym mappings', syn, syn, n, 'INFO',
          'synonyms embedded in scientific_name as (= ...) / [= ...]')
    for label, col in [('genus completeness', 'genus_name'),
                       ('family completeness', 'family_name'),
                       ('order completeness', 'order_name'),
                       ('class completeness', 'class_name'),
                       ('phylum completeness', 'phylum_name')]:
        have = int((~df[col].map(is_null)).sum())
        s.add(SEC, label, f'{have}/{n}', have, n,
              'PASS' if have == n else 'REVIEW',
              f'{col} non-null rate')
    details['taxonomy_issues'] = unresolved
    return None

def check_relational(c, s, details):
    SEC = 'Relational integrity'
    issues = []
    dup_pk_total = 0
    bad_pk_total = 0
    for tname, df in c.items():
        if df is None:
            continue
        pk = PK[tname]
        if pk not in df.columns:
            continue
        vals = [norm(v) for v in df[pk]]
        strict = [v for v in vals if not is_null(v)]
        dups = {k: n for k, n in collections.Counter(strict).items() if n > 1}
        dup_pk_total += sum(dups.values()) - len(dups)
        for k, nn in dups.items():
            issues.append({'table': tname, 'check': 'duplicate_pk',
                           'key': k, 'detail': f'appears {nn} times'})
        pat = PK_RE.get(pk)
        if pat:
            bad = [v for v in strict if not re.fullmatch(pat, v)]
            bad_pk_total += len(bad)
            for v in bad[:200]:
                issues.append({'table': tname, 'check': 'pk_format',
                               'key': v, 'detail': f'does not match {pat}'})
    s.add(SEC, 'duplicate primary keys', dup_pk_total,
          status='PASS' if dup_pk_total == 0 else 'FAIL',
          note='duplicate primary keys across all 8 tables')
    s.add(SEC, 'primary keys violating ID format', bad_pk_total,
          status='PASS' if bad_pk_total == 0 else 'FAIL',
          note='formats such as COM###### / TAX###### / TOX########')
    compound_ids = set(norm(v) for v in c['Compounds']['compound_id'])
    taxon_ids = set(norm(v) for v in c['Taxa']['taxon_id'])
    mech_ids = set(norm(v) for v in c['Toxicity_Mechanism']['toxicity_mechanism_id'])
    ref_ids = set(norm(v) for v in c['Referrences']['reference_id'])
    FK = [
        ('Toxicity', 'compound_id', compound_ids, 'compound_id'),
        ('Toxicity', 'toxicity_mechanism_id', mech_ids, 'mechanism_id'),
        ('Bioactivity_Target', 'compound_id', compound_ids, 'compound_id'),
        ('Compound_Species_Evidence', 'compound_id', compound_ids, 'compound_id'),
        ('Compound_Species_Evidence', 'taxon_id', taxon_ids, 'taxon_id'),
        ('Toxicity_Mechanism', 'compound_id', compound_ids, 'compound_id'),
        ('ADMET_Predictions', 'compound_id', compound_ids, 'compound_id'),
    ]
    counts = collections.Counter()
    for tname, col, valid, label in FK:
        df = c[tname]
        if df is None or col not in df.columns:
            counts[label] += 0
            continue
        bad = [norm(v) for v in df[col]
               if not is_null(v) and norm(v) not in valid]
        counts[label] += len(bad)
        for v in sorted(set(bad))[:100]:
            issues.append({'table': tname, 'check': f'fk_{col}',
                           'key': v, 'detail': f'{col} not present in the parent table'})
    ref_bad = 0
    for tname, col in REFERENCE_COLUMNS:
        df = c[tname]
        if df is None or col not in df.columns:
            continue
        bad = [norm(v) for v in df[col]
               if not is_null(v) and norm(v) not in ref_ids]
        ref_bad += len(bad)
        for v in sorted(set(bad))[:100]:
            issues.append({'table': tname, 'check': f'fk_{col}',
                           'key': v, 'detail': 'REF id not present in Referrences'})
    s.add(SEC, 'invalid compound_id', counts['compound_id'],
          status='PASS' if counts['compound_id'] == 0 else 'FAIL',
          note='orphan compound_id in Toxicity / Bioactivity / Evidence / Mechanism / ADMET')
    s.add(SEC, 'invalid taxon_id', counts['taxon_id'],
          status='PASS' if counts['taxon_id'] == 0 else 'FAIL',
          note='orphan taxon_id in Compound_Species_Evidence')
    s.add(SEC, 'invalid mechanism IDs', counts['mechanism_id'],
          status='PASS' if counts['mechanism_id'] == 0 else 'FAIL',
          note='orphan Toxicity.toxicity_mechanism_id (nullable)')
    s.add(SEC, 'invalid reference IDs', ref_bad,
          status='PASS' if ref_bad == 0 else 'FAIL',
          note='whether every reference column resolves in Referrences')
    ev = c['Compound_Species_Evidence']
    triples = [(norm(r['compound_id']), norm(r['taxon_id']), norm(r['reference_id']))
               for _, r in ev.iterrows()]
    dup3 = {k: n for k, n in collections.Counter(triples).items() if n > 1}
    s.add(SEC, 'duplicate compound–species–reference triples', len(dup3),
          len(dup3), len(triples),
          'PASS' if not dup3 else 'FAIL',
          'a compound-species-reference combination appearing more than once is a duplicate')
    for k, nn in sorted(dup3.items()):
        issues.append({'table': 'Compound_Species_Evidence',
                       'check': 'duplicate_triple',
                       'key': ' | '.join(k), 'detail': f'appears {nn} times'})
    dupr = {k: v for k, v in collections.Counter(
        norm(x) for x in c['Referrences']['reference_id']).items() if v > 1}
    s.add(SEC, 'duplicate reference IDs', len(dupr),
          status='PASS' if not dupr else 'FAIL',
          note='duplicate primary keys in Referrences')
    details['relational_issues'] = issues
    return None

def check_toxicology(c, s, details):
    SEC = 'Toxicology'
    df = c['Toxicity']
    n = len(df)
    ref_ids = set(norm(v) for v in c['Referrences']['reference_id'])
    issues = []
    s.add(SEC, 'toxicity records', n, status='INFO')
    have_ref = sum(1 for v in df['reference_id'] if not is_null(v))
    resolvable = sum(1 for v in df['reference_id']
                     if not is_null(v) and norm(v) in ref_ids)
    s.add(SEC, 'reference completeness', f'{have_ref}/{n}', have_ref, n,
          'PASS' if have_ref == n else 'FAIL', 'reference_id non-null rate')
    s.add(SEC, 'reference resolvable in Referrences', f'{resolvable}/{n}',
          resolvable, n, 'PASS' if resolvable == n else 'FAIL',
          'whether the REF id can be found in the Referrences table')
    for _, r in df.iterrows():
        v = r['reference_id']
        if is_null(v):
            issues.append({'toxicity_id': norm(r['toxicity_id']),
                           'check': 'reference_id', 'detail': 'reference missing', 'value': ''})
        elif norm(v) not in ref_ids:
            issues.append({'toxicity_id': norm(r['toxicity_id']),
                           'check': 'reference_id', 'detail': 'reference does not resolve',
                           'value': norm(v)})
    have_ep = sum(1 for v in df['toxicity_endpoint'] if not is_null(v))
    s.add(SEC, 'endpoint completeness', f'{have_ep}/{n}', have_ep, n, 'INFO',
          'toxicity_endpoint non-null rate; qualitative-observation records have no endpoint by design')
    gap_ep = []
    for _, r in df.iterrows():
        rt = norm(r['result_type'])
        if not rt.startswith('qualitative') and is_null(r['toxicity_endpoint']):
            gap_ep.append(norm(r['toxicity_id']))
            issues.append({'toxicity_id': norm(r['toxicity_id']),
                           'check': 'endpoint_missing',
                           'detail': f'non-qualitative record ({rt}) has no endpoint', 'value': ''})
    s.add(SEC, 'non-qualitative records missing an endpoint',
          len(gap_ep), len(gap_ep), n,
          'PASS' if not gap_ep else 'FAIL',
          'real endpoint gap after excluding qualitative observations')
    n_quant = sum(1 for v in df['result_type']
                  if norm(v).startswith('quantitative'))
    has_value = df['toxicity_value'].map(lambda v: not is_null(v))
    has_min = df['toxicity_value_min'].map(lambda v: not is_null(v))
    has_max = df['toxicity_value_max'].map(lambda v: not is_null(v))
    is_range = has_min & has_max
    has_result = has_value | is_range
    n_value = int(has_value.sum())
    n_range = int(is_range.sum())
    n_result = int(has_result.sum())
    unparseable = []
    for _, r in df.iterrows():
        for col in ('toxicity_value', 'toxicity_value_min', 'toxicity_value_max',
                    'variability_value'):
            v = norm(r[col])
            if is_null(v):
                continue
            try:
                float(v)
            except ValueError:
                unparseable.append({'toxicity_id': norm(r['toxicity_id']),
                                    'check': 'value_parse',
                                    'detail': f'{col} is not parseable as a number', 'value': v})
    s.add(SEC, 'numeric result completeness', f'{n_result}/{n}',
          n_result, n, 'PASS' if n_result >= n_quant else 'FAIL',
          f'{n_value} single values + {n_range} ranges (min/max); '
          f'{n_quant} quantitative records should all have a result')
    s.add(SEC, 'numeric values unparseable as float', len(unparseable),
          len(unparseable), status='PASS' if not unparseable else 'FAIL',
          note='cells in value / min / max / variability_value not parseable as numbers')
    issues += unparseable
    miss = []
    for _, r in df.iterrows():
        if not norm(r['result_type']).startswith('quantitative'):
            continue
        if not is_null(r['toxicity_value']):
            continue
        if not is_null(r['toxicity_value_min']) and not is_null(r['toxicity_value_max']):
            continue
        miss.append(norm(r['toxicity_id']))
        issues.append({'toxicity_id': norm(r['toxicity_id']),
                       'check': 'value_missing',
                       'detail': 'quantitative record with neither a single value nor a complete min/max', 'value': ''})
    s.add(SEC, 'quantitative records with no value and no complete range',
          len(miss), len(miss), n_quant,
          'PASS' if not miss else 'FAIL', 'quantitative records genuinely missing a result')
    half = []
    for _, r in df.iterrows():
        lo, hi = not is_null(r['toxicity_value_min']), not is_null(r['toxicity_value_max'])
        if lo != hi:
            half.append(norm(r['toxicity_id']))
            issues.append({'toxicity_id': norm(r['toxicity_id']),
                           'check': 'range_incomplete',
                           'detail': 'only one of min/max is filled',
                           'value': f"min={norm(r['toxicity_value_min'])} "
                                    f"max={norm(r['toxicity_value_max'])}"})
    s.add(SEC, 'incomplete value ranges', len(half),
          len(half), n, 'PASS' if not half else 'FAIL',
          'min and max must appear as a pair')
    inverted = []
    for _, r in df.iterrows():
        try:
            lo, hi = float(norm(r['toxicity_value_min'])), float(norm(r['toxicity_value_max']))
        except ValueError:
            continue
        if lo > hi:
            inverted.append(norm(r['toxicity_id']))
            issues.append({'toxicity_id': norm(r['toxicity_id']),
                           'check': 'range_inverted',
                           'detail': 'min > max', 'value': f'{lo} > {hi}'})
    s.add(SEC, 'inverted value ranges', len(inverted),
          len(inverted), n_range or 1, 'PASS' if not inverted else 'FAIL',
          'min should be <= max')
    served = int((has_result & df['toxicity_unit'].map(lambda v: not is_null(v))).sum())
    n_need = n_result
    s.add(SEC, 'unit completeness where applicable', f'{served}/{n_need}',
          served, n_need, 'PASS' if served == n_need else 'FAIL',
          'whether every record with a numeric result (single value or range) has a unit')
    for _, r in df.iterrows():
        v_ok = not is_null(r['toxicity_value'])
        r_ok = (not is_null(r['toxicity_value_min'])
                and not is_null(r['toxicity_value_max']))
        u_ok = not is_null(r['toxicity_unit'])
        if (v_ok or r_ok) and not u_ok:
            issues.append({'toxicity_id': norm(r['toxicity_id']),
                           'check': 'unit', 'detail': 'has a numeric result but no unit', 'value': ''})
        if not (v_ok or r_ok) and u_ok:
            issues.append({'toxicity_id': norm(r['toxicity_id']),
                           'check': 'unit', 'detail': 'has a unit but no numeric result at all',
                           'value': norm(r['toxicity_unit'])})
    dist = collections.Counter(norm(v) for v in df['result_type'])
    print(f"      result_type distribution: {dict(dist)}")
    structured = sum(v for k, v in dist.items() if k.startswith('quantitative'))
    s.add(SEC, 'structured (quantitative) records',
          f'{structured}/{n}', structured, n, 'INFO',
          'records whose result_type starts with quantitative')
    for k, v in sorted(dist.items()):
        s.add(SEC, f'  └ result_type = {k}', v, v, n, 'INFO')
    narrative = sum(1 for v in df['effect_description'] if not is_null(v))
    s.add(SEC, 'narrative records (effect_description present)',
          f'{narrative}/{n}', narrative, n, 'INFO',
          'records carrying a text description. The published schema has no separate "manually reviewed" flag')
    s.add(SEC, 'manually reviewed records', 'N/A', status='N/A',
          note='no review flag in the published schema; cannot be determined from the data')
    s.add(SEC, 'records subjected to random audit', 'N/A', status='N/A',
          note='same: no audit-sampling field. Add an audit_batch column to make this computable')
    linked = sum(1 for v in df['toxicity_mechanism_id'] if not is_null(v))
    s.add(SEC, 'records linked to a mechanism', f'{linked}/{n}', linked, n,
          'INFO', 'toxicity_mechanism_id non-null rate (the mechanism is optional supplementary information)')
    details['toxicology_issues'] = issues
    return None

def check_admet(c, s, details):
    SEC = 'ADMET'
    df = c['ADMET_Predictions']
    n = len(df)
    endpoints = [col for col in df.columns if col != 'compound_id']
    issues = []
    s.add(SEC, 'compounds with ADMET predictions', n, status='INFO')
    n_compounds = len(c['Compounds'])
    s.add(SEC, 'ADMET row count equals Compounds row count',
          f'{n}/{n_compounds}', n, n_compounds,
          'PASS' if n == n_compounds else 'FAIL',
          'ADMET is one-to-one with Compounds; the two must stay in sync')
    s.add(SEC, 'endpoints', len(endpoints),
          status='PASS' if len(endpoints) == 75 else 'FAIL',
          note='expected 75 endpoints; the actual column count excludes compound_id')
    print(f"      endpoint columns: {len(endpoints)}")
    missing = []
    for col in endpoints:
        for _, r in df.iterrows():
            if is_null(r[col]):
                missing.append({'compound_id': norm(r['compound_id']),
                                'endpoint': col, 'detail': 'missing'})
    s.add(SEC, 'missing predictions', len(missing),
          status='PASS' if not missing else 'FAIL',
          note='cell-level missing values (empty or placeholder)')
    issues += missing
    nonnumeric = []
    ranges = {}
    for col in endpoints:
        vals = []
        for _, r in df.iterrows():
            v = norm(r[col])
            if is_null(v):
                continue
            try:
                vals.append(float(v))
            except ValueError:
                nonnumeric.append({'compound_id': norm(r['compound_id']),
                                   'endpoint': col, 'value': v,
                                   'detail': 'not numeric'})
        if vals:
            ranges[col] = (min(vals), max(vals))
    s.add(SEC, 'numeric parsing', f'{n * len(endpoints) - len(nonnumeric)}/'
          f'{n * len(endpoints)}',
          n * len(endpoints) - len(nonnumeric), n * len(endpoints),
          'PASS' if not nonnumeric else 'FAIL',
          'every endpoint cell parses as a float')
    issues += nonnumeric
    viol = []
    for col in sorted(PROBABILITY_ENDPOINTS):
        if col not in df.columns:
            continue
        for _, r in df.iterrows():
            v = norm(r[col])
            if is_null(v):
                continue
            try:
                f = float(v)
            except ValueError:
                continue
            if not (0.0 <= f <= 1.0):
                viol.append({'compound_id': norm(r['compound_id']),
                             'endpoint': col, 'value': v,
                             'detail': 'probability out of range; must be in [0,1]'})
    n_checked = sum(1 for col in PROBABILITY_ENDPOINTS if col in df.columns)
    s.add(SEC, 'classification probabilities outside [0,1]', len(viol),
          len(viol), n * n_checked,
          status='PASS' if not viol else 'FAIL',
          note=f'only the {n_checked} endpoints that are semantically classification probabilities are checked (regression outputs excluded)')
    issues += viol
    empirical = {col for col, (lo, hi) in ranges.items()
                 if lo >= 0.0 and hi <= 1.0}
    only_sem = sorted(PROBABILITY_ENDPOINTS - empirical)
    only_emp = sorted(empirical - PROBABILITY_ENDPOINTS)
    s.add(SEC, 'probability endpoints (declared)',
          len(PROBABILITY_ENDPOINTS), status='INFO',
          note='count declared as classification probabilities by endpoint semantics')
    s.add(SEC, 'endpoints observed within [0,1]', len(empirical),
          status='INFO',
          note='data-driven range probe, for cross-checking against the declared list')
    if only_sem:
        s.add(SEC, 'declared probability endpoints with out-of-range values',
              len(only_sem), status='REVIEW',
              note=f'declared probabilities whose observed range is out of bounds: {", ".join(only_sem[:8])}')
    if only_emp:
        s.add(SEC, 'undefined endpoints observed within [0,1]',
              len(only_emp), status='INFO',
              note=f'not in the declared list but observed within [0,1]: {", ".join(only_emp[:8])}')
    for col in endpoints:
        if col in ranges:
            lo, hi = ranges[col]
            details['admet_ranges'].append({
                'endpoint': col, 'min': f'{lo:.6g}', 'max': f'{hi:.6g}',
                'declared_probability': 'Y' if col in PROBABILITY_ENDPOINTS else 'N',
                'observed_within_0_1': 'Y' if col in empirical else 'N'})
    details['admet_issues'] = issues
    return None

def main(argv=None):
    setup_stdout()
    parser = argparse.ArgumentParser(
        description='MushroomToxinDB pre-release validation package')
    parser.add_argument('--base-dir', default=DEFAULT_DIR,
                        help='FinalFiles directory')
    parser.add_argument('--out-dir', default=None,
                        help='output directory (default: same as --base-dir)')
    parser.add_argument('--online', action='store_true',
                        help='check NCBI taxid existence online (default: offline)')
    parser.add_argument('--cache', default=None,
                        help='path to the NCBI taxonomy cache json')
    parser.add_argument('--strict', action='store_true',
                        help='treat REVIEW as a failure too')
    args = parser.parse_args(argv)
    out_dir = args.out_dir or args.base_dir
    detail_dir = os.path.join(out_dir, 'validation_details')
    cache = args.cache or os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', 'scripts', 'reports', 'ncbi_taxonomy_cache.json')
    print('=== MushroomToxinDB pre-release validation ===')
    print(f"data directory: {args.base_dir}")
    print(f"output directory: {out_dir}")
    try:
        import rdkit
    except ImportError:
        print('error: rdkit is not installed. Run: pip install rdkit')
        return EXIT_ABORT
    print_section('0. Reading data')
    c = {}
    schema_issues = []
    for name in SCHEMA:
        df, cols = read_table(args.base_dir, name, schema_issues)
        if df is None:
            return EXIT_ABORT
        c[name] = df
        print(f"  {SCHEMA[name]['file']:32s} {len(df):5d} rows  {len(cols):3d} cols")
    s = Summary()
    details = collections.defaultdict(list)
    fatal = [i for i in schema_issues
             if i['issue'] in ('file_missing', 'unreadable', 'empty',
                               'column_mismatch')]
    s.add('Schema', 'tables with matching column names',
          f"{len(SCHEMA) - len({i['table'] for i in fatal})}/{len(SCHEMA)}",
          len(SCHEMA) - len({i['table'] for i in fatal}), len(SCHEMA),
          'PASS' if not fatal else 'FAIL',
          'file headers checked column by column against the declaration in validation.py')
    for i in schema_issues:
        if i['issue'] in ('column_order', 'ragged_rows'):
            s.add('Schema', f"{i['table']}: {i['issue']}", i['detail'],
                  status='REVIEW')
    for i in schema_issues:
        details['schema_issues'].append(i)
    print_section('A. Compound level')
    check_compounds(c, s, details)
    print_section('B. Taxonomy level')
    check_taxonomy(c, s, details, args.base_dir, args.online, cache)
    print_section('C. Relational integrity')
    check_relational(c, s, details)
    print_section('D. Toxicology')
    check_toxicology(c, s, details)
    print_section('E. ADMET')
    check_admet(c, s, details)
    print_section('Output')
    summary_path = os.path.join(out_dir, 'validation_summary.csv')
    write_csv(s.rows, summary_path)
    mapping = {
        'schema_issues': 'validation_schema_issues.csv',
        'compound_issues': 'validation_compound_issues.csv',
        'taxonomy_issues': 'validation_taxonomy_issues.csv',
        'relational_issues': 'validation_relational_issues.csv',
        'toxicology_issues': 'validation_toxicology_issues.csv',
        'admet_issues': 'validation_admet_issues.csv',
        'duplicate_structures': 'validation_duplicate_structures.csv',
        'admet_ranges': 'validation_admet_endpoint_ranges.csv',
    }
    for key, fname in mapping.items():
        write_csv(details.get(key, []), os.path.join(detail_dir, fname))
    n_fail = count_status(s, 'FAIL')
    n_review = count_status(s, 'REVIEW')
    n_pass = count_status(s, 'PASS')
    print_section('Result')
    print(f"  PASS {n_pass}   REVIEW {n_review}   FAIL {n_fail}   "
          f"N/A {count_status(s, 'N/A')}")
    if n_fail:
        print('  FAIL-level issues:')
        for r in s.rows:
            if r['status'] == 'FAIL':
                print(f"    ✗ [{r['section']}] {r['metric']}: {r['value']}")
    if n_review:
        print('  Needs human review:')
        for r in s.rows:
            if r['status'] == 'REVIEW':
                print(f"    ⚠ [{r['section']}] {r['metric']}: {r['value']}")
    if n_fail:
        code = EXIT_FAIL
    elif args.strict and n_review:
        code = EXIT_FAIL
    else:
        code = EXIT_OK
    print(f"exit code: {code}")
    return code

if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit(main(['--base-dir', DEFAULT_DIR]))
    sys.exit(main())
