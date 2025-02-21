import os

def create_structure(base_path, structure):
    """
    Recursively creates directories and files based on the provided structure dictionary.
    Directories are represented as dicts.
    Files are represented as key-value pairs (filename: file content).
    If a directory is empty, a .gitkeep file is added.
    """
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # Create directory
            os.makedirs(path, exist_ok=True)
            # If directory is empty, add a .gitkeep file to track it
            if not content:
                gitkeep_path = os.path.join(path, ".gitkeep")
                with open(gitkeep_path, "w") as f:
                    f.write("")
            else:
                # Recursively create subdirectories/files
                create_structure(path, content)
        else:
            # Create file with the provided content
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

def main():
    repo_structure = {
        "README.md": """# Besper Resources Repository

## Repository Purpose
Centralized digital asset management for Besper's operational documentation, marketing collateral, and product resources. Provides version-controlled access through GitHub's infrastructure with Power Pages integration.

## File Structure Guide

### Licensing Documentation
- **EULAs**: End-user license agreements (v1.2+ requires legal review)
- **Compliance**: Regional regulatory documentation (GDPR/CCPA updated Q2 2025)

### Press Resources
- **Media Kits**: High-resolution assets and brand guidelines
- **Press Releases**: Embargoed until publication dates in metadata

### Product Portfolio
- **Technical Specs**: Machine-readable JSON specifications with human-friendly markdown
- **Pricing Models**: Structured YAML files with regional pricing matrices

## Access Protocol
{% raw %}
{% bsp_file_download
file_path: "Portfolio/Product-Guides/Installation/BesperPro-Install-v2.1.pdf",
display_name: "Professional Installation Guide"
%}
{% endraw %}

[Full Developer Documentation](https://dev.azure.com/Besper/Besper%20-%20General/_wiki/wikis/Besper---General.wiki/59/File-Downloads)
""",
        "LICENSE.md": """MIT License

Copyright (c) [Year] Besper

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction...
""",
        ".github": {
            "workflows": {
                "release-checklist.yml": """# GitHub release checklist workflow
name: Release Checklist
on:
  push:
    tags:
      - 'v*'
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Run tests
        run: echo "Running tests..."
"""
            }
        },
        "Press": {
            "Media-Kits": {
                "Corporate": {},
                "Product": {}
            },
            "Press-Releases": {},
            "Brand-Assets": {
                "Logos": {},
                "Fonts": {},
                "Color-Palettes": {}
            }
        },
        "Licensing": {
            "EULAs": {},
            "Partner-Agreements": {},
            "Compliance": {
                "GDPR": {},
                "CCPA": {}
            }
        },
        "Portfolio": {
            "Product-Guides": {
                "Installation": {},
                "Troubleshooting": {}
            },
            "Technical-Specs": {},
            "Pricing-Models": {},
            "Feature-Catalogs": {}
        },
        "_powerpages": {
            "js": {
                "besper-downloads.js": """// besper-downloads.js
window.BesperDownloads = (function() {
  const GITHUB_PAT = '{% raw %}{{ settings.github_pat | escape }}{% endraw %}';

  async function downloadFile(config) {
    try {
      const response = await fetch(
        `https://api.github.com/repos/${config.repo}/contents/${encodeURIComponent(config.path)}`,
        {
          headers: {
            'Authorization': `token ${GITHUB_PAT}`,
            'Accept': 'application/vnd.github.v3.raw'
          }
        }
      );
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const anchor = document.createElement('a');
      
      anchor.href = url;
      anchor.download = config.name;
      document.body.appendChild(anchor);
      anchor.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(anchor);
    } catch (error) {
      console.error('Download failed:', error);
      throw new Error(`DOWNLOAD_FAILURE: ${error.message}`);
    }
  }

  return { downloadFile };
})();
"""
            }
        }
    }
    
    # Create the repository structure starting from the current directory
    create_structure(".", repo_structure)
    print("Repository structure created successfully.")

if __name__ == "__main__":
    main()
