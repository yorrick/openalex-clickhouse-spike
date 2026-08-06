# OpenAlex ClickHouse validation — stage2-repeat-medium-18c18t-r3

Local engine verdict: pass

Capacity verdict: Uncertain

## Input and environment identity

```json
{
  "environment": {
    "binfmt_registrations": "",
    "container_architecture": "aarch64",
    "container_cpuinfo": "processor\t: 0\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 1\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 2\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 3\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 4\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 5\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 6\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 7\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 8\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 9\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 10\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 11\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 12\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 13\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 14\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 15\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 16\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0\n\nprocessor\t: 17\nBogoMIPS\t: 48.00\nFeatures\t: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat ilrcpc flagm sb paca pacg dcpodp flagm2 frint i8mm bf16 bti afp ebf16\nCPU implementer\t: 0x61\nCPU architecture: 8\nCPU variant\t: 0x0\nCPU part\t: 0x000\nCPU revision\t: 0",
    "docker_server_architecture": "aarch64",
    "host_architecture": "arm64",
    "image": "clickhouse/clickhouse-server:26.3.12.3",
    "image_architecture": "arm64",
    "image_id": "sha256:b76fe13844679c04c28354a4d12c4ec8b242b51d05abadb176c8adbe1187d5ad",
    "published_hosts": {
      "8123": "127.0.0.1",
      "9000": "127.0.0.1"
    },
    "raw_mount_read_only": true,
    "repo_digests": [
      "clickhouse/clickhouse-server@sha256:1f7cd090d5c4e2b8bfe0ea5d8ae6125937e1d932c6371b4d25fbd6088829dc9c"
    ],
    "resource_limits": {
      "docker_cpus": 18,
      "docker_memory_bytes": 58864549888,
      "memory_bytes": 53687091200,
      "nano_cpus": 17999998976
    }
  },
  "inputs": {
    "complete_authors_bytes": 52769910496,
    "maximum_raw_input_bytes": 98301763421,
    "run_identity": {
      "config_sha256": "f30f5dc8ff0d754e60a9bddb803e8d91d249e262ce077766939744e13853e818",
      "download_state_sha256": "c01aa4ecf6f9b005eb14120b6de797a3e70a2c727a5e15254b6f6a8ef11a939e",
      "execution": {
        "cpus": 18,
        "maximum_seconds": 18000,
        "query_threads": 18,
        "workers": 1
      },
      "identity_version": 2,
      "memory_gib": 50,
      "rendered_sql_sha256": {
        "00_schema.sql": "77697425f578a6efb2b93cd8e0bca0157c8cec639b79be23555c7a470b971574",
        "11_load_complete_authors.sql": "110cef1958ee06ece4cc7ab7dda267baeeaa1ddf545ab67802610dad4cb93305",
        "12_load_small_dimensions.sql": "bbd0d0aa0e37362e7d4d2f47fc90ea9a0f39763d47856a2893d18aedacdb8cb5",
        "30_reverse_projection.sql": "05cad555e939464011ec68f5a449ef6c7d929f52ea41655ec6d9ab30150ea411",
        "stage2_medium/05_raw_evidence.sql": "486472a3a3a3ec5a2b11d965c4933a6bce4c1bd35dbdb31fe2d694f1c8d40e5a",
        "stage2_medium/20_load_works.sql": "6e6b922df37d24d735791e6c8be8895a560496264b9a6f95e72c9abf4c441069"
      },
      "run_id": "stage2-repeat-medium-18c18t-r3",
      "selection_sha256": "ccc7b5c51f04bd5972e6fb513f15157c13a79300be5fc5c36696aebbf56026b1",
      "sha256": "5b2e97c3aa944d1dd6929e4c0b926a83665e77f640dc84f39de75809e2976d6d",
      "tiers": [
        "stage2_medium"
      ]
    },
    "seed_work_ids": [
      25441,
      1491165,
      4388957908
    ],
    "selection_algorithm": "cumulative-bytes-four-strata-v2",
    "selection_sha256": "ccc7b5c51f04bd5972e6fb513f15157c13a79300be5fc5c36696aebbf56026b1",
    "tiers": {
      "stage2_medium": {
        "content_length": 15118229383,
        "record_count": 10109733
      }
    }
  }
}
```

## Correctness

