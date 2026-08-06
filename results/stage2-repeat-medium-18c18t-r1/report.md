# OpenAlex ClickHouse validation — stage2-repeat-medium-18c18t-r1

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
        "00_schema.sql": "1d224c02065f32587c45cbee4b234ab539407eb8b94bc8ce8ff754c72014f7c3",
        "11_load_complete_authors.sql": "5f95c957cdb0a9335471b58810d78a7f0605bc3987d668625947a7fc116cf241",
        "12_load_small_dimensions.sql": "c38feff5aaeae3d5962e1218cf7c0469a7b51407dd821735a66e0450e6ef0ad2",
        "30_reverse_projection.sql": "3ccf0eeb2ebe6e18f9e197bafbb154ec57bad8c5e65a8ee444dce2338f19e557",
        "stage2_medium/05_raw_evidence.sql": "486472a3a3a3ec5a2b11d965c4933a6bce4c1bd35dbdb31fe2d694f1c8d40e5a",
        "stage2_medium/20_load_works.sql": "f84de999d83d4070fbeb73915bfa2184cb26ae4e5aa7b383f3d1c00e45ddb8ac"
      },
      "run_id": "stage2-repeat-medium-18c18t-r1",
      "selection_sha256": "ccc7b5c51f04bd5972e6fb513f15157c13a79300be5fc5c36696aebbf56026b1",
      "sha256": "cd24b178823a08796ed2757e616e135881b3bbfdfc41eac2c2bb20bddcf2d1f0",
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
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.works) AS works, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_author) AS authors, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_institution) AS institutions, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_topic) AS topics, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.citation_edge) AS citations",
        "sql_sha256": "d563e99ed5adf5e697a5a71e5d834e219542bc663a32dfa0f56a5d1f9dd6e6ea"
      },
      {
        "name": "referential_coverage",
        "result_row_count": 1,
        "result_sha256": "9bfc14c04fcf4b2beb8ad257b9bc2d24f9e5b9f486bac539bfa8a33728e53a50",
        "sql": "SELECT (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.works w ON wa.work_id=w.work_id) AS missing_works_for_authors, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_author) AS author_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.authors a ON wa.author_id=a.author_id) AS missing_authors, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.authors a ON wa.author_id=a.author_id) AS distinct_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.authors a ON wa.author_id=a.author_id) AS works_with_missing_authors, if(author_bridge_rows = 0, 1., 1 - missing_authors / author_bridge_rows) AS author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_author WHERE author_id=9999999999) AS null_author_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_author WHERE author_id=5317838346) AS deleted_author_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_author WHERE author_id NOT IN (9999999999,5317838346)) AS ordinary_authorship_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS ordinary_missing_author_rows, (SELECT uniqExact(wa.author_id) FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS distinct_ordinary_missing_author_ids, (SELECT uniqExact(wa.work_id) FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.authors a ON wa.author_id=a.author_id WHERE wa.author_id NOT IN (9999999999,5317838346)) AS works_with_ordinary_missing_authors, if(ordinary_authorship_rows = 0, 1., 1 - ordinary_missing_author_rows / ordinary_authorship_rows) AS ordinary_author_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_institution) AS institution_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.institutions i ON wi.institution_id=i.institution_id) AS missing_institutions, (SELECT uniqExact(wi.institution_id) FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.institutions i ON wi.institution_id=i.institution_id) AS distinct_missing_institution_ids, (SELECT uniqExact(wi.work_id) FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.institutions i ON wi.institution_id=i.institution_id) AS works_with_missing_institutions, (SELECT uniqExact(wi.author_id) FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.institutions i ON wi.institution_id=i.institution_id) AS authors_with_missing_institutions, if(institution_bridge_rows = 0, 1., (institution_bridge_rows - missing_institutions) / institution_bridge_rows) AS institution_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_topic) AS topic_bridge_rows, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.topics t ON wt.topic_id=t.topic_id) AS missing_topics, (SELECT uniqExact(wt.topic_id) FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_topic wt LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.topics t ON wt.topic_id=t.topic_id) AS distinct_missing_topic_ids, if(topic_bridge_rows = 0, 1., (topic_bridge_rows - missing_topics) / topic_bridge_rows) AS topic_reference_coverage_ratio, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.citation_edge) AS citation_edges, (SELECT count() FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.citation_edge ce INNER JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.works w ON ce.cited_work_id=w.work_id) AS retained_cited_edges, if(citation_edges = 0, 1., retained_cited_edges / citation_edges) AS citation_retention_ratio",
        "sql_sha256": "e52273dda2cdf7a0d1d5bce4e98b166127e9c7d27610fe4281c9572200fdd8f8"
      },
      {
        "name": "missing_author_sample",
        "result_row_count": 25,
        "result_sha256": "2029b08cef3cc2b317e2e92a98c1c91cfbed1f75ef27fafca4b6a895f7c9fc95",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wa.author_id FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_author wa LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.authors a ON wa.author_id=a.author_id) SELECT openalex_numeric_id(authorship.author.id) AS author_id, multiIf(author_id=9999999999, 'null_author', author_id=5317838346, 'deleted_author', 'ordinary') AS classification, arraySlice(arraySort(groupUniqArray(ifNull(authorship.author.display_name, ''))), 1, 5) AS display_names, count() AS raw_bridge_rows FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship WHERE openalex_numeric_id(authorship.author.id) IN missing_ids GROUP BY author_id ORDER BY raw_bridge_rows DESC, author_id LIMIT 25",
        "sql_sha256": "37a0f0428d2abed3d7b23a9cb036855d2f7a4a5b1a5499278fae3627b0544868"
      },
      {
        "name": "missing_institution_sample",
        "result_row_count": 25,
        "result_sha256": "041d556c79b9cc31f860bd11a2eb21e1f96d47e8e9ce9c80b50b2f84fd9f03c5",
        "sql": "WITH missing_ids AS (SELECT DISTINCT wi.institution_id FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_institution wi LEFT ANTI JOIN openalex_stage2_stage2_repeat_medium_18c_71d30e8d.institutions i ON wi.institution_id=i.institution_id) SELECT openalex_numeric_id(raw_institution.id) AS institution_id, any(raw_institution.display_name) AS display_name, count() AS raw_bridge_rows FROM file('tiers/stage2_medium/works/*.parquet', Parquet) ARRAY JOIN authorships AS authorship ARRAY JOIN authorship.institutions AS raw_institution WHERE openalex_numeric_id(raw_institution.id) IN missing_ids GROUP BY institution_id ORDER BY raw_bridge_rows DESC, institution_id LIMIT 25",
        "sql_sha256": "a6f597c7722296424ee1716c91a78452716a8249f4e047839ab8d4ade48886e6"
      },
      {
        "name": "works_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "56aabad587204e1a393c30baf149217c0ee158c3b8434f32e4eba7ae0aae34cf",
        "sql": "SELECT count() AS rows, uniqExact(work_id) AS unique_ids FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.works",
        "sql_sha256": "9301b4fd5010ba5589701e8b20d10b70ef59d59c3c9cc5c5706a8b6e3747e3e2"
      },
      {
        "name": "authors_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "ad147b0c2afdbf81139c75c21696b85568b9bd6db2c30818e5fe0d962e8a0170",
        "sql": "SELECT count() AS rows, uniqExact(author_id) AS unique_ids FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.authors",
        "sql_sha256": "81b00523b8a7ead82b79bb43d2ea805c01d1709ecb707e2ac9a20f9588474d31"
      },
      {
        "name": "institutions_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "1d729a2ea001d72722af893931308d2a7ffb55562e2a5a3c33945a1cc15f9c47",
        "sql": "SELECT count() AS rows, uniqExact(institution_id) AS unique_ids FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.institutions",
        "sql_sha256": "eee672753a108cf89639883a93372a8e7e7e847e739bb66b3e8313d7db7cd7f2"
      },
      {
        "name": "sources_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "8515fa4a030ad72ca441f50ae103ac1b7701fb65366d5de9dab09a297ce71e9f",
        "sql": "SELECT count() AS rows, uniqExact(source_id) AS unique_ids FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.sources",
        "sql_sha256": "6150cb1859338e7efba588467aae7409e1f06737a1622f7fe98f8387dc3e934c"
      },
      {
        "name": "topics_id_uniqueness",
        "result_row_count": 1,
        "result_sha256": "83708a811c93190b16a1b7dbe7033261c7a31e9cc7d70ade69ae253c50e5ac75",
        "sql": "SELECT count() AS rows, uniqExact(topic_id) AS unique_ids FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.topics",
        "sql_sha256": "7b994216be62b34b8e6ddc6ee7f92a3fdcf836fdf351b9f40b048b982d198e72"
      },
      {
        "name": "year_type_topic_xpac_distribution",
        "result_row_count": 1307378,
        "result_sha256": "9fd1a41a5f5bc8119582c700239d950531afec5124792c9998806df498e7da42",
        "sql": "SELECT publication_year, work_type, primary_topic_id, is_xpac, count() AS works FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.works GROUP BY ALL ORDER BY ALL",
        "sql_sha256": "481943c13c648c7184ab797a2161f9969d6e8da0946c7ee4422dcae339b341af"
      },
      {
        "name": "authorships_per_work",
        "result_row_count": 447,
        "result_sha256": "2bc843d8da3f9998d26c7d558b7c8464e08af5a43f8e0128f60d3aa4c3f77d9e",
        "sql": "SELECT authorships, count() AS works FROM (SELECT work_id, count() AS authorships FROM openalex_stage2_stage2_repeat_medium_18c_71d30e8d.work_author GROUP BY work_id) GROUP BY authorships ORDER BY authorships",
        "sql_sha256": "fd6f142808ca5ad438c9654166a9b9d0ccdd4b2ab26d15c473ac246c9e648274"
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
      "20_load_works.sql": "f84de999d83d4070fbeb73915bfa2184cb26ae4e5aa7b383f3d1c00e45ddb8ac"
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
          "maximum_seconds": 11.07,
          "median_seconds": 2.915,
          "p95_seconds": 10.583,
          "peak_memory_bytes": 4523914495,
          "read_bytes": 227563532400,
          "read_rows": 10624296150,
          "spill_bytes": 0
        },
        "one_hop": {
          "count": 50,
          "insufficient_sample": false,
          "maximum_seconds": 0.086,
          "median_seconds": 0.006,
          "p95_seconds": 0.01,
          "peak_memory_bytes": 2313070,
          "read_bytes": 574721072,
          "read_rows": 71235184,
          "spill_bytes": 0
        },
        "routine": {
          "count": 99,
          "insufficient_sample": false,
          "maximum_seconds": 1.595,
          "median_seconds": 0.053,
          "p95_seconds": 1.566,
          "peak_memory_bytes": 6748442901,
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
        "completed_merge_count": 1239,
        "completed_system_merge_count": 1239,
        "foreign_databases": [],
        "in_flight_benchmark_merge_count": 0,
        "in_flight_foreign_merge_count": 0,
        "in_flight_merge_count": 0,
        "in_flight_system_merge_count": 0,
        "maximum_completed_merge_ms": 3420,
        "maximum_completed_system_merge_ms": 3420,
        "part_log_coverage": {
          "maximum_event_at_unix_us": 1785983674753387,
          "minimum_event_at_unix_us": 1785868945280710,
          "row_count": 49449
        },
        "schema_version": 1,
        "status": "complete"
      },
      "queries": {
        "q01": {
          "count": 50,
          "maximum_seconds": 0.053,
          "median_seconds": 0.026,
          "p95_seconds": 0.033,
          "peak_memory_bytes": 122058027,
          "spill_bytes": 0
        },
        "q02": {
          "count": 50,
          "maximum_seconds": 11.07,
          "median_seconds": 10.257,
          "p95_seconds": 10.774,
          "peak_memory_bytes": 3130756420,
          "spill_bytes": 0
        },
        "q03": {
          "count": 50,
          "maximum_seconds": 3.048,
          "median_seconds": 2.912,
          "p95_seconds": 3.024,
          "peak_memory_bytes": 4523914495,
          "spill_bytes": 0
        },
        "q04": {
          "count": 50,
          "maximum_seconds": 2.923,
          "median_seconds": 2.745,
          "p95_seconds": 2.915,
          "peak_memory_bytes": 2274594178,
          "spill_bytes": 0
        },
        "q05": {
          "count": 50,
          "maximum_seconds": 0.086,
          "median_seconds": 0.006,
          "p95_seconds": 0.01,
          "peak_memory_bytes": 2313070,
          "spill_bytes": 0
        },
        "q07": {
          "count": 49,
          "maximum_seconds": 1.595,
          "median_seconds": 1.519,
          "p95_seconds": 1.583,
          "peak_memory_bytes": 6748442901,
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
        "disk_read_elapsed_us": 34936,
        "elapsed_seconds": 0.043,
        "file_descriptor_read_bytes": 10225607,
        "finished_at_unix_us": 1785982516471007,
        "gating": true,
        "os_cpu_virtual_time_us": 256110,
        "os_cpu_wait_time_us": 18994,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10225607,
        "page_cache_miss_elapsed_us": 34637,
        "peak_memory_bytes": 120072986,
        "query_class": "routine",
        "query_id": "df512afc-6dbe-5945-a5d1-e55bf577bf44",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 876600,
        "result_rows": 9810,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982516427679,
        "synchronous_read_wait_us": 97110,
        "system_time_us": 27173,
        "user_time_us": 229223
      },
      {
        "disk_read_elapsed_us": 31013,
        "elapsed_seconds": 0.025,
        "file_descriptor_read_bytes": 10118752,
        "finished_at_unix_us": 1785982516837240,
        "gating": true,
        "os_cpu_virtual_time_us": 240464,
        "os_cpu_wait_time_us": 13654,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10118752,
        "page_cache_miss_elapsed_us": 30787,
        "peak_memory_bytes": 121601394,
        "query_class": "routine",
        "query_id": "daf2a53e-c750-5e2f-860b-e1505cfea366",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 510232,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982516811725,
        "synchronous_read_wait_us": 75875,
        "system_time_us": 19249,
        "user_time_us": 221404
      },
      {
        "disk_read_elapsed_us": 39690,
        "elapsed_seconds": 0.026,
        "file_descriptor_read_bytes": 10099869,
        "finished_at_unix_us": 1785982517221729,
        "gating": true,
        "os_cpu_virtual_time_us": 236831,
        "os_cpu_wait_time_us": 15389,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10099869,
        "page_cache_miss_elapsed_us": 39479,
        "peak_memory_bytes": 121333961,
        "query_class": "routine",
        "query_id": "d3bb4593-4c92-5135-a170-ffa8c6570ed0",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 532966,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982517195574,
        "synchronous_read_wait_us": 89324,
        "system_time_us": 22109,
        "user_time_us": 215112
      },
      {
        "disk_read_elapsed_us": 33050,
        "elapsed_seconds": 0.027,
        "file_descriptor_read_bytes": 10099633,
        "finished_at_unix_us": 1785982517588992,
        "gating": true,
        "os_cpu_virtual_time_us": 234377,
        "os_cpu_wait_time_us": 20970,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10099633,
        "page_cache_miss_elapsed_us": 32712,
        "peak_memory_bytes": 121604589,
        "query_class": "routine",
        "query_id": "5a32df48-5741-5587-ac89-9ce3aba1a9ab",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 546796,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982517561686,
        "synchronous_read_wait_us": 108212,
        "system_time_us": 19714,
        "user_time_us": 214825
      },
      {
        "disk_read_elapsed_us": 38443,
        "elapsed_seconds": 0.027,
        "file_descriptor_read_bytes": 10087309,
        "finished_at_unix_us": 1785982517955712,
        "gating": true,
        "os_cpu_virtual_time_us": 242777,
        "os_cpu_wait_time_us": 15055,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10087309,
        "page_cache_miss_elapsed_us": 38136,
        "peak_memory_bytes": 121329182,
        "query_class": "routine",
        "query_id": "e04f25c3-0733-5e23-9720-f93eefba728d",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 562681,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982517927948,
        "synchronous_read_wait_us": 106962,
        "system_time_us": 25190,
        "user_time_us": 217775
      },
      {
        "disk_read_elapsed_us": 28914,
        "elapsed_seconds": 0.026,
        "file_descriptor_read_bytes": 10062835,
        "finished_at_unix_us": 1785982518319660,
        "gating": true,
        "os_cpu_virtual_time_us": 238395,
        "os_cpu_wait_time_us": 22755,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 10062835,
        "page_cache_miss_elapsed_us": 28576,
        "peak_memory_bytes": 121440482,
        "query_class": "routine",
        "query_id": "3f5f661e-7b16-5e6b-8061-a243b02826cf",
        "query_name": "q01",
        "read_bytes": 60658398,
        "read_rows": 10109733,
        "real_time_us": 520105,
        "result_rows": 9810,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982518293591,
        "synchronous_read_wait_us": 84377,
        "system_time_us": 15060,
        "user_time_us": 223523
      },
      {
        "disk_read_elapsed_us": 2148394,
        "elapsed_seconds": 9.569,
        "file_descriptor_read_bytes": 3092895143,
        "finished_at_unix_us": 1785982541019668,
        "gating": true,
        "os_cpu_virtual_time_us": 15145461,
        "os_cpu_wait_time_us": 2780427,
        "os_read_bytes": 126976,
        "page_cache_miss_bytes": 189772045,
        "page_cache_miss_elapsed_us": 119555,
        "peak_memory_bytes": 3061024476,
        "query_class": "join",
        "query_id": "13595f55-8ce6-5f96-9afd-a4a8889d126a",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 190309551,
        "result_rows": 579800,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982531512486,
        "synchronous_read_wait_us": 278151,
        "system_time_us": 1089561,
        "user_time_us": 14056983
      },
      {
        "disk_read_elapsed_us": 2018570,
        "elapsed_seconds": 9.389,
        "file_descriptor_read_bytes": 2861962707,
        "finished_at_unix_us": 1785982550763069,
        "gating": true,
        "os_cpu_virtual_time_us": 15177494,
        "os_cpu_wait_time_us": 2538655,
        "os_read_bytes": 77824,
        "page_cache_miss_bytes": 190008241,
        "page_cache_miss_elapsed_us": 107034,
        "peak_memory_bytes": 3114826914,
        "query_class": "join",
        "query_id": "a2848046-3ec2-5022-963e-ecd8f76e25e6",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 186624838,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982541435867,
        "synchronous_read_wait_us": 230836,
        "system_time_us": 1053778,
        "user_time_us": 14124724
      },
      {
        "disk_read_elapsed_us": 2044878,
        "elapsed_seconds": 9.883,
        "file_descriptor_read_bytes": 3040948107,
        "finished_at_unix_us": 1785982560990827,
        "gating": true,
        "os_cpu_virtual_time_us": 15570516,
        "os_cpu_wait_time_us": 3214964,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 190009542,
        "page_cache_miss_elapsed_us": 112873,
        "peak_memory_bytes": 3052433036,
        "query_class": "join",
        "query_id": "5504b261-1dca-5b3c-a586-47a9e9403c20",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 196348340,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982551179965,
        "synchronous_read_wait_us": 232430,
        "system_time_us": 1192962,
        "user_time_us": 14378552
      },
      {
        "disk_read_elapsed_us": 2736390,
        "elapsed_seconds": 10.076,
        "file_descriptor_read_bytes": 3631065693,
        "finished_at_unix_us": 1785982571422282,
        "gating": true,
        "os_cpu_virtual_time_us": 16431051,
        "os_cpu_wait_time_us": 3601622,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 189872575,
        "page_cache_miss_elapsed_us": 109764,
        "peak_memory_bytes": 3072100246,
        "query_class": "join",
        "query_id": "edd03e6a-5f6b-5a3c-9c5b-bc50f3eddaad",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 199986029,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982561424628,
        "synchronous_read_wait_us": 221941,
        "system_time_us": 1440770,
        "user_time_us": 14991287
      },
      {
        "disk_read_elapsed_us": 2279672,
        "elapsed_seconds": 9.804,
        "file_descriptor_read_bytes": 3132561905,
        "finished_at_unix_us": 1785982581591574,
        "gating": true,
        "os_cpu_virtual_time_us": 15790598,
        "os_cpu_wait_time_us": 2839989,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 190004378,
        "page_cache_miss_elapsed_us": 103584,
        "peak_memory_bytes": 3091133585,
        "query_class": "join",
        "query_id": "bfad4687-cb42-5ffe-bbec-e399dc66ffac",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 194934692,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982571851076,
        "synchronous_read_wait_us": 228340,
        "system_time_us": 1354263,
        "user_time_us": 14437377
      },
      {
        "disk_read_elapsed_us": 2547090,
        "elapsed_seconds": 10.235,
        "file_descriptor_read_bytes": 3391810399,
        "finished_at_unix_us": 1785982592169013,
        "gating": true,
        "os_cpu_virtual_time_us": 16067028,
        "os_cpu_wait_time_us": 3527911,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 189815787,
        "page_cache_miss_elapsed_us": 127605,
        "peak_memory_bytes": 3120780889,
        "query_class": "join",
        "query_id": "c63b7a6c-1bb7-5a2d-8f4b-edc4eb13fe71",
        "query_name": "q02",
        "read_bytes": 498370632,
        "read_rows": 31771253,
        "real_time_us": 203597154,
        "result_rows": 579800,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982581996222,
        "synchronous_read_wait_us": 262768,
        "system_time_us": 1532790,
        "user_time_us": 14535292
      },
      {
        "disk_read_elapsed_us": 2955486,
        "elapsed_seconds": 2.683,
        "file_descriptor_read_bytes": 3044055352,
        "finished_at_unix_us": 1785982605263291,
        "gating": true,
        "os_cpu_virtual_time_us": 13931506,
        "os_cpu_wait_time_us": 1148936,
        "os_read_bytes": 262144,
        "page_cache_miss_bytes": 2736113683,
        "page_cache_miss_elapsed_us": 2600936,
        "peak_memory_bytes": 4397062743,
        "query_class": "join",
        "query_id": "55a2bf14-7bc6-50bb-b8f8-e7afc7b5a6d8",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 56063245,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982602604217,
        "synchronous_read_wait_us": 6296759,
        "system_time_us": 1275426,
        "user_time_us": 12665819
      },
      {
        "disk_read_elapsed_us": 3052586,
        "elapsed_seconds": 2.797,
        "file_descriptor_read_bytes": 3042716088,
        "finished_at_unix_us": 1785982608420479,
        "gating": true,
        "os_cpu_virtual_time_us": 14357186,
        "os_cpu_wait_time_us": 1210990,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2734775271,
        "page_cache_miss_elapsed_us": 2733615,
        "peak_memory_bytes": 4370266247,
        "query_class": "join",
        "query_id": "68b45e30-86bb-5487-9691-09331c63a648",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 58526579,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982605637085,
        "synchronous_read_wait_us": 6263473,
        "system_time_us": 1393204,
        "user_time_us": 12973546
      },
      {
        "disk_read_elapsed_us": 3041674,
        "elapsed_seconds": 2.785,
        "file_descriptor_read_bytes": 3043826923,
        "finished_at_unix_us": 1785982611552724,
        "gating": true,
        "os_cpu_virtual_time_us": 14377572,
        "os_cpu_wait_time_us": 1363921,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2735953545,
        "page_cache_miss_elapsed_us": 2731190,
        "peak_memory_bytes": 4382242182,
        "query_class": "join",
        "query_id": "c3ea97aa-7c10-5851-805d-648e39c76f4d",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 58254268,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982608783891,
        "synchronous_read_wait_us": 6382746,
        "system_time_us": 1406565,
        "user_time_us": 12980428
      },
      {
        "disk_read_elapsed_us": 3048998,
        "elapsed_seconds": 2.826,
        "file_descriptor_read_bytes": 3045634676,
        "finished_at_unix_us": 1785982614717873,
        "gating": true,
        "os_cpu_virtual_time_us": 14523364,
        "os_cpu_wait_time_us": 1167773,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2737659423,
        "page_cache_miss_elapsed_us": 2736076,
        "peak_memory_bytes": 4394653020,
        "query_class": "join",
        "query_id": "02ca305d-ad37-5cb1-a79a-a037ed6dc1df",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 58995718,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982611907646,
        "synchronous_read_wait_us": 6301496,
        "system_time_us": 1468013,
        "user_time_us": 13065222
      },
      {
        "disk_read_elapsed_us": 3195055,
        "elapsed_seconds": 2.854,
        "file_descriptor_read_bytes": 3044527919,
        "finished_at_unix_us": 1785982617912754,
        "gating": true,
        "os_cpu_virtual_time_us": 14611968,
        "os_cpu_wait_time_us": 1231929,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2736464155,
        "page_cache_miss_elapsed_us": 2877359,
        "peak_memory_bytes": 4350908846,
        "query_class": "join",
        "query_id": "5e44ed1a-1a6c-53c4-963f-15b1773e443c",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 59805357,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982615073423,
        "synchronous_read_wait_us": 6784709,
        "system_time_us": 1548218,
        "user_time_us": 13073482
      },
      {
        "disk_read_elapsed_us": 3246562,
        "elapsed_seconds": 2.821,
        "file_descriptor_read_bytes": 3044808262,
        "finished_at_unix_us": 1785982621071401,
        "gating": true,
        "os_cpu_virtual_time_us": 15038922,
        "os_cpu_wait_time_us": 1246866,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 2736857371,
        "page_cache_miss_elapsed_us": 2932531,
        "peak_memory_bytes": 4364112199,
        "query_class": "join",
        "query_id": "940ad897-60ba-5c49-9760-e4c1df1d7253",
        "query_name": "q03",
        "read_bytes": 3536312605,
        "read_rows": 145314875,
        "real_time_us": 59169071,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982618267466,
        "synchronous_read_wait_us": 6638321,
        "system_time_us": 1619409,
        "user_time_us": 13429838
      },
      {
        "disk_read_elapsed_us": 116218,
        "elapsed_seconds": 2.506,
        "file_descriptor_read_bytes": 137130090,
        "finished_at_unix_us": 1785982633148699,
        "gating": true,
        "os_cpu_virtual_time_us": 5122653,
        "os_cpu_wait_time_us": 24608,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137130090,
        "page_cache_miss_elapsed_us": 115329,
        "peak_memory_bytes": 2262226179,
        "query_class": "join",
        "query_id": "7ba2143e-1129-5b61-aa62-5815d203c396",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 50230959,
        "result_rows": 110456,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982630643647,
        "synchronous_read_wait_us": 308768,
        "system_time_us": 99004,
        "user_time_us": 5024441
      },
      {
        "disk_read_elapsed_us": 101089,
        "elapsed_seconds": 2.483,
        "file_descriptor_read_bytes": 137260434,
        "finished_at_unix_us": 1785982635995376,
        "gating": true,
        "os_cpu_virtual_time_us": 5072853,
        "os_cpu_wait_time_us": 15640,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137260434,
        "page_cache_miss_elapsed_us": 100257,
        "peak_memory_bytes": 2268042674,
        "query_class": "join",
        "query_id": "cedb075c-63d5-5b0e-95b3-395ba6ca4d9a",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 49636471,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982633513255,
        "synchronous_read_wait_us": 193472,
        "system_time_us": 77322,
        "user_time_us": 4996369
      },
      {
        "disk_read_elapsed_us": 113553,
        "elapsed_seconds": 2.464,
        "file_descriptor_read_bytes": 137113270,
        "finished_at_unix_us": 1785982638805458,
        "gating": true,
        "os_cpu_virtual_time_us": 5056304,
        "os_cpu_wait_time_us": 17325,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137113270,
        "page_cache_miss_elapsed_us": 112681,
        "peak_memory_bytes": 2263188196,
        "query_class": "join",
        "query_id": "9801aa14-b9e6-5fd2-b51f-036a8ddf9c9a",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 49315525,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982636341971,
        "synchronous_read_wait_us": 206134,
        "system_time_us": 97747,
        "user_time_us": 4959390
      },
      {
        "disk_read_elapsed_us": 140541,
        "elapsed_seconds": 2.532,
        "file_descriptor_read_bytes": 137311668,
        "finished_at_unix_us": 1785982641674299,
        "gating": true,
        "os_cpu_virtual_time_us": 5141432,
        "os_cpu_wait_time_us": 18481,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137311668,
        "page_cache_miss_elapsed_us": 139454,
        "peak_memory_bytes": 2263772140,
        "query_class": "join",
        "query_id": "cac9576c-5bbd-5797-b028-2d781cf4f7c1",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 50710447,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982639142495,
        "synchronous_read_wait_us": 240044,
        "system_time_us": 100383,
        "user_time_us": 5041876
      },
      {
        "disk_read_elapsed_us": 94809,
        "elapsed_seconds": 2.499,
        "file_descriptor_read_bytes": 137137744,
        "finished_at_unix_us": 1785982644513166,
        "gating": true,
        "os_cpu_virtual_time_us": 5092307,
        "os_cpu_wait_time_us": 19869,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137137744,
        "page_cache_miss_elapsed_us": 94000,
        "peak_memory_bytes": 2271985697,
        "query_class": "join",
        "query_id": "0810c65e-2c98-5cd1-b43c-bfb4c95a789a",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 49990447,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982642014979,
        "synchronous_read_wait_us": 183975,
        "system_time_us": 81603,
        "user_time_us": 5011627
      },
      {
        "disk_read_elapsed_us": 97317,
        "elapsed_seconds": 2.557,
        "file_descriptor_read_bytes": 137258157,
        "finished_at_unix_us": 1785982647417136,
        "gating": true,
        "os_cpu_virtual_time_us": 5131050,
        "os_cpu_wait_time_us": 10690,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 137258157,
        "page_cache_miss_elapsed_us": 96458,
        "peak_memory_bytes": 2260466005,
        "query_class": "join",
        "query_id": "3b30e5aa-2e1a-5868-8c48-f7db737325cd",
        "query_name": "q04",
        "read_bytes": 516587411,
        "read_rows": 35399795,
        "real_time_us": 51162102,
        "result_rows": 110456,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982644860739,
        "synchronous_read_wait_us": 186506,
        "system_time_us": 100269,
        "user_time_us": 5031564
      },
      {
        "disk_read_elapsed_us": 692404,
        "elapsed_seconds": 0.092,
        "file_descriptor_read_bytes": 416501254,
        "finished_at_unix_us": 1785982656779410,
        "gating": true,
        "os_cpu_virtual_time_us": 449992,
        "os_cpu_wait_time_us": 42218,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 416427481,
        "page_cache_miss_elapsed_us": 690979,
        "peak_memory_bytes": 2188584,
        "query_class": "one_hop",
        "query_id": "b730b9c4-9614-57b4-b429-efae8d8cca95",
        "query_name": "q05",
        "read_bytes": 563458944,
        "read_rows": 70432368,
        "real_time_us": 2805346,
        "result_rows": 0,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982656687371,
        "synchronous_read_wait_us": 1301992,
        "system_time_us": 163795,
        "user_time_us": 287924
      },
      {
        "disk_read_elapsed_us": 774042,
        "elapsed_seconds": 0.086,
        "file_descriptor_read_bytes": 413695666,
        "finished_at_unix_us": 1785982657211818,
        "gating": true,
        "os_cpu_virtual_time_us": 496355,
        "os_cpu_wait_time_us": 53067,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 413695666,
        "page_cache_miss_elapsed_us": 772548,
        "peak_memory_bytes": 2171542,
        "query_class": "one_hop",
        "query_id": "4c447197-0298-5dcc-863c-bb68268e94b7",
        "query_name": "q05",
        "read_bytes": 563555736,
        "read_rows": 70432368,
        "real_time_us": 2466458,
        "result_rows": 46,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982657125727,
        "synchronous_read_wait_us": 1128736,
        "system_time_us": 188412,
        "user_time_us": 309338
      },
      {
        "disk_read_elapsed_us": 804275,
        "elapsed_seconds": 0.085,
        "file_descriptor_read_bytes": 414158660,
        "finished_at_unix_us": 1785982657636156,
        "gating": true,
        "os_cpu_virtual_time_us": 489941,
        "os_cpu_wait_time_us": 61334,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 414158660,
        "page_cache_miss_elapsed_us": 803082,
        "peak_memory_bytes": 2253782,
        "query_class": "one_hop",
        "query_id": "cecc163f-7a64-5b1a-8a6b-67432d383cf3",
        "query_name": "q05",
        "read_bytes": 563590016,
        "read_rows": 70432368,
        "real_time_us": 2487846,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982657550483,
        "synchronous_read_wait_us": 1121037,
        "system_time_us": 198515,
        "user_time_us": 293204
      },
      {
        "disk_read_elapsed_us": 0,
        "elapsed_seconds": 0.001,
        "file_descriptor_read_bytes": 0,
        "finished_at_unix_us": 1785982657951159,
        "gating": true,
        "os_cpu_virtual_time_us": 1066,
        "os_cpu_wait_time_us": 0,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 0,
        "page_cache_miss_elapsed_us": 0,
        "peak_memory_bytes": 317264,
        "query_class": "one_hop",
        "query_id": "56847c14-8888-5648-b76e-e6bcc1efb0fe",
        "query_name": "q05",
        "read_bytes": 0,
        "read_rows": 0,
        "real_time_us": 1392,
        "result_rows": 0,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982657950011,
        "synchronous_read_wait_us": 0,
        "system_time_us": 24,
        "user_time_us": 1045
      },
      {
        "disk_read_elapsed_us": 263,
        "elapsed_seconds": 0.007,
        "file_descriptor_read_bytes": 105193,
        "finished_at_unix_us": 1785982658306504,
        "gating": true,
        "os_cpu_virtual_time_us": 11444,
        "os_cpu_wait_time_us": 22,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 105193,
        "page_cache_miss_elapsed_us": 258,
        "peak_memory_bytes": 355542,
        "query_class": "one_hop",
        "query_id": "05433fc9-a0fd-5105-a0bf-222b56ccdaee",
        "query_name": "q05",
        "read_bytes": 227864,
        "read_rows": 16384,
        "real_time_us": 31233,
        "result_rows": 46,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982658299136,
        "synchronous_read_wait_us": 485,
        "system_time_us": 10547,
        "user_time_us": 902
      },
      {
        "disk_read_elapsed_us": 213,
        "elapsed_seconds": 0.002,
        "file_descriptor_read_bytes": 83533,
        "finished_at_unix_us": 1785982658649743,
        "gating": true,
        "os_cpu_virtual_time_us": 2246,
        "os_cpu_wait_time_us": 20,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 83533,
        "page_cache_miss_elapsed_us": 211,
        "peak_memory_bytes": 435830,
        "query_class": "one_hop",
        "query_id": "4d1ec754-13eb-50d6-a22c-98ed007e69a9",
        "query_name": "q05",
        "read_bytes": 262144,
        "read_rows": 16384,
        "real_time_us": 6385,
        "result_rows": 3414,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982658647481,
        "synchronous_read_wait_us": 435,
        "system_time_us": 685,
        "user_time_us": 1566
      },
      {
        "disk_read_elapsed_us": 452,
        "elapsed_seconds": 0.004,
        "file_descriptor_read_bytes": 101562,
        "finished_at_unix_us": 1785982667733383,
        "gating": false,
        "os_cpu_virtual_time_us": 5616,
        "os_cpu_wait_time_us": 306,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 27789,
        "page_cache_miss_elapsed_us": 187,
        "peak_memory_bytes": 514648,
        "query_class": "two_hop",
        "query_id": "e3fe4ac0-fa86-5a02-8efd-25c540966369",
        "query_name": "q06",
        "read_bytes": 131072,
        "read_rows": 16384,
        "real_time_us": 35972,
        "result_rows": 1,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982667728995,
        "synchronous_read_wait_us": 624,
        "system_time_us": 3195,
        "user_time_us": 2440
      },
      {
        "disk_read_elapsed_us": 689806,
        "elapsed_seconds": 0.09,
        "file_descriptor_read_bytes": 452801894,
        "finished_at_unix_us": 1785982668158545,
        "gating": false,
        "os_cpu_virtual_time_us": 649682,
        "os_cpu_wait_time_us": 96954,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 452801894,
        "page_cache_miss_elapsed_us": 687497,
        "peak_memory_bytes": 6126540,
        "query_class": "two_hop",
        "query_id": "9d2e2953-22dd-5b31-b4e5-9cf8066454f2",
        "query_name": "q06",
        "read_bytes": 1126883608,
        "read_rows": 70432368,
        "real_time_us": 2492684,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982668067945,
        "synchronous_read_wait_us": 1106932,
        "system_time_us": 182673,
        "user_time_us": 469031
      },
      {
        "disk_read_elapsed_us": 716083,
        "elapsed_seconds": 0.097,
        "file_descriptor_read_bytes": 453088076,
        "finished_at_unix_us": 1785982668609714,
        "gating": false,
        "os_cpu_virtual_time_us": 696144,
        "os_cpu_wait_time_us": 96877,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 453088076,
        "page_cache_miss_elapsed_us": 713938,
        "peak_memory_bytes": 17722409,
        "query_class": "two_hop",
        "query_id": "31906d93-f6aa-506e-9e0d-98386489f28e",
        "query_name": "q06",
        "read_bytes": 1126917888,
        "read_rows": 70432368,
        "real_time_us": 2644261,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982668512739,
        "synchronous_read_wait_us": 1089358,
        "system_time_us": 198367,
        "user_time_us": 499451
      },
      {
        "disk_read_elapsed_us": 95,
        "elapsed_seconds": 0.003,
        "file_descriptor_read_bytes": 8840,
        "finished_at_unix_us": 1785982668962033,
        "gating": false,
        "os_cpu_virtual_time_us": 4390,
        "os_cpu_wait_time_us": 15,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 8840,
        "page_cache_miss_elapsed_us": 93,
        "peak_memory_bytes": 496384,
        "query_class": "two_hop",
        "query_id": "8be06a02-9757-5ba0-b974-acaa423bac3f",
        "query_name": "q06",
        "read_bytes": 131072,
        "read_rows": 16384,
        "real_time_us": 22552,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": 25441,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982668958991,
        "synchronous_read_wait_us": 195,
        "system_time_us": 2509,
        "user_time_us": 1895
      },
      {
        "disk_read_elapsed_us": 741052,
        "elapsed_seconds": 0.096,
        "file_descriptor_read_bytes": 452995302,
        "finished_at_unix_us": 1785982669386126,
        "gating": false,
        "os_cpu_virtual_time_us": 675025,
        "os_cpu_wait_time_us": 84934,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 452995302,
        "page_cache_miss_elapsed_us": 739490,
        "peak_memory_bytes": 5926933,
        "query_class": "two_hop",
        "query_id": "ca252312-d31a-51f9-97b5-8e8957b9d0f9",
        "query_name": "q06",
        "read_bytes": 1126883608,
        "read_rows": 70432368,
        "real_time_us": 2622264,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": 1491165,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982669289979,
        "synchronous_read_wait_us": 1112707,
        "system_time_us": 206686,
        "user_time_us": 470056
      },
      {
        "disk_read_elapsed_us": 743390,
        "elapsed_seconds": 0.098,
        "file_descriptor_read_bytes": 452943385,
        "finished_at_unix_us": 1785982669830326,
        "gating": false,
        "os_cpu_virtual_time_us": 696951,
        "os_cpu_wait_time_us": 86761,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 452943385,
        "page_cache_miss_elapsed_us": 741716,
        "peak_memory_bytes": 14826777,
        "query_class": "two_hop",
        "query_id": "06e16dca-0cb0-5a21-a590-9ab54e9aecf3",
        "query_name": "q06",
        "read_bytes": 1126917888,
        "read_rows": 70432368,
        "real_time_us": 2650943,
        "result_rows": 1,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": 4388957908,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982669732355,
        "synchronous_read_wait_us": 1113874,
        "system_time_us": 193035,
        "user_time_us": 505724
      },
      {
        "disk_read_elapsed_us": 813191,
        "elapsed_seconds": 1.23,
        "file_descriptor_read_bytes": 901935490,
        "finished_at_unix_us": 1785982681060260,
        "gating": true,
        "os_cpu_virtual_time_us": 17115920,
        "os_cpu_wait_time_us": 1004818,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426934520,
        "page_cache_miss_elapsed_us": 263520,
        "peak_memory_bytes": 6547124429,
        "query_class": "routine",
        "query_id": "98beb1b8-f4dc-5c3f-8698-b25017f646c8",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 24528396,
        "result_rows": 1000,
        "run_kind": "post_restart_run",
        "run_number": 0,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982679849359,
        "synchronous_read_wait_us": 1103298,
        "system_time_us": 594267,
        "user_time_us": 16523648
      },
      {
        "disk_read_elapsed_us": 796262,
        "elapsed_seconds": 1.21,
        "file_descriptor_read_bytes": 901109018,
        "finished_at_unix_us": 1785982682641582,
        "gating": true,
        "os_cpu_virtual_time_us": 16981114,
        "os_cpu_wait_time_us": 902727,
        "os_read_bytes": 20480,
        "page_cache_miss_bytes": 426443684,
        "page_cache_miss_elapsed_us": 252036,
        "peak_memory_bytes": 5779642395,
        "query_class": "routine",
        "query_id": "8f02c1e1-b7c5-5c70-90de-d5aac44f331b",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 24077582,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 1,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982681449710,
        "synchronous_read_wait_us": 1279166,
        "system_time_us": 544946,
        "user_time_us": 16438503
      },
      {
        "disk_read_elapsed_us": 749556,
        "elapsed_seconds": 1.199,
        "file_descriptor_read_bytes": 902188479,
        "finished_at_unix_us": 1785982684183344,
        "gating": true,
        "os_cpu_virtual_time_us": 17122128,
        "os_cpu_wait_time_us": 1073861,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426945754,
        "page_cache_miss_elapsed_us": 235382,
        "peak_memory_bytes": 6480259349,
        "query_class": "routine",
        "query_id": "58755398-ae4b-5258-8d79-71348767369e",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 23616056,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 2,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982683016378,
        "synchronous_read_wait_us": 956806,
        "system_time_us": 562859,
        "user_time_us": 16561363
      },
      {
        "disk_read_elapsed_us": 780799,
        "elapsed_seconds": 1.194,
        "file_descriptor_read_bytes": 902140445,
        "finished_at_unix_us": 1785982685741112,
        "gating": true,
        "os_cpu_virtual_time_us": 17043404,
        "os_cpu_wait_time_us": 973456,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426849353,
        "page_cache_miss_elapsed_us": 247506,
        "peak_memory_bytes": 6279311629,
        "query_class": "routine",
        "query_id": "ca0b271f-58da-5e7a-ae72-b5fb29797641",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 23738542,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 3,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982684567898,
        "synchronous_read_wait_us": 1006336,
        "system_time_us": 560602,
        "user_time_us": 16485244
      },
      {
        "disk_read_elapsed_us": 768462,
        "elapsed_seconds": 1.252,
        "file_descriptor_read_bytes": 902199001,
        "finished_at_unix_us": 1785982687339062,
        "gating": true,
        "os_cpu_virtual_time_us": 16991086,
        "os_cpu_wait_time_us": 791673,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 427285146,
        "page_cache_miss_elapsed_us": 248691,
        "peak_memory_bytes": 6043991985,
        "query_class": "routine",
        "query_id": "590f6f1c-a94f-543d-9cc9-292c8eca5018",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 24684564,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 4,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982686118993,
        "synchronous_read_wait_us": 1270773,
        "system_time_us": 592027,
        "user_time_us": 16401203
      },
      {
        "disk_read_elapsed_us": 818020,
        "elapsed_seconds": 1.235,
        "file_descriptor_read_bytes": 901330989,
        "finished_at_unix_us": 1785982688945984,
        "gating": true,
        "os_cpu_virtual_time_us": 17404487,
        "os_cpu_wait_time_us": 1202704,
        "os_read_bytes": 0,
        "page_cache_miss_bytes": 426739802,
        "page_cache_miss_elapsed_us": 240103,
        "peak_memory_bytes": 6145882077,
        "query_class": "routine",
        "query_id": "37eecc92-ac52-54ae-8794-7f5398c6662d",
        "query_name": "q07",
        "read_bytes": 774575824,
        "read_rows": 70415984,
        "real_time_us": 24570030,
        "result_rows": 1000,
        "run_kind": "warm_run",
        "run_number": 5,
        "seed_work_id": null,
        "spill_bytes": 0,
        "started_at_unix_us": 1785982687730826,
        "synchronous_read_wait_us": 1086782,
        "system_time_us": 632464,
        "user_time_us": 16774131
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
      "filesystem_bytes": 1810870272,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {},
      "timestamp": 1785982450.7055418
    },
    {
      "filesystem_bytes": 1810870272,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 195137916
      },
      "timestamp": 1785982451.935754
    },
    {
      "filesystem_bytes": 1810870272,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 412987097
      },
      "timestamp": 1785982453.153811
    },
    {
      "filesystem_bytes": 1810870272,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 660862371
      },
      "timestamp": 1785982454.3578172
    },
    {
      "filesystem_bytes": 1810870272,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 905113137
      },
      "timestamp": 1785982455.572178
    },
    {
      "filesystem_bytes": 1810870272,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1156637809
      },
      "timestamp": 1785982456.800863
    },
    {
      "filesystem_bytes": 1810870272,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1401645002
      },
      "timestamp": 1785982458.0093231
    },
    {
      "filesystem_bytes": 1810870272,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1655780113
      },
      "timestamp": 1785982459.245413
    },
    {
      "filesystem_bytes": 1810870272,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 1901383720
      },
      "timestamp": 1785982460.48947
    },
    {
      "filesystem_bytes": 1810870272,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2143606194
      },
      "timestamp": 1785982461.71542
    },
    {
      "filesystem_bytes": 1810870272,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2386983508
      },
      "timestamp": 1785982462.9456341
    },
    {
      "filesystem_bytes": 1810870272,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2637628011
      },
      "timestamp": 1785982464.171808
    },
    {
      "filesystem_bytes": 1810870272,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 2883879653
      },
      "timestamp": 1785982465.414121
    },
    {
      "filesystem_bytes": 1810870272,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3074059327
      },
      "timestamp": 1785982466.640815
    },
    {
      "filesystem_bytes": 1810870272,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3320070198
      },
      "timestamp": 1785982467.8697758
    },
    {
      "filesystem_bytes": 10724585472,
      "filesystem_vanished_directories": 0,
      "filesystem_vanished_files": 0,
      "projection_bytes": {},
      "table_bytes": {
        "authors": 3400460221,
        "institutions": 4357308,
        "sources": 10677280,
        "topics": 150309
      },
      "timestamp": 1785982468.664284
    }
  ],
  "tiers": {
    "stage2_medium": [
      {
        "filesystem_bytes": 11872862208,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3371491578,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309
        },
        "timestamp": 1785982474.3971992
      },
      {
        "filesystem_bytes": 11872862208,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3371491578,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 160865996
        },
        "timestamp": 1785982475.574949
      },
      {
        "filesystem_bytes": 11872862208,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3371491578,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 220508410
        },
        "timestamp": 1785982476.834099
      },
      {
        "filesystem_bytes": 11872862208,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348671848,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213817788
        },
        "timestamp": 1785982478.061692
      },
      {
        "filesystem_bytes": 11872862208,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348671848,
          "citation_edge": 33452144,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213817788
        },
        "timestamp": 1785982479.330197
      },
      {
        "filesystem_bytes": 11872862208,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348671848,
          "citation_edge": 176230116,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213817788
        },
        "timestamp": 1785982480.5406091
      },
      {
        "filesystem_bytes": 11872862208,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348671848,
          "citation_edge": 303661352,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213817788
        },
        "timestamp": 1785982481.75327
      },
      {
        "filesystem_bytes": 11872862208,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348671848,
          "citation_edge": 455461639,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213817788
        },
        "timestamp": 1785982482.970117
      },
      {
        "filesystem_bytes": 11872862208,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348671848,
          "citation_edge": 594081583,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "works": 213817788
        },
        "timestamp": 1785982484.287956
      },
      {
        "filesystem_bytes": 11872862208,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348671848,
          "citation_edge": 580794615,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 100137273,
          "works": 213817788
        },
        "timestamp": 1785982485.541735
      },
      {
        "filesystem_bytes": 11872862208,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348671848,
          "citation_edge": 516258604,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159100767,
          "works": 213817788
        },
        "timestamp": 1785982486.76217
      },
      {
        "filesystem_bytes": 11872862208,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348671848,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159100767,
          "work_institution": 36428763,
          "works": 213817788
        },
        "timestamp": 1785982487.987778
      },
      {
        "filesystem_bytes": 11872862208,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348671848,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159100767,
          "work_institution": 69529976,
          "works": 213817788
        },
        "timestamp": 1785982489.212685
      },
      {
        "filesystem_bytes": 11872862208,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348671848,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159100767,
          "work_institution": 104057691,
          "work_topic": 30902400,
          "works": 213817788
        },
        "timestamp": 1785982490.450291
      },
      {
        "filesystem_bytes": 11872862208,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348671848,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159100767,
          "work_institution": 100937535,
          "work_topic": 161583684,
          "works": 213817788
        },
        "timestamp": 1785982491.659864
      },
      {
        "filesystem_bytes": 15234535424,
        "filesystem_vanished_directories": 0,
        "filesystem_vanished_files": 0,
        "projection_bytes": {},
        "table_bytes": {
          "authors": 3348671848,
          "citation_edge": 461584771,
          "institutions": 4357308,
          "sources": 10677280,
          "topics": 150309,
          "work_author": 159100767,
          "work_institution": 100937535,
          "work_topic": 202506961,
          "works": 213817788
        },
        "timestamp": 1785982492.310493
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
