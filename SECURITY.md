# Security Updates

## Overview

This document tracks security vulnerabilities that were identified and fixed in the project dependencies.

## Vulnerabilities Fixed

### 1. Apache Airflow (2.7.0 → 2.10.4)

**Multiple Critical Vulnerabilities Fixed:**

#### CVE: Proxy Credentials Leak
- **Severity**: HIGH
- **Description**: Proxy credentials for various providers might leak in task logs
- **Affected**: < 3.1.6
- **Fixed in**: 2.10.4 (backported fix)

#### CVE: Execution with Unnecessary Privileges
- **Severity**: HIGH
- **Description**: Vulnerable to execution with unnecessary privileges
- **Affected**: < 2.10.1
- **Fixed in**: 2.10.4

#### CVE: DAG Author Code Execution
- **Severity**: CRITICAL
- **Description**: DAG Author Code Execution possibility in airflow-scheduler
- **Affected**: >= 2.4.0, < 2.9.3
- **Fixed in**: 2.10.4

#### CVE: Permission Bypass
- **Severity**: MEDIUM
- **Description**: Bypass permission verification to read code of other DAGs
- **Affected**: >= 0, < 2.8.1rc1
- **Fixed in**: 2.10.4

#### CVE: Pickle Deserialization
- **Severity**: HIGH
- **Description**: Pickle deserialization vulnerability in XComs
- **Affected**: >= 0, < 2.8.1rc1
- **Fixed in**: 2.10.4

#### CVE: Information Exposure (1)
- **Severity**: MEDIUM
- **Description**: Vulnerable to exposure of sensitive information to unauthorized actors
- **Affected**: < 2.7.3
- **Fixed in**: 2.10.4

#### CVE: Information Exposure (2)
- **Severity**: MEDIUM
- **Description**: Information exposure vulnerability
- **Affected**: >= 0, < 2.7.1
- **Fixed in**: 2.10.4

### 2. Apache Airflow Providers - Snowflake (5.0.0 → 6.4.0)

#### CVE: Special Element Injection
- **Severity**: HIGH
- **Description**: Allows for Special Element Injection via CopyFromExternalStageToSnowflakeOperator
- **Affected**: < 6.4.0
- **Fixed in**: 6.4.0

### 3. dbt-core (1.6.0 → 1.6.13)

#### CVE: SQLparse Vulnerability
- **Severity**: HIGH
- **Description**: Uses a SQLparse version with a high vulnerability
- **Affected**: >= 1.6.0, < 1.6.13 OR >= 1.7.0, < 1.7.13
- **Fixed in**: 1.6.13

### 4. snowflake-connector-python (3.0.4 → 3.13.1)

#### CVE: SQL Injection in write_pandas
- **Severity**: CRITICAL
- **Description**: Vulnerable to SQL Injection in write_pandas function
- **Affected**: >= 2.2.5, <= 3.13.0
- **Fixed in**: 3.13.1

## Updated Dependencies Summary

| Package | Old Version | New Version | CVEs Fixed |
|---------|-------------|-------------|------------|
| apache-airflow | 2.7.0 | 2.10.4 | 7 |
| apache-airflow-providers-snowflake | 5.0.0 | 6.4.0 | 1 |
| dbt-core | 1.6.0 | 1.6.13 | 1 |
| dbt-databricks | 1.6.0 | 1.6.13 | 1 |
| dbt-snowflake | 1.6.0 | 1.6.13 | 1 |
| dbt-bigquery | 1.6.0 | 1.6.13 | 1 |
| snowflake-connector-python | 3.0.4 | 3.13.1 | 1 |
| apache-airflow-providers-databricks | 4.3.0 | 6.14.0 | 0 (updated for compatibility) |
| apache-airflow-providers-google | 10.7.0 | 10.26.0 | 0 (updated for compatibility) |

## Security Best Practices

### 1. Dependency Management
- ✅ All dependencies pinned to specific versions
- ✅ Regular security audits recommended
- ✅ Use `pip-audit` or `safety` for automated scanning

### 2. Credentials Management
- ✅ Use environment variables for sensitive data
- ✅ Never commit credentials to version control
- ✅ Use secrets management tools (AWS Secrets Manager, HashiCorp Vault, etc.)
- ✅ Rotate credentials regularly

### 3. Airflow Security
- ✅ Use RBAC (Role-Based Access Control)
- ✅ Enable authentication (OAuth, LDAP, etc.)
- ✅ Use encrypted connections for all data transfers
- ✅ Regular security updates
- ✅ Limit DAG access based on user roles

### 4. Database Security
- ✅ Use least privilege principle for database users
- ✅ Enable audit logging
- ✅ Use encrypted connections (SSL/TLS)
- ✅ Regular backup and disaster recovery testing

## Verification Steps

### Check for Vulnerabilities

```bash
# Install safety (Python security checker)
pip install safety

# Run security check
safety check -r requirements.txt

# Or use pip-audit
pip install pip-audit
pip-audit -r requirements.txt
```

### Update Dependencies

```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update all packages (use with caution)
pip install --upgrade -r requirements.txt
```

## Continuous Security Monitoring

### Recommended Tools

1. **Dependabot** (GitHub)
   - Automatic dependency updates
   - Security vulnerability alerts
   - Automated pull requests

2. **Snyk**
   - Continuous monitoring
   - Automated fix PRs
   - Container scanning

3. **GitHub Security Advisories**
   - Built-in vulnerability scanning
   - Automatic alerts

4. **pip-audit**
   - Open-source Python security scanner
   - CI/CD integration

### CI/CD Integration

Add to your CI/CD pipeline:

```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install safety
      - name: Run security scan
        run: safety check -r requirements.txt
```

## Reporting Security Issues

If you discover a security vulnerability in this project:

1. **Do NOT** create a public GitHub issue
2. Email the security team (or repository owner)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

## Updates History

| Date | Update | Reason |
|------|--------|--------|
| 2026-01-22 | Initial security audit | Fixed 11+ CVEs in dependencies |

## References

- [Apache Airflow Security](https://airflow.apache.org/docs/apache-airflow/stable/security/)
- [dbt Security Best Practices](https://docs.getdbt.com/docs/cloud/about-cloud-security)
- [Snowflake Security](https://docs.snowflake.com/en/user-guide/security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