```json
{
  "stage2_medium": {
    "distribution_digests": {
      "authorships_per_work": {
        "item_count": 447,
        "sha256": "2bc843d8da3f9998d26c7d558b7c8464e08af5a43f8e0128f60d3aa4c3f77d9e",
        "value_kind": "rows"
      },
      "materialized_counts": {
        "item_count": 5,
        "sha256": "c7cb5044f5ae88ebb494ae9f013a9beaea31a1a8bf879c680f5843901b501295",
        "value_kind": "object"
      },
      "missing_author_sample": {
        "item_count": 25,
        "sha256": "2029b08cef3cc2b317e2e92a98c1c91cfbed1f75ef27fafca4b6a895f7c9fc95",
        "value_kind": "rows"
      },
      "missing_institution_sample": {
        "item_count": 25,
        "sha256": "041d556c79b9cc31f860bd11a2eb21e1f96d47e8e9ce9c80b50b2f84fd9f03c5",
        "value_kind": "rows"
      },
      "referential_coverage": {
        "item_count": 26,
        "sha256": "fdc73192483ebb54d8e94660e9c417dae234a3e725cbd345d34b86df26212b1e",
        "value_kind": "object"
      },
      "year_type_topic_xpac": {
        "item_count": 1307378,
        "sha256": "9fd1a41a5f5bc8119582c700239d950531afec5124792c9998806df498e7da42",
        "value_kind": "rows"
      }
    },
    "gates": [
      {
        "actual": 10109733,
        "blocking": true,
        "evidence": {
          "query": "raw_work_rows"
        },
        "expected": 10109733,
        "name": "manifest_rows_match_parquet",
        "passed": true
      },
      {
        "actual": 10109733,
        "blocking": true,
        "evidence": {
          "query": "raw_work_rows"
        },
        "expected": 10109733,
        "name": "raw_work_ids_are_unique",
        "passed": true
      },
      {
        "actual": 0,
        "blocking": true,
        "evidence": {
          "raw_evidence": {
            "distinct_valid_pairs": 70415984,
            "duplicate_pair_delta": 0,
            "null_topic_scores": 0,
            "raw_reference_entries": 70415984,
            "rejected_id_entries": 0
          }
        },
        "expected": 0,
        "name": "raw_reference_ids_parse",
        "passed": true
      },
      {
        "actual": 0,
        "blocking": true,
        "evidence": {
          "raw_evidence": {
            "distinct_valid_pairs": 70415984,
            "duplicate_pair_delta": 0,
            "null_topic_scores": 0,
            "raw_reference_entries": 70415984,
            "rejected_id_entries": 0
          }
        },
        "expected": 0,
        "name": "topic_scores_are_non_null",
        "passed": true
      },
      {
        "actual": 16075482,
        "blocking": true,
        "evidence": {
          "raw_query": "raw_bridge_counts",
          "table_query": "materialized_counts"
        },
        "expected": 16075482,
        "name": "authors_bridge_reconciles",
        "passed": true
      },
      {
        "actual": 12517247,
        "blocking": true,
        "evidence": {
          "raw_query": "raw_bridge_counts",
          "table_query": "materialized_counts"
        },
        "expected": 12517247,
        "name": "institutions_bridge_reconciles",
        "passed": true
      },
      {
        "actual": 21657004,
        "blocking": true,
        "evidence": {
          "raw_query": "raw_bridge_counts",
          "table_query": "materialized_counts"
        },
        "expected": 21657004,
        "name": "topics_bridge_reconciles",
        "passed": true
      },
      {
        "actual": 70415984,
        "blocking": true,
        "evidence": {
          "duplicate_pair_delta": 0
        },
        "expected": 70415984,
        "name": "citation_pairs_reconcile",
        "passed": true
      },
      {
        "actual": 0,
        "blocking": true,
        "evidence": {
          "query": "referential_coverage"
        },
        "expected": 0,
        "name": "missing_works_for_authors",
        "passed": true
      },
      {
        "actual": 0,
        "blocking": true,
        "evidence": {
          "query": "referential_coverage"
        },
        "expected": 0,
        "name": "missing_topics",
        "passed": true
      },
      {
        "actual": 33354,
        "blocking": false,
        "evidence": {
          "affected_works": 33242,
          "deleted_author_rows": 0,
          "distinct_missing_ids": 238,
          "null_author_rows": 33089,
          "overall_coverage": 0.9979251633014798,
          "query": "referential_coverage",
          "sample_query": "missing_author_sample",
          "special_author_documentation": "https://help.openalex.org/hc/en-us/articles/28763618477975-Why-are-some-authors-assigned-to-NULL-AUTHOR-ID-A9999999999",
          "special_author_ids": [
            9999999999,
            5317838346
          ]
        },
        "expected": 0,
        "name": "missing_authors",
        "passed": false
      },
      {
        "actual": 0.9999834812674144,
        "blocking": true,
        "evidence": {
          "affected_works": 198,
          "distinct_ordinary_missing_ids": 237,
          "excluded_special_author_ids": [
            9999999999,
            5317838346
          ],
          "ordinary_authorship_rows": 16042393,
          "ordinary_missing_rows": 265,
          "query": "referential_coverage",
          "zero_denominator_convention": "coverage is 1 only when ordinary_authorship_rows is zero; authors_bridge_reconciles independently pins total bridge rows"
        },
        "expected": ">=0.999000",
        "name": "ordinary_author_reference_coverage",
        "passed": true
      },
      {
        "actual": 14602,
        "blocking": false,
        "evidence": {
          "distinct_missing_ids": 134,
          "query": "referential_coverage",
          "sample_query": "missing_institution_sample"
        },
        "expected": 0,
        "name": "missing_institutions",
        "passed": false
      },
      {
        "actual": 10109733,
        "blocking": true,
        "evidence": {
          "query": "works_id_uniqueness"
        },
        "expected": 10109733,
        "name": "works_ids_are_unique",
        "passed": true
      },
      {
        "actual": 119129660,
        "blocking": true,
        "evidence": {
          "query": "authors_id_uniqueness"
        },
        "expected": 119129660,
        "name": "authors_ids_are_unique",
        "passed": true
      },
      {
        "actual": 127784,
        "blocking": true,
        "evidence": {
          "query": "institutions_id_uniqueness"
        },
        "expected": 127784,
        "name": "institutions_ids_are_unique",
        "passed": true
      },
      {
        "actual": 283287,
        "blocking": true,
        "evidence": {
          "query": "sources_id_uniqueness"
        },
        "expected": 283287,
        "name": "sources_ids_are_unique",
        "passed": true
      },
      {
        "actual": 4516,
        "blocking": true,
        "evidence": {
          "query": "topics_id_uniqueness"
        },
        "expected": 4516,
        "name": "topics_ids_are_unique",
        "passed": true
      }
    ],
    "missing_author_sample": [
      {
        "author_id": 9999999999,
        "classification": "null_author",
        "display_names": [
          "",
          "\"Jos\u00e9 Francisco Vald\u00e9s-Galicia\"",
          "\"Lukas Einkemmer\"",
          "\"Ralf Kissmann\"",
          "\"The CIA's Hidden War.\""
        ],
        "raw_bridge_rows": 33089
      },
      {
        "author_id": 5013217494,
        "classification": "ordinary",
        "display_names": [
          "F. Xavier Medina",
          "Francesc-Xavier Medina"
        ],
        "raw_bridge_rows": 6
      },
      {
        "author_id": 5063807156,
        "classification": "ordinary",
        "display_names": [
          "Diego Redolar",
          "Diego Redolar Ripoll",
          "Diego Redolar-Ripoll"
        ],
        "raw_bridge_rows": 5
      },
      {
        "author_id": 5015883457,
        "classification": "ordinary",
        "display_names": [
          "Porter, SR"
        ],
        "raw_bridge_rows": 4
      },
      {
        "author_id": 5108107655,
        "classification": "ordinary",
        "display_names": [
          "Jos\u00e9 Brandariz",
          "Jos\u00e9 \u00c1ngel Brandariz",
          "Jos\u00e9 \u00c1ngel Brandariz Garc\u00eda"
        ],
        "raw_bridge_rows": 4
      },
      {
        "author_id": 5083729552,
        "classification": "ordinary",
        "display_names": [
          "Cristina Pujol",
          "Universitat Oberta de Catalunya"
        ],
        "raw_bridge_rows": 3
      },
      {
        "author_id": 5101601348,
        "classification": "ordinary",
        "display_names": [
          "A. Martelli",
          "Martelli, A."
        ],
        "raw_bridge_rows": 3
      },
      {
        "author_id": 5014983459,
        "classification": "ordinary",
        "display_names": [
          "Gomes, Maria Elisa Preto"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5031019573,
        "classification": "ordinary",
        "display_names": [
          "Nasir, ZA",
          "Nasir,\u00a0ZA"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5034986435,
        "classification": "ordinary",
        "display_names": [
          "Elisenda Ard\u00e8vol",
          "Elisenda Ard\u00e8vol Piera"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5041415886,
        "classification": "ordinary",
        "display_names": [
          "Poulsen, Niels Kj\u00f8lstad"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5074326473,
        "classification": "ordinary",
        "display_names": [
          "Borja Martinez",
          "Martinez, Borja"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5080662145,
        "classification": "ordinary",
        "display_names": [
          "ISIDORI, Andrea"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5099632339,
        "classification": "ordinary",
        "display_names": [
          "Zygmunt Bauman"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5099632340,
        "classification": "ordinary",
        "display_names": [
          "Prof Tim May"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5115575883,
        "classification": "ordinary",
        "display_names": [
          "Acad\u00e9mie nationale de m\u00e9decine"
        ],
        "raw_bridge_rows": 2
      },
      {
        "author_id": 5001400935,
        "classification": "ordinary",
        "display_names": [
          "Cecillon, L."
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5001448296,
        "classification": "ordinary",
        "display_names": [
          "Hagopian, S"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5002485218,
        "classification": "ordinary",
        "display_names": [
          "Copin, Y."
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5003024816,
        "classification": "ordinary",
        "display_names": [
          "Lamers, C."
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5004335124,
        "classification": "ordinary",
        "display_names": [
          "Kurki-Suonio, H."
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5004399630,
        "classification": "ordinary",
        "display_names": [
          "F. Etienne"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5004495876,
        "classification": "ordinary",
        "display_names": [
          "Abdoulaye, Tahirou"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5004822510,
        "classification": "ordinary",
        "display_names": [
          "Carvalho, W"
        ],
        "raw_bridge_rows": 1
      },
      {
        "author_id": 5005191039,
        "classification": "ordinary",
        "display_names": [
          "Chollet, Franck"
        ],
        "raw_bridge_rows": 1
      }
    ],
    "missing_institution_sample": [
      {
        "display_name": "Tampere University",
        "institution_id": 4210133110,
        "raw_bridge_rows": 3208
      },
      {
        "display_name": "Southwestern Medical Center",
        "institution_id": 4210096815,
        "raw_bridge_rows": 2069
      },
      {
        "display_name": "National Yang Ming Chiao Tung University",
        "institution_id": 96323854,
        "raw_bridge_rows": 1085
      },
      {
        "display_name": "North West Agriculture and Forestry University",
        "institution_id": 4210088176,
        "raw_bridge_rows": 876
      },
      {
        "display_name": "The University of Texas Health Science Center",
        "institution_id": 4210159031,
        "raw_bridge_rows": 696
      },
      {
        "display_name": "Institut Agro Montpelier",
        "institution_id": 4210136436,
        "raw_bridge_rows": 436
      },
      {
        "display_name": "University of Campania \"Luigi Vanvitelli\"",
        "institution_id": 4210126337,
        "raw_bridge_rows": 433
      },
      {
        "display_name": "University of Clermont Auvergne",
        "institution_id": 4210103002,
        "raw_bridge_rows": 430
      },
      {
        "display_name": "Seattle Children's Hospital",
        "institution_id": 4210109034,
        "raw_bridge_rows": 372
      },
      {
        "display_name": "Toulouse Mathematics Institute",
        "institution_id": 4210098964,
        "raw_bridge_rows": 227
      },
      {
        "display_name": "Lurie Children's Hospital",
        "institution_id": 4210125713,
        "raw_bridge_rows": 227
      },
      {
        "display_name": "Autonomous University of Yucat\u00e1n",
        "institution_id": 4210122862,
        "raw_bridge_rows": 181
      },
      {
        "display_name": "ZHAW Zurich University of Applied Sciences",
        "institution_id": 200744771,
        "raw_bridge_rows": 177
      },
      {
        "display_name": "University of Management and Technology",
        "institution_id": 4210089805,
        "raw_bridge_rows": 170
      },
      {
        "display_name": "Beibu Gulf University",
        "institution_id": 4210128032,
        "raw_bridge_rows": 169
      },
      {
        "display_name": "Department of Biomedicine Basel",
        "institution_id": 4210128905,
        "raw_bridge_rows": 166
      },
      {
        "display_name": "Pontificial Catholic University of Valparaiso",
        "institution_id": 4210116133,
        "raw_bridge_rows": 154
      },
      {
        "display_name": "Parul University",
        "institution_id": 4210112983,
        "raw_bridge_rows": 147
      },
      {
        "display_name": "Universit\u00e9 Paul-Val\u00e9ry Montpellier",
        "institution_id": 4210095130,
        "raw_bridge_rows": 139
      },
      {
        "display_name": "Netherlands Cancer Institute-Antoni van Leeuwenhoek Hospital",
        "institution_id": 4210124352,
        "raw_bridge_rows": 138
      },
      {
        "display_name": "The Nature Conservancy",
        "institution_id": 4210093580,
        "raw_bridge_rows": 137
      },
      {
        "display_name": "Federal University of S\u00e3o Jo\u00e3o del-Rei",
        "institution_id": 4210130985,
        "raw_bridge_rows": 134
      },
      {
        "display_name": "Texas A&M Health Science Center",
        "institution_id": 4210105967,
        "raw_bridge_rows": 127
      },
      {
        "display_name": "Klinik und Poliklinik f\u00fcr Hautkrankheiten",
        "institution_id": 4210096309,
        "raw_bridge_rows": 116
      },
      {
        "display_name": "Cracow University of Technology",
        "institution_id": 4210092770,
        "raw_bridge_rows": 113
      }
    ],
    "normalized_sha256": "531e11864e9400d1380f705917458d6c4347a7486fd169b53cdcfed2e0712b5b",
    "queries": [
      {
        "name": "raw_work_rows",
        "result_row_count": 1,
        "result_sha256": "56aabad587204e1a393c30baf149217c0ee158c3b8434f32e4eba7ae0aae34cf",
        "sql": "SELECT count() AS rows, uniqExact(id) AS unique_ids FROM file('tiers/stage2_medium/works/*.parquet', Parquet)",
        "sql_sha256": "5cca43f5303f6f77de8548e48e3b253f4fdd371536eb45f61817dd76a8e3c016"
      },
      {
        "name": "raw_bridge_counts",
        "result_row_count": 1,
        "result_sha256": "10478b44e6fea1feb3051bf9b4625e98038cf06496f8c0fac7d9dc751b5d6494",
        "sql": "SELECT (SELECT count() FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS a WHERE openalex_numeric_id(id) IS NOT NULL AND openalex_numeric_id(a.author.id) IS NOT NULL) AS authors, (SELECT uniqExact(tuple(openalex_numeric_id(id), openalex_numeric_id(a.author.id), openalex_numeric_id(i.id))) FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS a ARRAY JOIN a.institutions AS i WHERE openalex_numeric_id(id) IS NOT NULL AND openalex_numeric_id(a.author.id) IS NOT NULL AND openalex_numeric_id(i.id) IS NOT NULL) AS institutions, (SELECT count() FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN topics AS t WHERE openalex_numeric_id(id) IS NOT NULL AND openalex_numeric_id(t.id) IS NOT NULL AND t.score IS NOT NULL) AS topics",
        "sql_sha256": "93dcf68e68aadb14440aac0c84d26eb71fb4ef267f3bcdd6e390cc1f9703407f"
      },
      {
        "name": "materialized_counts",
        "result_row_count": 1,
        "result_sha256": "047939a06cf113e6883e8e3ade97f07d1b24f1fa5295d68a611feba1140d5de0",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.works) AS works, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_author) AS authors, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_institution) AS institutions, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_topic) AS topics, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.citation_edge) AS citations",
        "sql_sha256": "465b8bbac5ebba0f799e3f98aa4e22126b817899586b28baa0c99b6b1cfa7667"
      },
      {
        "name": "referential_coverage",
        "result_row_count": 1,
        "result_sha256": "9bfc14c04fcf4b2beb8ad257b9bc2d24f9e5b9f486bac539bfa8a33728e53a50",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.works w ON wa.work_id=w.work_id) AS missing_works_for_authors, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_author) AS author_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.authors a ON wa.author_id=a.author_id) AS missing_authors, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.authors a ON wa.author_id=a.author_id) AS distinct_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.authors a ON wa.author_id=a.author_id) AS works_with_missing_authors, if(author_bridge_rows = 0, 1., 1 - missing_authors / author_bridge_rows) AS author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_author WHERE author_id=9999999999) AS null_author_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_author WHERE author_id=5317838346) AS deleted_author_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_author WHERE author_id NOT IN (9999999999,5317838346)) AS ordinary_authorship_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS ordinary_missing_author_rows, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS distinct_ordinary_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS works_with_ordinary_missing_authors, if(ordinary_authorship_rows = 0, 1., 1 - ordinary_missing_author_rows / ordinary_authorship_rows) AS ordinary_author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_institution) AS institution_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.institutions i ON wi.institution_id=i.institution_id) AS missing_institutions, (SELECT uniqExact(wi.institution_id) FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.institutions i ON wi.institution_id=i.institution_id) AS distinct_missing_institution_ids, (SELECT uniqExact(wi.work_id) FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.institutions i ON wi.institution_id=i.institution_id) AS works_with_missing_institutions, (SELECT uniqExact(wi.author_id) FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.institutions i ON wi.institution_id=i.institution_id) AS authors_with_missing_institutions, if(institution_bridge_rows = 0, 1., (institution_bridge_rows - missing_institutions) / institution_bridge_rows) AS institution_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_topic) AS topic_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.topics t ON wt.topic_id=t.topic_id) AS missing_topics, (SELECT uniqExact(wt.topic_id) FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.topics t ON wt.topic_id=t.topic_id) AS distinct_missing_topic_ids, if(topic_bridge_rows = 0, 1., (topic_bridge_rows - missing_topics) / topic_bridge_rows) AS topic_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.citation_edge) AS citation_edges, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.citation_edge ce INNER JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.works w ON ce.cited_work_id=w.work_id) AS retained_cited_edges, if(citation_edges = 0, 1., retained_cited_edges / citation_edges) AS citation_retention_ratio",
        "sql_sha256": "a72751deea2feb71afe8b3790d27b9f7151fb887d363632db47870e8c3f50121"
      },
      {
        "name": "missing_author_sample",
        "result_row_count": 25,
        "result_sha256": "2029b08cef3cc2b317e2e92a98c1c91cfbed1f75ef27fafca4b6a895f7c9fc95",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wa.author_id FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.authors a ON wa.author_id=a.author_id) SELECT openalex_numeric_id(authorship.author.id) AS author_id, multiIf(author_id=9999999999, 'null_author', author_id=5317838346, 'deleted_author', 'ordinary') AS classification, arraySlice(arraySort(groupUniqArray(ifNull(authorship.author.display_name, ''))), 1, 5) AS display_names, count() AS raw_bridge_rows FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship WHERE openalex_numeric_id(authorship.author.id) IN missing_ids GROUP BY author_id ORDER BY raw_bridge_rows DESC, author_id LIMIT 25",
        "sql_sha256": "c645e188e08c310cba689e0663d240ed93b66c1a50a03d4681dbb2bca394ac6a"
      },
      {
        "name": "missing_institution_sample",
        "result_row_count": 25,
        "result_sha256": "041d556c79b9cc31f860bd11a2eb21e1f96d47e8e9ce9c80b50b2f84fd9f03c5",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wi.institution_id FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_900581fe.institutions i ON wi.institution_id=i.institution_id) SELECT openalex_numeric_id(raw_institution.id) AS institution_id, any(raw_institution.display_name) AS display_name, count() AS raw_bridge_rows FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship ARRAY JOIN authorship.institutions AS raw_institution WHERE openalex_numeric_id(raw_institution.id) IN missing_ids GROUP BY institution_id ORDER BY raw_bridge_rows DESC, institution_id LIMIT 25",
        "sql_sha256": "e36c3592f33d6e3559a36bdf1d40bc2a54edeaac23fdcd89a49bff110ab41404"
      },
      {
        "name": "works_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "56aabad587204e1a393c30baf149217c0ee158c3b8434f32e4eba7ae0aae34cf",
        "sql": "SELECT count() AS rows, uniqExact(work_id) AS unique_ids FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.works",
        "sql_sha256": "3c059472eb841f7d5e2c4f51caa24d4a41a414e0650cd59b34226e6f1cf8f2ed"
      },
      {
        "name": "authors_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "ad147b0c2afdbf81139c75c21696b85568b9bd6db2c30818e5fe0d962e8a0170",
        "sql": "SELECT count() AS rows, uniqExact(author_id) AS unique_ids FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.authors",
        "sql_sha256": "7b05139eedcc45ede9ecba9cf6581d1fa303a2a0f2debeb0b122918dcfd04bac"
      },
      {
        "name": "institutions_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "1d729a2ea001d72722af893931308d2a7ffb55562e2a5a3c33945a1cc15f9c47",
        "sql": "SELECT count() AS rows, uniqExact(institution_id) AS unique_ids FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.institutions",
        "sql_sha256": "c49f2b8176366d211a3232582296ad7f8d7c26530afd0c5f6ae2c170d19d1ea3"
      },
      {
        "name": "sources_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "8515fa4a030ad72ca441f50ae103ac1b7701fb65366d5de9dab09a297ce71e9f",
        "sql": "SELECT count() AS rows, uniqExact(source_id) AS unique_ids FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.sources",
        "sql_sha256": "8457e9fb80bcae13ec41a5312f0edbf5ada4da0cebb4cec564b465051e01c7b0"
      },
      {
        "name": "topics_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "83708a811c93190b16a1b7dbe7033261c7a31e9cc7d70ade69ae253c50e5ac75",
        "sql": "SELECT count() AS rows, uniqExact(topic_id) AS unique_ids FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.topics",
        "sql_sha256": "4426c9f8d751720309561b45c74a3ea7cfd0c44f9861c056d57cd2cf576979f0"
      },
      {
        "name": "year_type_topic_xpac_distribution",
        "result_row_count": 1307378,
        "result_sha256": "9fd1a41a5f5bc8119582c700239d950531afec5124792c9998806df498e7da42",
        "sql": "SELECT publication_year, work_type, primary_topic_id, is_xpac, count() AS works FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.works GROUP BY ALL ORDER BY ALL",
        "sql_sha256": "17d99f211803ac6546bad5e3e56a05884c954eaae73d1b1e314e10e545e401ba"
      },
      {
        "name": "authorships_per_work",
        "result_row_count": 447,
        "result_sha256": "2bc843d8da3f9998d26c7d558b7c8464e08af5a43f8e0128f60d3aa4c3f77d9e",
        "sql": "SELECT authorships, count() AS works FROM (SELECT work_id, count() AS authorships FROM openalex_stage2_stage2_repeat_medium_18c_900581fe.work_author GROUP BY work_id) GROUP BY authorships ORDER BY authorships",
        "sql_sha256": "2803cfda7e92eb90215e97a84540d698107a72e374fd261f56229e218588bcc9"
      }
    ],
    "raw_evidence": {
      "distinct_valid_pairs": 70415984,
      "duplicate_pair_delta": 0,
      "null_topic_scores": 0,
      "raw_reference_entries": 70415984,
      "rejected_id_entries": 0
    },
    "referential_coverage": {
      "author_bridge_rows": 16075482,
      "author_reference_coverage_ratio": 0.9979251633014798,
      "authors_with_missing_institutions": 12233,
      "citation_edges": 70415984,
      "citation_retention_ratio": 0.021169738961540324,
      "deleted_author_rows": 0,
      "distinct_missing_author_ids": 238,
      "distinct_missing_institution_ids": 134,
      "distinct_missing_topic_ids": 0,
      "distinct_ordinary_missing_author_ids": 237,
      "institution_bridge_rows": 12517247,
      "institution_reference_coverage_ratio": 0.9988334495596356,
      "missing_authors": 33354,
      "missing_institutions": 14602,
      "missing_topics": 0,
      "missing_works_for_authors": 0,
      "null_author_rows": 33089,
      "ordinary_author_reference_coverage_ratio": 0.9999834812674144,
      "ordinary_authorship_rows": 16042393,
      "ordinary_missing_author_rows": 265,
      "retained_cited_edges": 1490688,
      "topic_bridge_rows": 21657004,
      "topic_reference_coverage_ratio": 1,
      "works_with_missing_authors": 33242,
      "works_with_missing_institutions": 6908,
      "works_with_ordinary_missing_authors": 198
    },
    "sql_sha256": {
      "05_raw_evidence.sql": "486472a3a3a3ec5a2b11d965c4933a6bce4c1bd35dbdb31fe2d694f1c8d40e5a",
      "20_load_works.sql": "6e6b922df37d24d735791e6c8be8895a560496264b9a6f95e72c9abf4c441069"
    }
  }
}
```

