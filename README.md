# SafePath Portfolio Edition

[中文](#中文说明) | [English](#english)

## English

SafePath is a portfolio case study for a **mobile-first service-access navigator**. It demonstrates how I turned a fragmented, time-sensitive service-discovery problem into a small product system with explicit data-quality and privacy boundaries.

This public repository is intentionally a **sanitized, non-production code sample**. It contains no production records, personal data, real provider details, user submissions, screenshots, commercial links, credentials, or operational configuration. Every record in `data/demo_records.json` is fictional.

### What I built

- A normalized record model for service channels and price observations.
- Filterable catalog logic for city, service type, channel type, and free-text search.
- Median/min/max aggregation that excludes records awaiting review.
- A data-quality gate that makes the public-release rule executable.
- A mobile web and native mini-program information architecture in the original private project.

### Product decisions illustrated here

| Problem | Design response |
|---|---|
| Information changes quickly | Attach status and verification metadata to each record. |
| Urgent and planned journeys differ | Model service type separately from channel type. |
| Small price samples can mislead | Report sample counts and exclude unverified observations from summaries. |
| A public portfolio must be safe to share | Publish only synthetic records and validate the repository before release. |

### Run locally

Requires Python 3.11+ and only the standard library.

```bash
python -m unittest discover -s tests -v
python scripts/validate_public_repo.py
python -m app.catalog
```

### Repository map

```text
app/catalog.py                 Core filtering and aggregation logic
data/demo_records.json         Synthetic demonstration data only
docs/ARCHITECTURE.md           Product/data-flow design
docs/PUBLIC_RELEASE_CHECKLIST.md  Release and privacy guardrails
scripts/validate_public_repo.py   Public-repository safety check
tests/test_catalog.py          Executable behavior examples
```

### Scope note

This is a product-engineering case study, not medical advice and not a live service directory. It deliberately omits production integrations, real-world records, pricing, and operational workflows.

## 中文说明

SafePath 是一个“服务可及性导航”产品案例：面向信息分散、时效性高的服务查询场景，展示我如何把用户路径、数据质量和隐私边界一起落到产品与代码中。

这个仓库是可公开展示的脱敏版本，**不是线上服务**。其中不包含真实机构/地址/联系方式、用户提交内容、截图、平台链接、商业采样、凭据或运维配置；`data/demo_records.json` 中的记录均为虚构示例。

可重点查看：

- `app/catalog.py`：筛选、查询与价格样本汇总的核心逻辑；
- `docs/ARCHITECTURE.md`：产品和数据流设计；
- `scripts/validate_public_repo.py`：将脱敏规则变成可执行发布检查；
- `tests/test_catalog.py`：关键行为的自动化验证。

原创项目的完整实现和真实运营材料仅在私有环境中保存。

以下是小程序码
<img width="430" height="430" alt="a97061ae6de67eb53cb0e1cd4668b236" src="https://github.com/user-attachments/assets/511f8c7e-85f9-44b1-971e-c9a492e02ec1" />
