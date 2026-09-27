<p align="center">
  <a href="https://linkedin.com/in/wisrovi-rodriguez"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="https://wisrovi.dev"><img src="https://img.shields.io/badge/Author-wisrovi.dev-111827?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Portal" /></a>
  <a href="https://orcid.org/0009-0005-0710-1861"><img src="https://img.shields.io/badge/ORCID-0009--0005--0710--1861-A6CE39?style=for-the-badge&logo=orcid&logoColor=white" alt="ORCID" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License" /></a>
</p>

# wmariadb

**MariaDB ORM using Pydantic models - simple, type-safe database operations**

High-level Python ORM library providing a clean, type-safe interface for MariaDB database operations using Pydantic models for schema definition.

## Key Features

- **Pydantic Integration** - Define database schema using Pydantic v2 models
- **Auto Table Creation** - Tables created/synchronized automatically with model changes
- **CRUD Operations** - Simple insert, get, update, delete methods
- **Column Sync** - Automatically adds new columns when model changes
- **Constraints Support** - Primary Key, UNIQUE, NOT NULL, Foreign Keys
- **Type Safety** - Full type hints and Pydantic validation
- **Async Support** - Full async/await for high-performance applications
- **Query Builder** - Safe query construction with SQL injection prevention
- **CLI Tool** - Command-line interface for common operations
- **Code Quality** - Pylint compatible, comprehensive type hints

## Technical Stack

- **Python**: 3.9+
- **Key Libraries**: pydantic>=2.0.0, loguru>=0.7.0, click>=8.0.0, mariadb>=1.1.0, aiomysql>=0.2.0
- **Testing**: pytest, pytest-cov, pytest-asyncio
- **Code Quality**: ruff, black, mypy

## Installation & Setup

```bash
pip install wmariadb
```

Development installation:
```bash
pip install -e ".[dev]"
```

## Architecture & Workflow

```
wmariadb/
├── src/wmariadb/          # Main library package
│   ├── core/             # Core database operations
│   ├── builders/          # SQL query builder
│   ├── exceptions/       # Custom exceptions
│   ├── types/            # SQL type mapping
│   └── cli/              # CLI tool
├── examples/             # Usage examples (25+ folders)
├── test/                 # Test suite
│   ├── unit/            # Unit tests
│   └── integration/    # Integration tests
├── docs/                 # Sphinx documentation
│   ├── tutorials/
│   ├── api_reference/
│   └── getting_started/
├── stress_test/          # Performance testing
├── docker/               # Docker configurations
├── pyproject.toml        # Project config
└── README.md
```

**Workflow**: Define Pydantic model → Configure MariaDB connection → Initialize WMariaDB → Auto table creation → Perform CRUD operations

## Configuration

**Environment Variables**:
- `WMARIADB_HOST` - Database host
- `WMARIADB_PORT` - Database port (default: 3306)
- `WMARIADB_USER` - Database user
- `WMARIADB_PASSWORD` - Database password
- `WMARIADB_DBNAME` - Database name

**Configuration Files**:
- `pyproject.toml` - Project metadata and dependencies
- `setup.py` - Package configuration

## Usage

```python
from pydantic import BaseModel
from wmariadb import WMariaDB

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "password",
    "dbname": "mydb",
}

class User(BaseModel):
    id: int
    name: str
    email: str

db = WMariaDB(User, DB_CONFIG)
db.insert(User(id=1, name="John", email="john@example.com"))
users = db.get_all()
```

---

## 👤 Autor & Afiliación Oficial

* **William Steve Rodriguez Villamizar (Wisrovi)**
* **Cargo:** Principal AI Engineer & Applied AI Solutions Architect | Scientific Researcher
* 📧 **Email:** [wisrovi.rodriguez@gmail.com](mailto:wisrovi.rodriguez@gmail.com) / [wisrovi@wisrovi.dev](mailto:wisrovi@wisrovi.dev)
* 🌐 **Portal Oficial:** [wisrovi.dev](https://wisrovi.dev)
* 💼 **LinkedIn:** [wisrovi-rodriguez](https://www.linkedin.com/in/wisrovi-rodriguez/)
* 🆔 **ORCID:** [0009-0005-0710-1861](https://orcid.org/0009-0005-0710-1861)
* 📦 **PyPI:** [pypi.org/user/wisrovi/](https://pypi.org/user/wisrovi/)
* 🐙 **GitHub:** [@wisrovi](https://github.com/wisrovi)