## Sequential and concurrent evidence

```json
{
  "concurrent": {
    "stage2_medium": {
      "classes": {
        "join": {
          "count": 150,
          "insufficient_sample": false,
          "maximum_seconds": 10.652,
          "median_seconds": 2.862,
          "p95_seconds": 10.456,
          "peak_memory_bytes": 4542195053,
          "read_bytes": 227563532400,
          "read_rows": 10624296150,
          "spill_bytes": 0
        },
        "one_hop": {
          "count": 50,
          "insufficient_sample": false,
          "maximum_seconds": 0.083,
          "median_seconds": 0.006,
          "p95_seconds": 0.01,
          "peak_memory_bytes": 2174598,
          "read_bytes": 574721072,
          "read_rows": 71235184,
          "spill_bytes": 0
        },
        "routine": {
          "count": 99,
          "insufficient_sample": false,
          "maximum_seconds": 1.625,
          "median_seconds": 0.04,
          "p95_seconds": 1.574,
          "peak_memory_bytes": 6613705229,
          "read_bytes": 40987135276,
          "read_rows": 3955869866,
          "spill_bytes": 0
        }
      },
      "execution": {
        "cpus": 18,
        "maximum_seconds": 18000,
        "query_threads": 18,
        "workers": 1
      },
      "first_error": null,
      "forced_verdict": null,
      "merge_activity": {
        "completed_benchmark_merge_count": 0,
        "completed_foreign_merge_count": 0,
        "completed_merge_count": 1004,
        "completed_system_merge_count": 1004,
        "foreign_databases": [],
        "in_flight_benchmark_merge_count": 0,
        "in_flight_foreign_merge_count": 0,
        "in_flight_merge_count": 0,
        "in_flight_system_merge_count": 0,
        "maximum_completed_merge_ms": 371,
        "maximum_completed_system_merge_ms": 371,
        "part_log_coverage": {
          "maximum_event_at_unix_us": 1785986780275985,
          "minimum_event_at_unix_us": 1785868945280710,
          "row_count": 53138
        },
        "schema_version": 1,
        "status": "complete"
      },
      "queries": {
        "q01": {
          "count": 50,
          "maximum_seconds": 0.04,
          "median_seconds": 0.026,
          "p95_seconds": 0.029,
          "peak_memory_bytes": 122771976,
          "spill_bytes": 0
        },
        "q02": {
          "count": 50,
          "maximum_seconds": 10.652,
          "median_seconds": 10.216,
          "p95_seconds": 10.552,
          "peak_memory_bytes": 3110851898,
          "spill_bytes": 0
        },
        "q03": {
          "count": 50,
          "maximum_seconds": 3.106,
          "median_seconds": 2.84,
          "p95_seconds": 3.008,
          "peak_memory_bytes": 4542195053,
          "spill_bytes": 0
        },
        "q04": {
          "count": 50,
          "maximum_seconds": 2.93,
          "median_seconds": 2.728,
          "p95_seconds": 2.897,
          "peak_memory_bytes": 2273315470,
          "spill_bytes": 0
        },
        "q05": {
          "count": 50,
          "maximum_seconds": 0.083,
          "median_seconds": 0.006,
          "p95_seconds": 0.01,
          "peak_memory_bytes": 2174598,
          "spill_bytes": 0
        },
        "q07": {
          "count": 49,
          "maximum_seconds": 1.625,
          "median_seconds": 1.485,
          "p95_seconds": 1.59,
          "peak_memory_bytes": 6613705229,
          "spill_bytes": 0
        }
      },
      "server_restarted": false,
      "verdict_cap": "pass"
    }
  },
  "sequential": {
    "stage2_medium": [
      {
        "disk_read_elapsed_us": 34540,
        "elapsed_seconds": 0.046,
        "file_descriptor_read_bytes": 10303267,
        "finished_at_unix_us": 1785985634452229,
        "gating": true,
        "os_cpu_virtual_time_us": 254267,
        "os_cpu_wait_time_us": 18279,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10303267,
        "page_cache_miss_elapsed_us": 34241,
        "peak_memory_bytes": 120141554,
        "query_class": "routine",
        "query_id": "df512afc-6dbe-5945-a5d1-e55bf577bf44",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 981150,
        "result_rows": 9810,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985634406247,
        "synchronous_read_wait_us": 147625,
        "system_time_us": 29069,
        "user_time_us": 225403
      },
      {
        "disk_read_elapsed_us": 30951,
        "elapsed_seconds": 0.025,
        "file_descriptor_read_bytes": 10371190,
        "finished_at_unix_us": 1785985634852233,
        "gating": true,
        "os_cpu_virtual_time_us": 228077,
        "os_cpu_wait_time_us": 21425,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10371190,
        "page_cache_miss_elapsed_us": 30737,
        "peak_memory_bytes": 122018762,
        "query_class": "routine",
        "query_id": "daf2a53e-c750-5e2f-860b-e1505cfea366",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 496695,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985634827318,
        "synchronous_read_wait_us": 77412,
        "system_time_us": 11267,
        "user_time_us": 216984
      },
      {
        "disk_read_elapsed_us": 39777,
        "elapsed_seconds": 0.027,
        "file_descriptor_read_bytes": 10470767,
        "finished_at_unix_us": 1785985635239447,
        "gating": true,
        "os_cpu_virtual_time_us": 235401,
        "os_cpu_wait_time_us": 22726,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10470767,
        "page_cache_miss_elapsed_us": 39556,
        "peak_memory_bytes": 122342574,
        "query_class": "routine",
        "query_id": "d3bb4593-4c92-5135-a170-ffa8c6570ed0",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 551528,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985635212300,
        "synchronous_read_wait_us": 81128,
        "system_time_us": 22903,
        "user_time_us": 212702
      },
      {
        "disk_read_elapsed_us": 30812,
        "elapsed_seconds": 0.027,
        "file_descriptor_read_bytes": 10551275,
        "finished_at_unix_us": 1785985635605506,
        "gating": true,
        "os_cpu_virtual_time_us": 239646,
        "os_cpu_wait_time_us": 33285,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10551275,
        "page_cache_miss_elapsed_us": 30599,
        "peak_memory_bytes": 121583347,
        "query_class": "routine",
        "query_id": "5a32df48-5741-5587-ac89-9ce3aba1a9ab",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 543739,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985635578247,
        "synchronous_read_wait_us": 88062,
        "system_time_us": 19998,
        "user_time_us": 219801
      },
      {
        "disk_read_elapsed_us": 27975,
        "elapsed_seconds": 0.026,
        "file_descriptor_read_bytes": 10454619,
        "finished_at_unix_us": 1785985635977802,
        "gating": true,
        "os_cpu_virtual_time_us": 235261,
        "os_cpu_wait_time_us": 18527,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10454619,
        "page_cache_miss_elapsed_us": 27661,
        "peak_memory_bytes": 122227132,
        "query_class": "routine",
        "query_id": "e04f25c3-0733-5e23-9720-f93eefba728d",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 529757,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985635951215,
        "synchronous_read_wait_us": 90545,
        "system_time_us": 13525,
        "user_time_us": 221790
      },
      {
        "disk_read_elapsed_us": 32067,
        "elapsed_seconds": 0.029,
        "file_descriptor_read_bytes": 10292998,
        "finished_at_unix_us": 1785985636350780,
        "gating": true,
        "os_cpu_virtual_time_us": 237031,
        "os_cpu_wait_time_us": 27312,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10292998,
        "page_cache_miss_elapsed_us": 31877,
        "peak_memory_bytes": 122116054,
        "query_class": "routine",
        "query_id": "3f5f661e-7b16-5e6b-8061-a243b02826cf",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 589490,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985636321302,
        "synchronous_read_wait_us": 116750,
        "system_time_us": 20623,
        "user_time_us": 216585
      },
      {
        "disk_read_elapsed_us": 2439986,
        "elapsed_seconds": 9.722,
        "file_descriptor_read_bytes": 3389752436,
        "finished_at_unix_us": 1785985656062254,
        "gating": true,
        "os_cpu_virtual_time_us": 15582251,
        "os_cpu_wait_time_us": 3387367,
        "os_read_bytes": 20480,
        "page_cache_miss_bytes": 189964943,
        "page_cache_miss_elapsed_us": 102249,
        "peak_memory_bytes": 3016207320,
        "query_class": "join",
        "query_id": "13595f55-8ce6-5f96-9afd-a4a8889d126a",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 193390780,
        "result_rows": 579800,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985646401939,
        "synchronous_read_wait_us": 411540,
        "system_time_us": 1071558,
        "user_time_us": 14511743
      },
      {
        "disk_read_elapsed_us": 2340033,
        "elapsed_seconds": 9.541,
        "file_descriptor_read_bytes": 3057210499,
        "finished_at_unix_us": 1785985665948158,
        "gating": true,
        "os_cpu_virtual_time_us": 15629736,
        "os_cpu_wait_time_us": 3144385,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 189947958,
        "page_cache_miss_elapsed_us": 109218,
        "peak_memory_bytes": 3086706328,
        "query_class": "join",
        "query_id": "a2848046-3ec2-5022-963e-ecd8f76e25e6",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 189491174,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985656478576,
        "synchronous_read_wait_us": 228634,
        "system_time_us": 1192083,
        "user_time_us": 14438679
      },
      {
        "disk_read_elapsed_us": 2756144,
        "elapsed_seconds": 10.245,
        "file_descriptor_read_bytes": 3469372549,
        "finished_at_unix_us": 1785985676575862,
        "gating": true,
        "os_cpu_virtual_time_us": 16434434,
        "os_cpu_wait_time_us": 3493631,
        "os_read_bytes": 45056,
        "page_cache_miss_bytes": 189988208,
        "page_cache_miss_elapsed_us": 119788,
        "peak_memory_bytes": 3091917897,
        "query_class": "join",
        "query_id": "5504b261-1dca-5b3c-a586-47a9e9403c20",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 203762151,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985666394336,
        "synchronous_read_wait_us": 235837,
        "system_time_us": 1600634,
        "user_time_us": 14834633
      },
      {
        "disk_read_elapsed_us": 2598061,
        "elapsed_seconds": 10.543,
        "file_descriptor_read_bytes": 3400347180,
        "finished_at_unix_us": 1785985687427314,
        "gating": true,
        "os_cpu_virtual_time_us": 16438768,
        "os_cpu_wait_time_us": 3752483,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 189847248,
        "page_cache_miss_elapsed_us": 112957,
        "peak_memory_bytes": 3052018809,
        "query_class": "join",
        "query_id": "edd03e6a-5f6b-5a3c-9c5b-bc50f3eddaad",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 208958810,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985676982309,
        "synchronous_read_wait_us": 234464,
        "system_time_us": 1534329,
        "user_time_us": 14905457
      },
      {
        "disk_read_elapsed_us": 2493166,
        "elapsed_seconds": 9.892,
        "file_descriptor_read_bytes": 3164926790,
        "finished_at_unix_us": 1785985697677019,
        "gating": true,
        "os_cpu_virtual_time_us": 16123434,
        "os_cpu_wait_time_us": 3383369,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 189816328,
        "page_cache_miss_elapsed_us": 110406,
        "peak_memory_bytes": 3084373052,
        "query_class": "join",
        "query_id": "bfad4687-cb42-5ffe-bbec-e399dc66ffac",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 196204091,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985687874622,
        "synchronous_read_wait_us": 240934,
        "system_time_us": 1421949,
        "user_time_us": 14702426
      },
      {
        "disk_read_elapsed_us": 2747126,
        "elapsed_seconds": 10.354,
        "file_descriptor_read_bytes": 3466625362,
        "finished_at_unix_us": 1785985708423788,
        "gating": true,
        "os_cpu_virtual_time_us": 16580537,
        "os_cpu_wait_time_us": 3723112,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 189807330,
        "page_cache_miss_elapsed_us": 109542,
        "peak_memory_bytes": 3056047314,
        "query_class": "join",
        "query_id": "c63b7a6c-1bb7-5a2d-8f4b-edc4eb13fe71",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 205968032,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985698131540,
        "synchronous_read_wait_us": 251504,
        "system_time_us": 1586346,
        "user_time_us": 14995242
      },
      {
        "disk_read_elapsed_us": 3103487,
        "elapsed_seconds": 2.774,
        "file_descriptor_read_bytes": 3044011844,
        "finished_at_unix_us": 1785985720242430,
        "gating": true,
        "os_cpu_virtual_time_us": 14097814,
        "os_cpu_wait_time_us": 1320969,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2736090786,
        "page_cache_miss_elapsed_us": 2762886,
        "peak_memory_bytes": 4349239148,
        "query_class": "join",
        "query_id": "55a2bf14-7bc6-50bb-b8f8-e7afc7b5a6d8",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 58171759,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985717485254,
        "synchronous_read_wait_us": 6030150,
        "system_time_us": 1342955,
        "user_time_us": 12765263
      },
      {
        "disk_read_elapsed_us": 3341761,
        "elapsed_seconds": 2.689,
        "file_descriptor_read_bytes": 3043397496,
        "finished_at_unix_us": 1785985723310083,
        "gating": true,
        "os_cpu_virtual_time_us": 14431382,
        "os_cpu_wait_time_us": 1343000,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2735493253,
        "page_cache_miss_elapsed_us": 2999839,
        "peak_memory_bytes": 4382187884,
        "query_class": "join",
        "query_id": "68b45e30-86bb-5487-9691-09331c63a648",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 56589148,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985720636272,
        "synchronous_read_wait_us": 6255746,
        "system_time_us": 1471704,
        "user_time_us": 12968257
      },
      {
        "disk_read_elapsed_us": 3440115,
        "elapsed_seconds": 2.692,
        "file_descriptor_read_bytes": 3044223983,
        "finished_at_unix_us": 1785985726382712,
        "gating": true,
        "os_cpu_virtual_time_us": 14719223,
        "os_cpu_wait_time_us": 1415861,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2736288415,
        "page_cache_miss_elapsed_us": 3092106,
        "peak_memory_bytes": 4385547174,
        "query_class": "join",
        "query_id": "c3ea97aa-7c10-5851-805d-648e39c76f4d",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 56766069,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985723706506,
        "synchronous_read_wait_us": 6289122,
        "system_time_us": 1465318,
        "user_time_us": 13263520
      },
      {
        "disk_read_elapsed_us": 3274542,
        "elapsed_seconds": 2.862,
        "file_descriptor_read_bytes": 3044399845,
        "finished_at_unix_us": 1785985729603147,
        "gating": true,
        "os_cpu_virtual_time_us": 14993637,
        "os_cpu_wait_time_us": 1409955,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2736541829,
        "page_cache_miss_elapsed_us": 2898952,
        "peak_memory_bytes": 4383122816,
        "query_class": "join",
        "query_id": "02ca305d-ad37-5cb1-a79a-a037ed6dc1df",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 59846136,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985726757935,
        "synchronous_read_wait_us": 6337228,
        "system_time_us": 1476283,
        "user_time_us": 13527446
      },
      {
        "disk_read_elapsed_us": 3495699,
        "elapsed_seconds": 2.936,
        "file_descriptor_read_bytes": 3043053849,
        "finished_at_unix_us": 1785985732933210,
        "gating": true,
        "os_cpu_virtual_time_us": 14872287,
        "os_cpu_wait_time_us": 1424946,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2735201559,
        "page_cache_miss_elapsed_us": 3145089,
        "peak_memory_bytes": 4480786373,
        "query_class": "join",
        "query_id": "5e44ed1a-1a6c-53c4-963f-15b1773e443c",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 61750375,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985730010883,
        "synchronous_read_wait_us": 6263967,
        "system_time_us": 1543584,
        "user_time_us": 13337171
      },
      {
        "disk_read_elapsed_us": 3206356,
        "elapsed_seconds": 2.871,
        "file_descriptor_read_bytes": 3042802622,
        "finished_at_unix_us": 1785985736163488,
        "gating": true,
        "os_cpu_virtual_time_us": 15184660,
        "os_cpu_wait_time_us": 1511355,
        "os_read_bytes": 131072,
        "page_cache_miss_bytes": 2734870711,
        "page_cache_miss_elapsed_us": 2841551,
        "peak_memory_bytes": 4391087917,
        "query_class": "join",
        "query_id": "940ad897-60ba-5c49-9760-e4c1df1d7253",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 60071249,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985733309609,
        "synchronous_read_wait_us": 6517447,
        "system_time_us": 1659793,
        "user_time_us": 13535114
      },
      {
        "disk_read_elapsed_us": 119948,
        "elapsed_seconds": 2.543,
        "file_descriptor_read_bytes": 137386484,
        "finished_at_unix_us": 1785985749213150,
        "gating": true,
        "os_cpu_virtual_time_us": 5221803,
        "os_cpu_wait_time_us": 13225,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137386484,
        "page_cache_miss_elapsed_us": 118861,
        "peak_memory_bytes": 2265189914,
        "query_class": "join",
        "query_id": "7ba2143e-1129-5b61-aa62-5815d203c396",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 51088509,
        "result_rows": 110456,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985746669414,
        "synchronous_read_wait_us": 402014,
        "system_time_us": 110477,
        "user_time_us": 5112136
      },
      {
        "disk_read_elapsed_us": 109912,
        "elapsed_seconds": 2.592,
        "file_descriptor_read_bytes": 137196602,
        "finished_at_unix_us": 1785985752176183,
        "gating": true,
        "os_cpu_virtual_time_us": 5229659,
        "os_cpu_wait_time_us": 22072,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137196602,
        "page_cache_miss_elapsed_us": 108897,
        "peak_memory_bytes": 2254903162,
        "query_class": "join",
        "query_id": "cedb075c-63d5-5b0e-95b3-395ba6ca4d9a",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 51818655,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985749584957,
        "synchronous_read_wait_us": 215805,
        "system_time_us": 69349,
        "user_time_us": 5161166
      },
      {
        "disk_read_elapsed_us": 114171,
        "elapsed_seconds": 2.513,
        "file_descriptor_read_bytes": 137476431,
        "finished_at_unix_us": 1785985755039955,
        "gating": true,
        "os_cpu_virtual_time_us": 5194244,
        "os_cpu_wait_time_us": 747004,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137476431,
        "page_cache_miss_elapsed_us": 113199,
        "peak_memory_bytes": 2262694991,
        "query_class": "join",
        "query_id": "9801aa14-b9e6-5fd2-b51f-036a8ddf9c9a",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 50280859,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985752527028,
        "synchronous_read_wait_us": 226194,
        "system_time_us": 114327,
        "user_time_us": 5080822
      },
      {
        "disk_read_elapsed_us": 106984,
        "elapsed_seconds": 2.519,
        "file_descriptor_read_bytes": 136987034,
        "finished_at_unix_us": 1785985757922315,
        "gating": true,
        "os_cpu_virtual_time_us": 5169575,
        "os_cpu_wait_time_us": 325387,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 136987034,
        "page_cache_miss_elapsed_us": 106047,
        "peak_memory_bytes": 2260807808,
        "query_class": "join",
        "query_id": "cac9576c-5bbd-5797-b028-2d781cf4f7c1",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 50401563,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985755403585,
        "synchronous_read_wait_us": 233088,
        "system_time_us": 108667,
        "user_time_us": 5061782
      },
      {
        "disk_read_elapsed_us": 108892,
        "elapsed_seconds": 2.549,
        "file_descriptor_read_bytes": 137096365,
        "finished_at_unix_us": 1785985760849806,
        "gating": true,
        "os_cpu_virtual_time_us": 5175732,
        "os_cpu_wait_time_us": 22279,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137096365,
        "page_cache_miss_elapsed_us": 107957,
        "peak_memory_bytes": 2260069493,
        "query_class": "join",
        "query_id": "0810c65e-2c98-5cd1-b43c-bfb4c95a789a",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 50968399,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985758301700,
        "synchronous_read_wait_us": 212062,
        "system_time_us": 94197,
        "user_time_us": 5082380
      },
      {
        "disk_read_elapsed_us": 104406,
        "elapsed_seconds": 2.622,
        "file_descriptor_read_bytes": 137175615,
        "finished_at_unix_us": 1785985763832023,
        "gating": true,
        "os_cpu_virtual_time_us": 5274240,
        "os_cpu_wait_time_us": 20918,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137175615,
        "page_cache_miss_elapsed_us": 103508,
        "peak_memory_bytes": 2272654613,
        "query_class": "join",
        "query_id": "3b30e5aa-2e1a-5868-8c48-f7db737325cd",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 52459550,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985761210631,
        "synchronous_read_wait_us": 203255,
        "system_time_us": 122662,
        "user_time_us": 5152383
      },
      {
        "disk_read_elapsed_us": 956251,
        "elapsed_seconds": 0.102,
        "file_descriptor_read_bytes": 413586675,
        "finished_at_unix_us": 1785985773793374,
        "gating": true,
        "os_cpu_virtual_time_us": 488175,
        "os_cpu_wait_time_us": 82106,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 413512902,
        "page_cache_miss_elapsed_us": 954531,
        "peak_memory_bytes": 2178560,
        "query_class": "one_hop",
        "query_id": "b730b9c4-9614-57b4-b429-efae8d8cca95",
        "query_name": "q05",
        "read_bytes": 563458944,
        "read_rows": 70432368,
        "real_time_us": 3166333,
        "result_rows": 0,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985773691313,
        "synchronous_read_wait_us": 1471741,
        "system_time_us": 168353,
        "user_time_us": 321486
      },
      {
        "disk_read_elapsed_us": 790344,
        "elapsed_seconds": 0.085,
        "file_descriptor_read_bytes": 413695666,
        "finished_at_unix_us": 1785985774227742,
        "gating": true,
        "os_cpu_virtual_time_us": 491762,
        "os_cpu_wait_time_us": 64991,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 413695666,
        "page_cache_miss_elapsed_us": 788162,
        "peak_memory_bytes": 2171254,
        "query_class": "one_hop",
        "query_id": "4c447197-0298-5dcc-863c-bb68268e94b7",
        "query_name": "q05",
        "read_bytes": 563555736,
        "read_rows": 70432368,
        "real_time_us": 2461680,
        "result_rows": 46,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985774142841,
        "synchronous_read_wait_us": 1107653,
        "system_time_us": 196153,
        "user_time_us": 297023
      },
      {
        "disk_read_elapsed_us": 773919,
        "elapsed_seconds": 0.086,
        "file_descriptor_read_bytes": 413967145,
        "finished_at_unix_us": 1785985774681929,
        "gating": true,
        "os_cpu_virtual_time_us": 488881,
        "os_cpu_wait_time_us": 91247,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 413967145,
        "page_cache_miss_elapsed_us": 772621,
        "peak_memory_bytes": 2250886,
        "query_class": "one_hop",
        "query_id": "cecc163f-7a64-5b1a-8a6b-67432d383cf3",
        "query_name": "q05",
        "read_bytes": 563590016,
        "read_rows": 70432368,
        "real_time_us": 2470061,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985774595699,
        "synchronous_read_wait_us": 1111535,
        "system_time_us": 183772,
        "user_time_us": 306723
      },
      {
        "disk_read_elapsed_us": 0,
        "elapsed_seconds": 0.001,
        "file_descriptor_read_bytes": 0,
        "finished_at_unix_us": 1785985775036549,
        "gating": true,
        "os_cpu_virtual_time_us": 1178,
        "os_cpu_wait_time_us": 0,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 0,
        "page_cache_miss_elapsed_us": 0,
        "peak_memory_bytes": 317488,
        "query_class": "one_hop",
        "query_id": "56847c14-8888-5648-b76e-e6bcc1efb0fe",
        "query_name": "q05",
        "read_bytes": 0,
        "read_rows": 0,
        "real_time_us": 1500,
        "result_rows": 0,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985775035299,
        "synchronous_read_wait_us": 0,
        "system_time_us": 62,
        "user_time_us": 1117
      },
      {
        "disk_read_elapsed_us": 244,
        "elapsed_seconds": 0.006,
        "file_descriptor_read_bytes": 105193,
        "finished_at_unix_us": 1785985775413977,
        "gating": true,
        "os_cpu_virtual_time_us": 10586,
        "os_cpu_wait_time_us": 17,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 105193,
        "page_cache_miss_elapsed_us": 240,
        "peak_memory_bytes": 355542,
        "query_class": "one_hop",
        "query_id": "05433fc9-a0fd-5105-a0bf-222b56ccdaee",
        "query_name": "q05",
        "read_bytes": 227864,
        "read_rows": 16384,
        "real_time_us": 29430,
        "result_rows": 46,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985775407078,
        "synchronous_read_wait_us": 479,
        "system_time_us": 9150,
        "user_time_us": 1440
      },
      {
        "disk_read_elapsed_us": 195,
        "elapsed_seconds": 0.002,
        "file_descriptor_read_bytes": 83533,
        "finished_at_unix_us": 1785985775751732,
        "gating": true,
        "os_cpu_virtual_time_us": 2106,
        "os_cpu_wait_time_us": 16,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 83533,
        "page_cache_miss_elapsed_us": 192,
        "peak_memory_bytes": 436278,
        "query_class": "one_hop",
        "query_id": "4d1ec754-13eb-50d6-a22c-98ed007e69a9",
        "query_name": "q05",
        "read_bytes": 262144,
        "read_rows": 16384,
        "real_time_us": 6340,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985775749503,
        "synchronous_read_wait_us": 404,
        "system_time_us": 307,
        "user_time_us": 1805
      },
      {
        "disk_read_elapsed_us": 499,
        "elapsed_seconds": 0.004,
        "file_descriptor_read_bytes": 101562,
        "finished_at_unix_us": 1785985784764785,
        "gating": false,
        "os_cpu_virtual_time_us": 5571,
        "os_cpu_wait_time_us": 375,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 27789,
        "page_cache_miss_elapsed_us": 181,
        "peak_memory_bytes": 517424,
        "query_class": "two_hop",
        "query_id": "e3fe4ac0-fa86-5a02-8efd-25c540966369",
        "query_name": "q06",
        "read_bytes": 131072,
        "read_rows": 16384,
        "real_time_us": 33769,
        "result_rows": 1,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985784760266,
        "synchronous_read_wait_us": 632,
        "system_time_us": 2411,
        "user_time_us": 3171
      },
      {
        "disk_read_elapsed_us": 757858,
        "elapsed_seconds": 0.1,
        "file_descriptor_read_bytes": 452784897,
        "finished_at_unix_us": 1785985785205451,
        "gating": false,
        "os_cpu_virtual_time_us": 677974,
        "os_cpu_wait_time_us": 131082,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 452784897,
        "page_cache_miss_elapsed_us": 756074,
        "peak_memory_bytes": 4636792,
        "query_class": "two_hop",
        "query_id": "9d2e2953-22dd-5b31-b4e5-9cf8066454f2",
        "query_name": "q06",
        "read_bytes": 1126883608,
        "read_rows": 70432368,
        "real_time_us": 2737829,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985785104890,
        "synchronous_read_wait_us": 1229743,
        "system_time_us": 191153,
        "user_time_us": 488239
      },
      {
        "disk_read_elapsed_us": 774409,
        "elapsed_seconds": 0.101,
        "file_descriptor_read_bytes": 452467313,
        "finished_at_unix_us": 1785985785676216,
        "gating": false,
        "os_cpu_virtual_time_us": 705603,
        "os_cpu_wait_time_us": 116968,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 452467313,
        "page_cache_miss_elapsed_us": 772131,
        "peak_memory_bytes": 13426720,
        "query_class": "two_hop",
        "query_id": "31906d93-f6aa-506e-9e0d-98386489f28e",
        "query_name": "q06",
        "read_bytes": 1126917888,
        "read_rows": 70432368,
        "real_time_us": 2799087,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985785574478,
        "synchronous_read_wait_us": 1179400,
        "system_time_us": 164825,
        "user_time_us": 542117
      },
      {
        "disk_read_elapsed_us": 117,
        "elapsed_seconds": 0.003,
        "file_descriptor_read_bytes": 8840,
        "finished_at_unix_us": 1785985786026056,
        "gating": false,
        "os_cpu_virtual_time_us": 4979,
        "os_cpu_wait_time_us": 17,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 8840,
        "page_cache_miss_elapsed_us": 114,
        "peak_memory_bytes": 503040,
        "query_class": "two_hop",
        "query_id": "8be06a02-9757-5ba0-b974-acaa423bac3f",
        "query_name": "q06",
        "read_bytes": 131072,
        "read_rows": 16384,
        "real_time_us": 30689,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985786022689,
        "synchronous_read_wait_us": 231,
        "system_time_us": 2805,
        "user_time_us": 2182
      },
      {
        "disk_read_elapsed_us": 792935,
        "elapsed_seconds": 0.102,
        "file_descriptor_read_bytes": 452092633,
        "finished_at_unix_us": 1785985786476821,
        "gating": false,
        "os_cpu_virtual_time_us": 665867,
        "os_cpu_wait_time_us": 111048,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 452092633,
        "page_cache_miss_elapsed_us": 790802,
        "peak_memory_bytes": 5941437,
        "query_class": "two_hop",
        "query_id": "ca252312-d31a-51f9-97b5-8e8957b9d0f9",
        "query_name": "q06",
        "read_bytes": 1126883608,
        "read_rows": 70432368,
        "real_time_us": 2800192,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985786374317,
        "synchronous_read_wait_us": 1228971,
        "system_time_us": 197062,
        "user_time_us": 470360
      },
      {
        "disk_read_elapsed_us": 723616,
        "elapsed_seconds": 0.097,
        "file_descriptor_read_bytes": 452592726,
        "finished_at_unix_us": 1785985786934454,
        "gating": false,
        "os_cpu_virtual_time_us": 705454,
        "os_cpu_wait_time_us": 96560,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 452592726,
        "page_cache_miss_elapsed_us": 721430,
        "peak_memory_bytes": 13352165,
        "query_class": "two_hop",
        "query_id": "06e16dca-0cb0-5a21-a590-9ab54e9aecf3",
        "query_name": "q06",
        "read_bytes": 1126917888,
        "read_rows": 70432368,
        "real_time_us": 2660287,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985786836841,
        "synchronous_read_wait_us": 1114596,
        "system_time_us": 197411,
        "user_time_us": 509545
      },
      {
        "disk_read_elapsed_us": 763897,
        "elapsed_seconds": 1.24,
        "file_descriptor_read_bytes": 901580243,
        "finished_at_unix_us": 1785985797095365,
        "gating": true,
        "os_cpu_virtual_time_us": 17252138,
        "os_cpu_wait_time_us": 1100113,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426560991,
        "page_cache_miss_elapsed_us": 263972,
        "peak_memory_bytes": 6437137477,
        "query_class": "routine",
        "query_id": "98beb1b8-f4dc-5c3f-8698-b25017f646c8",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 24878754,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985795871693,
        "synchronous_read_wait_us": 1245092,
        "system_time_us": 659936,
        "user_time_us": 16594310
      },
      {
        "disk_read_elapsed_us": 867664,
        "elapsed_seconds": 1.229,
        "file_descriptor_read_bytes": 902566879,
        "finished_at_unix_us": 1785985798730321,
        "gating": true,
        "os_cpu_virtual_time_us": 17120560,
        "os_cpu_wait_time_us": 1098503,
        "os_read_bytes": 20480,
        "page_cache_miss_bytes": 426673313,
        "page_cache_miss_elapsed_us": 265346,
        "peak_memory_bytes": 5676376387,
        "query_class": "routine",
        "query_id": "8f02c1e1-b7c5-5c70-90de-d5aac44f331b",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 24481866,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985797519569,
        "synchronous_read_wait_us": 1207768,
        "system_time_us": 552037,
        "user_time_us": 16570691
      },
      {
        "disk_read_elapsed_us": 904319,
        "elapsed_seconds": 1.273,
        "file_descriptor_read_bytes": 901976074,
        "finished_at_unix_us": 1785985800321802,
        "gating": true,
        "os_cpu_virtual_time_us": 17442644,
        "os_cpu_wait_time_us": 1409197,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426786596,
        "page_cache_miss_elapsed_us": 328617,
        "peak_memory_bytes": 5860775149,
        "query_class": "routine",
        "query_id": "58755398-ae4b-5258-8d79-71348767369e",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 25010280,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985799090277,
        "synchronous_read_wait_us": 1402406,
        "system_time_us": 543139,
        "user_time_us": 16901502
      },
      {
        "disk_read_elapsed_us": 841846,
        "elapsed_seconds": 1.237,
        "file_descriptor_read_bytes": 901983947,
        "finished_at_unix_us": 1785985801965133,
        "gating": true,
        "os_cpu_virtual_time_us": 17368823,
        "os_cpu_wait_time_us": 1137922,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426869470,
        "page_cache_miss_elapsed_us": 254562,
        "peak_memory_bytes": 5919480741,
        "query_class": "routine",
        "query_id": "ca0b271f-58da-5e7a-ae72-b5fb29797641",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 24636026,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985800747147,
        "synchronous_read_wait_us": 1120388,
        "system_time_us": 610799,
        "user_time_us": 16760250
      },
      {
        "disk_read_elapsed_us": 914198,
        "elapsed_seconds": 1.276,
        "file_descriptor_read_bytes": 901730076,
        "finished_at_unix_us": 1785985803595679,
        "gating": true,
        "os_cpu_virtual_time_us": 17626403,
        "os_cpu_wait_time_us": 1102354,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426705782,
        "page_cache_miss_elapsed_us": 255206,
        "peak_memory_bytes": 5881307168,
        "query_class": "routine",
        "query_id": "590f6f1c-a94f-543d-9cc9-292c8eca5018",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 25103040,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985802355599,
        "synchronous_read_wait_us": 1083447,
        "system_time_us": 639426,
        "user_time_us": 16989772
      },
      {
        "disk_read_elapsed_us": 792867,
        "elapsed_seconds": 1.259,
        "file_descriptor_read_bytes": 901818197,
        "finished_at_unix_us": 1785985805232417,
        "gating": true,
        "os_cpu_virtual_time_us": 17680495,
        "os_cpu_wait_time_us": 1272035,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426668637,
        "page_cache_miss_elapsed_us": 256119,
        "peak_memory_bytes": 6109801141,
        "query_class": "routine",
        "query_id": "37eecc92-ac52-54ae-8794-7f5398c6662d",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 25063686,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785985803993164,
        "synchronous_read_wait_us": 1176734,
        "system_time_us": 682402,
        "user_time_us": 17000161
      }
    ]
  }
}
```

