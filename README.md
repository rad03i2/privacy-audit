# Privacy Audit

A dependency-free, local-first Python tool that scans text files and source trees for privacy-sensitive material **without uploading or modifying your data**.

[العربية](#العربية) · [Installation](#installation) · [Usage](#usage) · [Security](#security--privacy)

## Overview

Privacy Audit helps developers catch accidental exposure before sharing a folder, publishing a repository, or attaching files. It performs conservative, explainable pattern checks and reports the file, line, severity, rule, and a redacted excerpt.

### Why it exists

Simple pre-publication checks should not require sending potentially sensitive files to a third party. Privacy Audit runs locally, is read-only, follows no symbolic links, and has no runtime dependencies or telemetry.

## Key features

- Recursively scans UTF-8/UTF-8-BOM text files or one file.
- Detects possible email addresses, IPv4 addresses, private-key headers, AWS-style access-key IDs, GitHub-style tokens, and generic embedded credentials.
- `low`, `medium`, and `high` severities with explainable rule names.
- Redacts excerpts so a full detected credential is not echoed to output.
- Skips binary, undecodable, oversized, generated/dependency directories, and symbolic links.
- Human-readable and JSON output.
- CI-friendly `--fail-on low|medium|high` threshold.
- Python API plus `privacy-audit` and `python -m privacy_audit` entry points.
- No network calls, API keys, accounts, telemetry, or runtime packages.

## Preview

```text
$ privacy-audit ./project
Scanned: 18 | Skipped: 2 | Findings: 1
[LOW   ] project/config.txt:4 email — Possible email address — owne…com
```

The example is illustrative. Exact paths and counts depend on the scanned content.

## Requirements

- Python 3.10+
- Windows, macOS, or Linux

## Installation

From a clone:

```bash
git clone https://github.com/rad03i2/privacy-audit.git
cd privacy-audit
python -m pip install .
```

For development:

```bash
python -m pip install -e .
```

## Usage

Scan a directory:

```bash
privacy-audit ./project
```

Scan one file and emit JSON:

```bash
privacy-audit notes.txt --json
```

Fail CI when medium-or-higher findings exist:

```bash
privacy-audit . --fail-on medium
```

Limit inspected file size (bytes):

```bash
privacy-audit . --max-bytes 500000
```

Exit codes: `0` means the scan completed and the configured threshold was not reached; `1` means invalid input/read failure; `2` means `--fail-on` was reached.

### Python API

```python
from privacy_audit import scan_path, scan_text

findings, summary = scan_path("./project")
for finding in findings:
    print(finding.rule, finding.severity, finding.path, finding.line)

inline = scan_text("Contact: person@example.com")
```

## Configuration

No environment variables or configuration file are required. Behavior is controlled by CLI flags. The default per-file limit is 2,000,000 bytes. Common dependency/build directories such as `.git`, `.venv`, `node_modules`, `dist`, and `build` are skipped.

## Project structure

```text
privacy-audit/
├── src/privacy_audit/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   └── scanner.py
├── tests/test_scanner.py
├── .github/workflows/ci.yml
├── pyproject.toml
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

## Testing

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
```

GitHub Actions runs the package on Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.

## Security & privacy

The scanner reads local files only. It does not modify them, access the network, follow symbolic links, or intentionally persist scanned content. Output itself may still reveal that sensitive material exists, so treat reports as sensitive. See [SECURITY.md](SECURITY.md).

## Limitations

Privacy Audit is a heuristic pre-publication aid, **not** a DLP platform, secret manager, malware scanner, or compliance certification tool. Pattern matching can produce false positives and false negatives. It does not inspect binary formats, archives, images, PDFs, office documents, git history, or remote services. A clean report is not proof that content contains no personal or secret information.

## Optional roadmap

Possible future work includes opt-in custom rules, ignore files, SARIF export, and additional structured-text detectors. These are not required for the current scanner to work end-to-end.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Never use real credentials or personal information in tests or issues.

## License

MIT License — see [LICENSE](LICENSE).

## Author

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

# العربية

## نظرة عامة

**Privacy Audit** أداة Python محلية وخفيفة لفحص الملفات النصية ومجلدات الشيفرة بحثًا عن مؤشرات قد تكشف معلومات حساسة قبل مشاركة الملفات أو نشر المستودع. تعمل الأداة على جهازك فقط، ولا ترفع البيانات ولا تعدّل الملفات.

### لماذا هذا المشروع؟

قد يحتوي مشروع جاهز للنشر دون قصد على بريد إلكتروني أو عنوان IP أو مفتاح خاص أو رمز وصول. الهدف هو توفير فحص أولي واضح وقابل للتفسير من دون إرسال الملفات الحساسة إلى خدمة خارجية.

## الميزات الرئيسية

- فحص ملف واحد أو مجلد كامل بصورة تكرارية.
- دعم UTF-8 وUTF-8 BOM، بما في ذلك النص العربي.
- كشف مؤشرات البريد الإلكتروني وIPv4 ورؤوس المفاتيح الخاصة ومعرّفات مفاتيح AWS وأنماط رموز GitHub والبيانات السرية العامة.
- مستويات خطورة `low` و`medium` و`high`.
- إظهار الملف ورقم السطر والقاعدة مع مقتطف مخفي جزئيًا بدل طباعة السر كاملًا.
- تجاهل الملفات الثنائية وغير القابلة لفك UTF-8 والملفات الكبيرة والروابط الرمزية ومجلدات الاعتماد والبناء الشائعة.
- إخراج نصي أو JSON وخيار `--fail-on` المناسب للتكامل المستمر.
- واجهة Python برمجية وCLI.
- لا اتصالات شبكة ولا مفاتيح API ولا تتبع ولا حزم تشغيل خارجية.

## المعاينة

```text
privacy-audit ./project
Scanned: 18 | Skipped: 2 | Findings: 1
```

الأرقام أعلاه توضيحية فقط؛ النتيجة الفعلية تعتمد على الملفات التي تفحصها.

## المتطلبات والتثبيت

تحتاج Python 3.10 أو أحدث على Windows أو macOS أو Linux:

```bash
git clone https://github.com/rad03i2/privacy-audit.git
cd privacy-audit
python -m pip install .
```

وللتطوير:

```bash
python -m pip install -e .
```

## الاستخدام

```bash
privacy-audit ./project
privacy-audit notes.txt --json
privacy-audit . --fail-on medium
privacy-audit . --max-bytes 500000
```

يمكن أيضًا التشغيل هكذا:

```bash
python -m privacy_audit ./project
```

رمز الخروج `0` يعني اكتمال الفحص دون بلوغ حد الفشل المحدد، و`1` لخطأ الإدخال/القراءة، و`2` عند بلوغ مستوى `--fail-on`.

### واجهة Python

```python
from privacy_audit import scan_path

findings, summary = scan_path("./project")
print(summary)
```

## الإعداد

لا يحتاج المشروع ملف `.env` أو متغيرات بيئة. الحد الافتراضي لحجم الملف المفحوص هو 2,000,000 بايت، ويمكن تغييره من CLI. يتم تجاهل مجلدات شائعة مثل `.git` و`.venv` و`node_modules` و`dist` و`build`.

## بنية المشروع

الشيفرة الفعلية داخل `src/privacy_audit/`، والاختبارات داخل `tests/`، وإعداد CI داخل `.github/workflows/ci.yml`، وبيانات الحزمة في `pyproject.toml`.

## الاختبارات

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
```

إعداد GitHub Actions يشغّل الاختبارات على Ubuntu وWindows وmacOS مع عدة إصدارات من Python.

## الأمان والخصوصية

الأداة للقراءة فقط: لا تعدّل الملفات، ولا تتصل بالإنترنت، ولا تتبع الروابط الرمزية، ولا تحفظ محتوى الملفات عمدًا. مع ذلك قد يكشف تقرير النتائج وجود بيانات حساسة، لذلك يجب التعامل معه بحذر. راجع [SECURITY.md](SECURITY.md).

## القيود

هذه الأداة فحص استدلالي أولي وليست نظام DLP أو مدير أسرار أو ماسح برمجيات خبيثة أو إثبات امتثال. قد تظهر نتائج إيجابية أو سلبية خاطئة. لا تفحص حاليًا الملفات الثنائية أو الأرشيفات أو الصور أو PDF أو مستندات Office أو تاريخ Git. النتيجة النظيفة لا تضمن خلو المحتوى من كل البيانات الحساسة.

## تطوير اختياري مستقبلًا

يمكن مستقبلًا إضافة قواعد مخصصة اختيارية، وملف تجاهل، وتصدير SARIF، وكواشف إضافية للنصوص المنظمة. الوظائف الحالية لا تعتمد على هذه الإضافات.

## المساهمة

راجع [CONTRIBUTING.md](CONTRIBUTING.md)، ولا تستخدم بيانات شخصية أو أسرارًا حقيقية في الاختبارات أو البلاغات.

## الترخيص

المشروع مرخص بترخيص MIT. راجع [LICENSE](LICENSE).

## المؤلف

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
