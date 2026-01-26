# External Projects

This directory contains external dbt projects and references that can be used as examples or for learning purposes.

## Contents

### dbt-project_data-engineering

**Source**: https://github.com/varmara/dbt-project_data-engineering.git

**Description**: Week 4 Analytics Engineering homework project from Data Engineering Zoomcamp 2024. This is a dbt project focused on NYC taxi trip data analytics.

**Structure**:
- `models/staging/` - Staging models for yellow, green, and FHV trip data
- `models/core/` - Core fact and dimension tables
- `macros/` - Reusable SQL macros
- `seeds/` - Static data files (taxi zone lookup)

**Use Case**: Reference implementation for dbt best practices and analytics engineering patterns.

## How to Use

These external projects serve as reference materials and examples. Each project maintains its own structure and can be used independently:

1. Navigate to the project directory
2. Follow the project-specific README for setup instructions
3. Configure your own database connections as needed

## Adding New External Projects

To add new external projects to this directory:

```bash
cd external_projects
git clone <repository-url>
```

Then update this README with information about the new project.