## Storage and capacity evidence

```json
{
  "capacity_model_status": "not yet validated at full corpus scale",
  "dimension_samples": [
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 31999198
      },
      "timestamp": 1785985566.2998989
    },
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 292128372
      },
      "timestamp": 1785985567.538465
    },
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 544857846
      },
      "timestamp": 1785985568.7662568
    },
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 820617094
      },
      "timestamp": 1785985569.99202
    },
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 942321443
      },
      "timestamp": 1785985571.2184079
    },
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1033867568
      },
      "timestamp": 1785985572.43287
    },
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1224939667
      },
      "timestamp": 1785985573.672172
    },
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1478397806
      },
      "timestamp": 1785985574.890176
    },
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1696474566
      },
      "timestamp": 1785985576.114602
    },
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1879934479
      },
      "timestamp": 1785985577.345477
    },
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2094373546
      },
      "timestamp": 1785985578.5613408
    },
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2362041966
      },
      "timestamp": 1785985579.800061
    },
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2607832477
      },
      "timestamp": 1785985581.0273669
    },
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2857931399
      },
      "timestamp": 1785985582.258591
    },
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3076356508
      },
      "timestamp": 1785985583.471806
    },
    {
      "filesystem_bytes": 3286265856,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3325475931
      },
      "timestamp": 1785985584.7106502
    },
    {
      "filesystem_bytes": 11121467392,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3400014177,
        "institutions": 4357308,
        "sources": 10677280,
        "topics": 150309
      },
      "timestamp": 1785985585.562724
    }
  ],
  "tiers": {
    "stage2_medium": [
      {
        "filesystem_bytes": 12290797568,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3370985788,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309
        },
        "timestamp": 1785985591.232002
      },
      {
        "filesystem_bytes": 12290797568,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3370985788,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 184585137
        },
        "timestamp": 1785985592.444638
      },
      {
        "filesystem_bytes": 12290797568,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3370985788,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 220443153
        },
        "timestamp": 1785985593.70507
      },
      {
        "filesystem_bytes": 12290797568,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348479837,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213799392
        },
        "timestamp": 1785985594.929163
      },
      {
        "filesystem_bytes": 12290797568,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348479837,
          "citation_edge": 55751436,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213799392
        },
        "timestamp": 1785985596.193145
      },
      {
        "filesystem_bytes": 12290797568,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348479837,
          "citation_edge": 187361023,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213799392
        },
        "timestamp": 1785985597.388227
      },
      {
        "filesystem_bytes": 12290797568,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348479837,
          "citation_edge": 314799147,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213799392
        },
        "timestamp": 1785985598.601825
      },
      {
        "filesystem_bytes": 12290797568,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348479837,
          "citation_edge": 466602130,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213799392
        },
        "timestamp": 1785985599.820551
      },
      {
        "filesystem_bytes": 12290797568,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348479837,
          "citation_edge": 594073186,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213799392
        },
        "timestamp": 1785985601.050456
      },
      {
        "filesystem_bytes": 12290797568,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348479837,
          "citation_edge": 580786218,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 100105542,
          "works": 213799392
        },
        "timestamp": 1785985602.2980638
      },
      {
        "filesystem_bytes": 12290797568,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348479837,
          "citation_edge": 516250207,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159130271,
          "works": 213799392
        },
        "timestamp": 1785985603.530587
      },
      {
        "filesystem_bytes": 12290797568,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348479837,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159130271,
          "work_institution": 36602900,
          "works": 213799392
        },
        "timestamp": 1785985604.7808158
      },
      {
        "filesystem_bytes": 12290797568,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348479837,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159130271,
          "work_institution": 69719157,
          "works": 213799392
        },
        "timestamp": 1785985606.02643
      },
      {
        "filesystem_bytes": 12290797568,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348479837,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159130271,
          "work_institution": 104042410,
          "work_topic": 20394050,
          "works": 213799392
        },
        "timestamp": 1785985607.2777941
      },
      {
        "filesystem_bytes": 12290797568,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348479837,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159130271,
          "work_institution": 100941640,
          "work_topic": 150685241,
          "works": 213799392
        },
        "timestamp": 1785985608.495229
      },
      {
        "filesystem_bytes": 15642726400,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348479837,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159130271,
          "work_institution": 100941640,
          "work_topic": 202518521,
          "works": 213799392
        },
        "timestamp": 1785985609.2507572
      }
    ]
  }
}
```

Scaling slopes are empirical evidence from sampled tiers; they are not a full-size prediction.

## Limitations

- This local Stage 2 run executed the requested 50 GiB ClickHouse container with 18 CPUs, 1 concurrent worker(s), and 18 query threads; no resource fallback was attempted.
- The OpenAlex manifests publish byte lengths and record counts but no content checksum; verification checks size and Parquet footer row counts and does not claim cryptographic object integrity.
- The Works samples are stratified by updated_date and are not a population-representative sample.
- Local Apple Silicon and local SSD latency is not extrapolated to an Alliance x86 VM with network-backed storage.
- The Alliance performance envelope remains unvalidated.
- stage2_medium: the canonical Authors snapshot leaves 33354 of 16075482 Work-author bridge rows unresolved, including 33089 documented NULL-author rows and 0 documented deleted-author rows. The ordinary unresolved count is 265 of 16042393 (coverage 0.9999834813; blocking floor 0.999000). Raw links are preserved; use LEFT JOIN when unmatched authorships matter.
