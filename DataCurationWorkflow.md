# PMMdb Data Curation Workflow

## 1. Overview

The Poisonous Mushroom Metabolites Dataset (PMMdb) was developed through literature retrieval, manual data extraction, data restructuring, annotation, and technical validation. It brings together information on compounds reported from poisonous mushrooms, their source taxa, experimental toxicological observations, biological activities, and supporting literature.

The initial dataset was compiled manually in three CSV tables. The first version was deposited in Figshare (v1: https://doi.org/10.6084/m9.figshare.32647398.v1). During the subsequent revision of the dataset, the original tables were substantially reorganized to improve data structure, define relationships between records, and make the supporting literature easier to trace. This work resulted in eight interconnected TSV tables, together with standardized chemical structures and accompanying documentation.

This document describes the process from the initial literature-based compilation to the current relational dataset.

## 2. Candidate Species Selection and Literature Retrieval

The initial search scope covered 643 candidate poisonous mushroom species, selected primarily from the global compilation reported by He et al. For each species, literature searches were conducted in SciFinder, PubMed, and China National Knowledge Infrastructure (CNKI), using its current scientific name together with documented synonyms and previously used names.

Systematic species-specific searches began in September 2024, with supplementary searches continuing until 15 October 2025. Searches were conducted primarily in the Abstract and Keywords fields and were extended to all available search fields when no relevant records were retrieved. No language restrictions were imposed.

Search terms included "metabolite", "secondary metabolite", "compound", "toxin", "isolation", "structure", "toxicity", "toxicology", "cytotoxicity", "LD50", "IC50", and "EC50". These terms were used to guide literature retrieval and screening rather than as components of a single standardized Boolean search query.

## 3. Literature Screening and Eligibility Criteria

Retrieved publications were manually examined for reports of defined secondary metabolites and compound-specific toxicological information associated with the candidate mushroom species.

Compound records were included when a defined secondary metabolite was explicitly reported as isolated from or present in a specific mushroom taxon, with a clear compound–taxon association supported by traceable literature evidence. Both newly characterized and previously known compounds were eligible, provided that their identities could be established from the source publication or traced to earlier identification reports. The analytical evidence for compound identification was assessed in the context of the methods used in each publication. Historical analytical approaches, including thin-layer chromatography (TLC), were not excluded solely because they predated modern spectroscopic techniques, provided that the reported evidence supported the compound identification.

Reports describing only primary metabolites, crude extracts, mixed fractions, compounds with undefined structures, or records lacking a clear compound–taxon association were excluded. Toxicological records were included only when they could be linked to an identified compound and were directly reported in the primary literature. Reports of whole-mushroom poisoning or clinical cases without attribution to a specific identified compound were not considered compound-specific toxicological records. Speculative interpretations, secondary reports without traceable primary evidence, and computationally predicted toxicity results were not included as experimental observations.

Following screening, qualifying compound-level records were obtained for 235 of the 643 candidate species. The remaining 408 species did not yield records meeting the inclusion criteria within the defined search scope.



## 4. Initial Data Compilation

Relevant publications were read manually, and information was extracted into three CSV tables designed according to the research objectives. These tables formed the basis of the initial PMMdb dataset.

•	Compounds.csv: Contained chemical information for individual compounds, including common names, chemical taxonomy, PubChem CID, ChEBI ID, CAS number, synonyms, molecular formula, SMILES, InChI, InChIKey, and physicochemical properties.

•	Mushrooms.csv: Contained information on mushroom species, including fungal names, synonyms or previously used names, taxonomic classifications, NCBI Taxonomy IDs, and associated compound names.

•	ToxicityData.csv: Contained compound-associated toxicological information linked to the corresponding literature references. Toxicity records were organized into three major categories: general toxicity, organ toxicity, and cytotoxicity. Organ toxicity was further divided into hepatotoxicity, nephrotoxicity, gastrointestinal toxicity, neurotoxicity, and other toxicities. For quantitative endpoints, such as IC50, EC50, and LD50, the recorded information included the endpoint type, numerical value, unit, administration route, experimental model, and source reference. Descriptive information, including organ injury manifestations, toxicity characteristics, and mechanisms of action, was recorded as text linked to the original literature.

The extracted information was entered manually into the corresponding tables, with the original publications serving as the primary sources of evidence. The initial Figshare release (v1) contained these three CSV files.



## 5. Data Restructuring, Annotation, and Standardization

During preparation of the revised dataset, the original three-table structure was substantially reorganized. The existing records were reviewed, field definitions were refined, and chemical, taxonomic, toxicological, and literature information was standardized. The data were then organized into eight interconnected TSV tables.

### 5.1. Relational Data Organization

The revised dataset comprises three master and reference tables and five evidence and annotation tables.

The three master and reference tables are:

•	Compounds.tsv: Contains standardized chemical records. Each compound is assigned a unique compound_id.

•	Taxa.tsv: Contains standardized taxonomic records. Each taxon is assigned a unique taxon_id.

•	References.tsv: Contains information on individual literature and other information sources. Each source is assigned a unique reference_id, with its source type, identifier, and corresponding URL recorded where available.

The five evidence and annotation tables are:

•	Compound_Species_Evidence.tsv: Records literature-supported compound–taxon associations, linking compound_id, taxon_id, and the supporting reference_id.

•	Toxicity.tsv: Contains individual experimental toxicological observations linked to the corresponding compounds and supporting literature.

•	Toxicity_Mechanism.tsv: Contains literature-derived descriptions of toxicological mechanisms associated with the corresponding compounds.

•	Bioactivity_Target.tsv: Contains non-toxicological biological activity and molecular-target information, together with supporting references.

•	ADMET_Predictions.tsv: Contains calculated physicochemical descriptors and ADMET predictions linked to the corresponding compounds.

Each record was assigned an appropriate unique identifier, serving as a primary key (PK) in its respective table. Foreign-key (FK) fields were introduced to connect related records across tables. Compound–taxon associations were separated from the compound and taxon records and maintained in Compound_Species_Evidence.tsv. This allows a compound to be associated with multiple taxa, and a taxon to be associated with multiple compounds, without duplicating the corresponding entity records.

Experimental toxicological observations, mechanistic descriptions, and non-toxicological biological activities were also placed in separate tables. Results from different publications, experimental systems, exposure conditions, or endpoints were retained as individual records rather than combined into summary values.

To make source information directly accessible, human-readable references fields were added to six tables: Compounds.tsv, Taxa.tsv, Compound_Species_Evidence.tsv, Toxicity.tsv, Toxicity_Mechanism.tsv, and Bioactivity_Target.tsv. In Compounds.tsv, these fields contain source identifiers derived from the corresponding compound–taxon evidence records. In the evidence-level tables, they provide readable representations of the associated references. The underlying reference_id fields remain the relational links to References.tsv. ADMET_Predictions.tsv does not contain a record-level literature reference field because all predictions were generated using the same computational platform.

### 5.2. Chemical Annotation and Structure Standardization

Chemical information was checked against the structures reported in the primary literature and available chemical resources, including SciFinder, PubChem, and ChEBI. Compound names, synonyms, molecular formulae, CAS numbers, PubChem CIDs, ChEBI IDs, SMILES, InChI, and InChIKey were recorded and cross-checked where reliable matches could be established. When an external identifier could not be reliably assigned, the corresponding field was left unassigned rather than inferred.

Stereochemical information was retained only when supported by the original literature or the cited reference reporting the compound structure. When stereochemistry was not reported or could not be uniquely established, non-stereospecific structural representations were used rather than assigning configurations speculatively.

For compounds that could not be matched to standardized records in the consulted chemical resources, two-dimensional structures were reconstructed in KingDraw (Education Edition, version 4.0), based on the structures reported in the primary literature. Open Babel (version 3.1.1) was then used to generate the corresponding SMILES, InChI, and InChIKey representations. The generated representations were checked against the reconstructed structures and the original literature before inclusion. The curated structures were also exported in Structure Data File (SDF) format.

### 5.3. Taxonomic Annotation

Taxonomic information was standardized primarily against NCBI Taxonomy. Scientific names reported in the literature were checked against accepted taxonomic names where possible, and corresponding NCBI Taxonomy identifiers and higher-level classifications were recorded when available. Literature-reported synonyms and previously used names were retained as taxonomic synonyms associated with the standardized taxa. Taxa for which an NCBI Taxonomy identifier could not be established were retained without an assigned identifier.

### 5.4. Toxicological and Biological Activity Annotation

Experimental toxicological information was standardized at the level of individual literature-derived observations. Each record was assigned a toxicity type and a result type. Where reported, information was organized into fields covering the toxicity endpoint, comparator, numerical value or range, variability, unit, exposure duration, exposure value and unit, administration route, assay method, biological test system, qualitative effect description, original reported result, and supporting literature source.

Information not reported in the source literature was not inferred or supplemented speculatively. Mechanistic descriptions were separated from observed toxicological outcomes and stored in Toxicity_Mechanism.tsv. Non-toxicological biological activity and molecular-target information were stored separately in Bioactivity_Target.tsv to distinguish these records from experimental toxicological observations.

### 5.5. Literature Provenance

A centralized reference table was established to manage the sources associated with individual records. Each unique literature or information source was assigned a reference_id. Available identifiers, including DOI, PMID, URL, TKOI (Traditional Knowledge Object Identifier), and other persistent identifiers, were retained where applicable.

Compound–taxon associations, toxicological observations, toxicity mechanisms, and biological activity records were linked to their supporting sources through these reference identifiers. This allows individual records to be traced to the corresponding literature without repeatedly storing full reference information in different tables.

### 5.6. Computational Annotation

Physicochemical descriptors and ADMET-related predictions were generated from compound SMILES using ADMETlab 3.0. The main batch calculations for the curated compound set were performed in April 2026. The outputs included calculated physicochemical descriptors, continuous regression predictions, and classification probabilities covering absorption, distribution, metabolism, excretion, and toxicity-related endpoints.

One prediction record was retained for each compound in ADMET_Predictions.tsv. These computational results were stored separately from experimentally reported toxicological observations.

## 6. Technical Validation

The revised dataset was checked using an automated validation workflow implemented in Python 3.12.6 with RDKit 2025.9.1. The checks covered table schema conformity, primary-key uniqueness, identifier formats, foreign-key relationships, chemical structure consistency, taxonomic annotations, toxicological data completeness, and ADMET predictions.

Chemical checks included parsing SMILES and InChI representations, comparing chemical identifiers, and checking molecular formulae and molecular weights against calculated values. Taxonomic and relational checks covered NCBI Taxonomy identifiers, taxonomic classifications, and relationships between tables. Toxicological checks examined reference linkage, numerical values or ranges, and associated units. ADMET checks covered prediction completeness and numerical validity.

A random manual audit of 60 records was also performed, comprising 20 compound records, 20 compound–taxon association records, and 20 toxicity records. These records were checked against their supporting primary sources for chemical identity, compound–taxon correspondence, toxicological results, experimental context, and reference assignment, as applicable. All 60 audited records were concordant with the corresponding source information.

The results of the automated checks were recorded in a validation summary provided with the dataset.

## 7. Data Packaging and Release

The current PMMdb data package comprises eight TSV tables, an SDF file containing standardized structures linked to compound identifiers, a Data Dictionary in both CSV and TSV formats, and a validation summary.

The Data Dictionary describes the fields, data types, definitions, units or scales, identifier relationships, source provenance, and missing-value conventions used in the eight tables. The validation summary records the checks performed on the released files.

The versioned dataset and its accompanying documentation are deposited in Figshare. The data curation workflow and the code used for technical validation are also made available through the PMMdb GitHub repository.

---

## Workflow summary

Manual literature retrieval and screening → Manual information extraction and compilation into three initial CSV tables → Data restructuring and standardization during preparation of the revised dataset, including chemical, taxonomic, and toxicological annotation and the establishment of relational links → Organization into eight interconnected TSV tables → Technical validation → Data packaging and public release.

