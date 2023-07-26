# semv - Semantic Version Printing

Intended use case:
  $ git tag $(semv)

## Design principles

- Python Standard Library only
- No write access to repository
- Core functionality: parsing and validating commit messages
- Feature 1: Version Printing
- Feature 2: At some point change log formatting (maybe)
- Hooks for validation
- Minimal configuration (only validation hooks?)
- No support beyond Major.Minor.Patch
- Use for semv for developing semv
