# PMMdb - Mushroom Toxin Database (MushroomToxinDB)

## Overview

PMMdb is a mushroom secondary metabolites database system that provides information query, search, and browsing capabilities for mushrooms and their related compounds. The system adopts a front-end and back-end separated architecture, supporting compound structure search, similarity matching, and detailed toxicological data queries.

**🌐 Online Access**: [https://www.cellknowledge.com.cn/pmmdb/](https://www.cellknowledge.com.cn/pmmdb/)

## Technology Stack

### Backend
- **Framework**: Spring Boot 2.5.6
- **Persistence Layer**: MyBatis-Plus 3.4.3.4
- **Database**: MySQL 5.6
- **Cheminformatics**: CDK (Chemistry Development Kit) 2.7.1 - For molecular structure processing and similarity calculation
- **Others**: Lombok, Jackson

### Frontend
- **Framework**: Vue 3.4
- **Build Tool**: Vite 5.0
- **UI Component Library**: Element Plus 2.4
- **Routing**: Vue Router 4.2
- **HTTP Client**: Axios 1.6
- **Charts**: ECharts 6.0, Plotly.js 3.3
- **Styling**: TailwindCSS 3.4

## Project Structure

```
PMMdb/
├── backend/                    # Backend project
│   ├── src/main/java/com/yy/mushroomtoxindb/
│   │   ├── config/            # Configuration classes (MyBatis config, etc.)
│   │   ├── controller/        # REST API controllers
│   │   ├── dto/               # Data Transfer Objects
│   │   ├── entity/            # Entity classes
│   │   ├── mapper/            # MyBatis Mapper interfaces
│   │   └── service/           # Business logic layer
│   ├── src/main/resources/
│   │   └── application.properties  # Application configuration file
│   └── pom.xml                # Maven configuration file
│
└── frontend/                  # Frontend project
    ├── public/ketcher/        # Ketcher molecular editor static resources
    ├── src/
    │   ├── api/               # API interface encapsulation
    │   ├── assets/            # Static resources
    │   ├── components/        # Vue components
    │   ├── router/            # Route configuration
    │   ├── styles/            # Style files
    │   └── views/             # Page views
    ├── package.json           # npm dependency configuration
    └── vite.config.js         # Vite build configuration
```

## Key Features

### 1. Data Browsing
- **Compound Browsing**: Paginated display of all compounds with sorting by toxicity count or name
- **Fungus Browsing**: Paginated display of fungus information including taxonomic details

### 2. Search Functionality
- **Compound Name Search**: Fuzzy matching for compound common names and other names
- **CAS Number Search**: Exact matching for compound CAS numbers
- **SMILES Similarity Search**: Molecular structure-based similarity search (threshold > 0.70)
- **Fungus Name Search**: Fuzzy matching for fungus names
- **Fungus Taxonomy Search**: Search by Family or Genus

### 3. Detail Views
- **Compound Details**: Display basic compound information, molecular formula, SMILES, InChI, and related toxicity data and molecular activities
- **Fungus Details**: Display taxonomic information, references, and associated compound lists

### 4. Statistics
- Total number of compounds
- Total number of fungi
- Total toxicity records
- Total molecular activity records

### 5. Data Submission
- Support for users to submit new mushroom or compound data

### 6. Molecular Structure Editing
- Integrated Ketcher molecular editor for drawing and editing chemical structures

## API Endpoints

### Compound APIs
- `GET /api/compounds` - Get compound list (paginated)
- `GET /api/compound/{id}` - Get compound details
- `GET /api/search/compound/name?name={name}` - Search compounds by name
- `GET /api/search/compound/cas?cas={cas}` - Search compounds by CAS number
- `GET /api/search/compound/smiles?querySmiles={smiles}` - SMILES similarity search

### Fungus APIs
- `GET /api/fungi` - Get fungus list (paginated)
- `GET /api/fungus/{id}` - Get fungus details
- `GET /api/search/fungus/name?name={name}` - Search fungi by name
- `GET /api/search/fungus/family?family={family}` - Search fungi by family
- `GET /api/search/fungus/genus?genus={genus}` - Search fungi by genus

### Other APIs
- `POST /api/submit` - Submit new data
- `GET /api/statistics` - Get database statistics

## Data Models

### Main Entities

#### Compound
- compoundId: Compound ID
- commonName: Common name
- otherName: Other names
- molecularFormula: Molecular formula
- smiles: SMILES string
- inchi: InChI string
- inchikey: InChIKey
- cas: CAS number
- pubchemCid: PubChem ID
- chebiId: ChEBI ID
- chemicalTaxonomy: Chemical taxonomy
- fileSource: Data source

#### FungusInfo
- fungusId: Fungus ID
- fungusName: Fungus name
- ncbiTaxonomyId: NCBI taxonomy ID
- phylum: Phylum
- class: Class
- order: Order
- family: Family
- genus: Genus
- reference: Reference

#### Toxicity
- Toxicity information linking compounds and fungi

#### MolecularActivity
- Molecular activity data for compounds

#### AdmetPrediction
- ADMET (Absorption, Distribution, Metabolism, Excretion, and Toxicity) predictions for compounds

## Development Notes

### Backend Development
- Uses MyBatis-Plus for database operations
- Follows RESTful API design principles
- Automatic result mapping and underscore-to-camelCase conversion enabled
- SQL logging enabled in development environment, recommended to disable in production

### Frontend Development
- Uses Vue 3 Composition API
- Route base path set to `/pmmdb/`
- Element Plus UI component library
- TailwindCSS for styling

## License

This project is for educational and research purposes only.

## Contact

For questions or suggestions, please contact the project maintainers.
